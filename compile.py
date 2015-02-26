import compiler
import sys
import x86AST
from compiler.ast import *
from x86AST import *

class GetTag(Node):
    def __init__(self, arg):
        self.arg = arg
class InjectFrom(Node):
    def __init__(self, typ, arg):
        self.typ = typ
        self.arg = arg
class ProjectTo(Node):
    def __init__(self, typ, arg):
        self.typ = typ
        self.arg = arg
class Let(Node):
    def __init__(self, var, rhs, body):
        self.var = var
        self.rhs = rhs
        self.body = body

class flatParser:
  def __init__(self, ast):
    self.tmp = 0
    self.ast = ast
    self.flat = []

  def flatAst(self, ast):
    if isinstance(ast,Module):
      self.flatAst(ast.node)

    elif isinstance(ast,Stmt):
      for stmt in ast.nodes:
        self.flatAst(stmt)

    elif isinstance(ast,Printnl):
      child = self.flatAst(ast.nodes[0])
      if isinstance(child, Const):
          newTmp = self.getNewTmp()
          self.flat.append(Assign(newTmp,child))
          child= newTmp
      self.flat.append(Printnl([child],None))

    elif isinstance(ast,Assign):
      varVal = self.flatAst(ast.expr)
      for node in ast.nodes:
        varName = self.flatAst(node)
        self.flat.append(Assign(varName, varVal))
        self.tmp += 1
      return varVal

    elif isinstance(ast,AssName):
      return Name(ast.name)

    elif isinstance(ast,Discard):
      child = self.flatAst(ast.expr)
      if isinstance(child,CallFunc):
        self.flat.append(child)

    elif isinstance(ast,Const):
      return ast

    elif isinstance(ast,Name):
      return ast

    elif isinstance(ast,Add): #Add
        l = self.flatAst(ast.left)
        r = self.flatAst(ast.right)
        if(isinstance(l,Const) and isinstance(r,Const)):
            return Const(l.value+r.value)
        # self.flat.append(IfExp(And([Compare(GetTag(l),[('==',0)]),Compare(GetTag(l),[('==',0)])),
        # Add(ProjectTo('int',l),ProjectTo('int',r)),
        # IfExp(And([Compare(GetTag(l),[('==',2)]),Compare(GetTag(l),[('==',2)])),
        # Add(ProjectTo('big',l),ProjectTo('big',r)),
        # nil)))


        newTmp = self.getNewTmp()
        self.flat.append(Assign(newTmp, Add((l,r))))
        return newTmp

    elif isinstance(ast,UnarySub):
      child = self.flatAst(ast.expr)
      if isinstance(child, Const):
        child = Const(-child.value)
        newTmp = child
      else:
        newTmp = self.getNewTmp()
        self.flat.append(Assign(newTmp,UnarySub(child)))
      return newTmp

    elif isinstance(ast,CallFunc):
      newTmp = self.getNewTmp()
      self.flat.append(Assign(newTmp, ast))
      newTmp2 = self.getNewTmp()
      self.flat.append(Assign(newTmp2, newTmp))
      return newTmp2

    elif isinstance(ast,Compare):
      print ast.expr
      print ast.ops

    elif isinstance(ast,Or):
      print ast.nodes

    elif isinstance(ast,And):
      print ast.nodes

    elif isinstance(ast,Not):
      print ast.expr

    elif isinstance(ast,List):
      print ast.nodes

    elif isinstance(ast,Dict):
      print self.items

    elif isinstance(ast,Subscript):
      print self.expr
      print self.flags
      print self.subs
    elif isinstance(ast,IfExp):
      print ast.test
      print ast.then
      print ast.else_
    else:
      pass

  def getNewTmp(self):
      newTmp = Name('tmp '+`self.tmp`)
      self.tmp += 1
      return newTmp

  def printFlat(self):
    print "*****Args*****"
    for args in self.flat:
      print args

class pyTo86:
  def __init__(self, flatAst, stackSize):
    self.flatAst = flatAst
    self.stackSize = stackSize
    self.output = []
    self.varLookup = {}
    self.varCounter = 4

  def convert86(self):
    for curLine in self.flatAst:
      if isinstance(curLine, Assign):
        self.convertLine(curLine.expr, curLine.nodes.name)
      elif isinstance(curLine, Printnl):
        self.output.append(PrintOp(self.getConstOrName(curLine.nodes[0])))
      elif isinstance(curLine, UnarySub):
          self.output.append(UnaryOp("negl", NameOp(curLine.expr.name)))

      #elif isinstance(curLine,UnarySub):
      #  if isinstance(curLine.expr, Name):
      #    self.output.append(UnaryOp("negl", NameOp(curLine.expr.name)))
      #  else:
      #    pass

  def convertLine(self,curLine,tmpName):
    if isinstance(curLine,Add):
      self.output.append(BinaryOp("movl", self.getConstOrName(curLine.left), NameOp(tmpName)))
      self.output.append(BinaryOp("addl", self.getConstOrName(curLine.right), NameOp(tmpName)))
    elif isinstance(curLine, Const):
      self.output.append(BinaryOp("movl", ConstOp(curLine.value), NameOp(tmpName)))
    elif isinstance(curLine, Name):
      self.output.append(BinaryOp("movl", NameOp(curLine.name), NameOp(tmpName)))
    elif isinstance(curLine, UnarySub):
      #print "wrong"
      self.output.append(BinaryOp("movl", NameOp(curLine.expr.name), NameOp(tmpName)))
      self.output.append(UnaryOp("negl", NameOp(tmpName)))
    elif isinstance(curLine, CallFunc):
      self.output.append(FuncOp("input", tmpName))

  def getConstOrName(self, line):
    if isinstance(line, Name):
      return  NameOp(line.name)
    else:
      return ConstOp(line.value)

  def getConstOrNamePrint(self, line):
    if isinstance(line, Name):
      return "\tmovl -%d(%%ebp), %%eax\n" % self.getAddr(line.name)
    else:
      return "\tmovl $%d, %%eax" % line.value

  def getAddr(self,varName):
    if varName not in self.varLookup:
      self.varLookup[varName] = self.varCounter
      self.varCounter+=4
    return self.varLookup[varName]

  def endStack(self):
    self.output+=("\tmovl $0,%eax\n")
    self.output+=("\tleave\n")
    self.output+=("\tret\n")


if __name__ == "__main__":
  with open (sys.argv[1], "r") as myfile:
    inStr=myfile.read()

  ast = compiler.parse(inStr)
  parser = flatParser(ast)
  #print inStr, "\n"
  print ast

  parser.flatAst(parser.ast)
  parser.printFlat()
  to86 = pyTo86(parser.flat,parser.tmp)
  to86.convert86()
  #to86.endStack()
  #print "\n"
  #for line in to86.output:
  #  print line
  #print to86.output
  ig = InterferenceGraph()

  output = ig.createLiveness(to86.output)
  #output
  #igcolor = ig.colorGraph()
  #ig.cleanUpCrew(to86.output,igcolor)

  outFileName = sys.argv[1].replace('.py','.s')
  fout = open(outFileName, 'w+')
  fout.write(output)
