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
    def __repr__(self):
        return "InjectFrom(%s,%s)" % (self.typ,self.arg)
class ProjectTo(Node):
    def __init__(self, typ, arg):
        self.typ = typ
        self.arg = arg
    def __repr__(self):
        return "ProjectTo(%s,%s)" % (self.typ,self.arg)
class Let(Node):
    def __init__(self, var, rhs, body):
        self.var = var
        self.rhs = rhs
        self.body = body
    def __repr__(self):
        return "Let(%s,%s,%s)" % (self.var,self.rhs,self.body)
class ThrowErr(Node):
    def __init__(self,strName):
        self.strName = strName
class IsType(Node):
    def __init__(self,typ, var):
        self.typ = typ
        self.var = var
    def __repr__(self):
        return "IsType(%s,%s)" % (self.typ,self.var)

class ExplicateParser:
    def __init__(self, ast):
        self.tmp = 0
        self.ast = ast
        #self.flat = []
    def explicate(self,ast):
        if isinstance(ast,Module):
            return Module(ast.doc,self.explicate(ast.node))
        elif isinstance(ast,Stmt):
            return Stmt([self.explicate(stmt) for stmt in ast.nodes])
        elif isinstance(ast,Printnl):
            return Printnl(self.explicate(ast.nodes),ast.dest)
        elif isinstance(ast,Assign):
            return Assign([ast.nodes[0]], self.explicate(ast.expr))
        elif isinstance(ast,AssName):
            return ast
        elif isinstance(ast,Discard):
            return Discard(self.explicate(ast.expr))
        elif isinstance(ast,Const):
            return ast
        elif isinstance(ast,Name):
            return ast
        elif isinstance(ast,Add):
            l = self.explicate(ast.left)
            r = self.explicate(ast.right)

            name1 = self.getNewTmp()
            name2 = self.getNewTmp()


            leftWord = self.explicate(Or([IsType('int',name1),IsType('bool',name1)]))
            rightWord = self.explicate(Or([IsType('int',name2),IsType('bool',name2)]))
            leftBig = IsType('big', name1)
            rightBig = IsType('big', name2)

            ifExp = IfExp(self.explicate(And([leftWord,rightWord])),InjectFrom('int', Add(ProjectTo('int',name1),ProjectTo('int',name2))),
                IfExp(self.explicate(And([leftBig,rightBig])),InjectFrom('big',(Add(ProjectTo('big',name1),ProjectTo('big',name2)))), ThrowErr('add_error')))

            return Let(name1, l,Let(name2,r,ifExp))

        elif isinstance(ast,UnarySub):
            child = self.explicate(ast.expr)
            name = self.getNewTmp()

            orStmt= self.explicate(Or([IsType('int',name),IsType('bool',name)]))

            ifExp = IfExp(orStmt,InjectFrom('int', UnarySub(ProjectTo('int',name))), ThrowErr('unarysub_error'))
            return Let(name,child,ifExp)

        elif isinstance(ast,CallFunc):
            return ast
            #TODO: explicate over args

        elif isinstance(ast,Compare):
            l = self.explicate(ast.expr)
            r = self.explicate(ast.ops[0][1])

            name1 = self.getNewTmp()
            name2 = self.getNewTmp()
            op = ast.ops[0][0]

            if op == '==' or op == '!=':
                funcName = 'equals' if op == '==' else 'not_equals'
                leftWord = self.explicate(Or([IsType('int',name1),IsType('bool',name1)]))
                rightWord = self.explicate(Or([IsType('int',name2),IsType('bool',name2)]))
                leftBig = IsType('big', name1)
                rightBig = IsType('big', name2)

                ifExp = IfExp(self.explicate(And([leftWord,rightWord])),InjectFrom('bool', Compare(name1,[op, name2])),
                IfExp(self.explicate(And([leftBig,rightBig])),InjectFrom('bool',CallFunc(funcName,[ProjectTo('big',name1),ProjectTo('big',name2)])), Name("False")))

                return Let(name1,l,Let(name2,r,ifExp))
            elif op == 'is':
                return Compare(l,[op,r])
            else:
                print "Error Compare"
                exit()


        elif isinstance(ast,Or):
            pass
        elif isinstance(ast,And):
            
            pass

        elif isinstance(ast,Not):
            pass

        elif isinstance(ast,List):
            pass

        elif isinstance(ast,Dict):
            pass

        elif isinstance(ast,Subscript):
            pass
        elif isinstance(ast,IfExp):
            pass
        else:
          pass
    def getNewTmp(self):
      newTmp = Name('expl '+`self.tmp`)
      self.tmp += 1
      return newTmp


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
  print ast
  myExplicate = ExplicateParser(ast)
  ast = myExplicate.explicate(ast)
  print ast

  parser = flatParser(ast)
  #print inStr, "\n"

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
