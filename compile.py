#import compiler
import explicate
import sys
import x86AST
#from compiler.ast import *
from x86AST import *
from explicate import *

class flatParser:
  def __init__(self, ast):
    self.tmp = 0
    self.ast = ast
    self.flat = []
    self.ifTmp =0

  def flatAst(self, ast):
    if isinstance(ast,Module):
      self.flatAst(ast.node)

    elif isinstance(ast,Stmt):
      for stmt in ast.nodes:
        self.flatAst(stmt)

    elif isinstance(ast,Printnl):
      print "@@@@@@@@@@@@@@"
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

    elif isinstance(ast,Add):
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
      argFlat = [self.flatAst(arg) for arg in ast.args]
      newTmp = self.getNewTmp()
      self.flat.append(Assign(newTmp, CallFunc(ast.node,argFlat)))
      newTmp2 = self.getNewTmp()
      self.flat.append(Assign(newTmp2, newTmp))
      return newTmp2

    elif isinstance(ast,Compare):
      #print ast.expr
      #print ast.ops
      l = self.flatAst(ast.expr)
      r = self.flatAst(ast.ops[0][1])
      newTmp = self.getNewTmp()
      self.flat.append(Assign(newTmp,Compare(l,[(ast.ops[0][0],r)])))

    elif isinstance(ast,Not):
        newTmp = self.getNewTmp()
        child = self.flatAst(ast.expr)
        self.flat.append(Assign(newTmp,Not(child)))
        return newTmp

    elif isinstance(ast,List):
        print ast.nodes

    elif isinstance(ast,Dict):
        print self.items

    elif isinstance(ast,Subscript):
        print self.expr
        print self.flags
        print self.subs
    elif isinstance(ast,IfExp):
        condTmp = self.getNewTmp()
        newTmp = self.getNewTmp()
        test = self.flatAst(ast.test)
        self.flat.append(Assign(condTmp,test))

        (ifName,elifName,endName) = self.getIfTmp()
        #(ifName,elifName,endName) = (Name("if"),Name("then"),Name("if"))
        self.flat.append(ifName)
        then = self.flatAst(ast.then)
        self.flat.append(Assign(newTmp,then))

        self.flat.append(elifName)
        else_ = self.flatAst(ast.else_)
        self.flat.append(Assign(newTmp,else_))

        self.flat.append(endName)
        return newTmp
    elif isinstance(ast,InjectFrom):
        child = self.flatAst(ast.arg)
        newTmp = self.getNewTmp()
        self.flat.append(Assign(newTmp, InjectFrom(ast.typ,child)))
        return newTmp
    elif isinstance(ast,ProjectTo):
        child = self.flatAst(ast.arg)
        newTmp = self.getNewTmp()
        self.flat.append(Assign(newTmp, ProjectTo(ast.typ,child)))
        return newTmp

    elif isinstance(ast, Let):
        rhs = self.flatAst(ast.rhs)
        self.flat.append(Assign(ast.var,rhs))
        newTmp1 = self.getNewTmp()
        child = self.flatAst(ast.body)
        self.flat.append(Assign(newTmp1,child))
        return newTmp1
    elif isinstance(ast,IsType):
        child = self.flatAst(ast.var)
        newTmp = self.getNewTmp()
        funcName = Name("is_%s" % ast.typ )
        self.flat.append(Assign(newTmp, CallFunc(funcName, [child])))
        self.flat.append(Assign(newTmp, InjectFrom('bool',newTmp)))
        return newTmp
    elif isinstance(ast,ThrowErr):
        return ast

    else:
        print "***error:", ast
        pass

  def getNewTmp(self):
      newTmp = Name('tmp '+`self.tmp`)
      self.tmp += 1
      return newTmp
  def getIfTmp(self):
      ifName = Name('if '+`self.ifTmp`)
      elifName = Name('else '+`self.ifTmp`)
      endName = Name('end '+`self.ifTmp`)
      self.tmp += 1
      return (ifName,elifName,endName)

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
    self.cmp =0

  def convert86(self):
      for curLine in self.flatAst:
          if isinstance(curLine, Assign):
              self.convertLine(curLine.expr, NameOp(curLine.nodes.name))
          elif isinstance(curLine, Printnl):
              self.output.append(PrintOp(self.getConstOrName(curLine.nodes[0])))
          if isinstance(curLine,Name):
              pass
          elif isinstance(curLine, UnarySub):
              #check to delete
              self.output.append(UnaryOp("negl", NameOp(curLine.expr.name)))


  def convertLine(self,curLine,tmpName):
      if isinstance(curLine,Add):
          self.output.append(BinaryOp("movl", self.getConstOrName(curLine.left), tmpName))
          self.output.append(BinaryOp("addl", self.getConstOrName(curLine.right), tmpName))
      elif isinstance(curLine, Const):
          self.output.append(BinaryOp("movl", ConstOp(curLine.value), tmpName))
      elif isinstance(curLine, Name):
          self.output.append(BinaryOp("movl", NameOp(curLine.name), tmpName))
      elif isinstance(curLine, UnarySub):
          #print "wrong"
          self.output.append(BinaryOp("movl", NameOp(curLine.expr.name), tmpName))
          self.output.append(UnaryOp("negl", tmpName))
      elif isinstance(curLine, CallFunc):
          #if not curLine.node.name in ["input", "is_true", "is_int","is_bool","is_big", "equals"]:
          #    print "Trying to call ", curLine.node.name
          self.output.append(FuncOp(curLine.node.name,[self.getConstOrName(arg) for arg in curLine.args],tmpName))
      elif isinstance(curLine, InjectFrom):
          funcName = Name("project_%s"%(curLine.typ))
          self.output.append(FuncOp(funcName,[self.getConstOrName(curLine.arg)],tmpName))
      elif isinstance(curLine, ProjectTo):
          funcName = Name("inject_%s"%(curLine.typ))
          self.output.append(FuncOp(funcName,[self.getConstOrName(curLine.arg.name)],tmpName))
          #self.output.append(FuncOp(funcName,[curLine.arg],tmpName))
      elif isinstance(curLine,Not):
          self.output.append(BinaryOp("movl", NameOp(curLine.expr),tmpName))
          self.output.append(UnaryOp("notl",tmpName))
      elif isinstance(curLine,Compare):
          self.output.append(CompareOp(self.getConstOrName(curLine.expr),self.getConstOrName(curLine.ops[0][1])))
          (neCmp,endCmp) = self.getCmpLabel()
          
          self.output.append(JumpOp("jne",neCmp))
          self.output.append(BinaryOp("movl", ConstOp(1) ,tmpName))
          self.output.append(JumpOp("jne",endCmp))
          self.output.append(ClauseOp(neCmp))
          self.output.append(BinaryOp("movl", ConstOp(0) ,tmpName))
          self.output.append(ClauseOp(endCmp))

      else:
          print "Assign Error:",curLine 

  def getConstOrName(self, line):
    if isinstance(line, Name):
      return  NameOp(line.name)
    elif isinstance(line,Name):
      return ConstOp(line.value)
    else:
      return None

  def getAddr(self,varName):
    if varName not in self.varLookup:
      self.varLookup[varName] = self.varCounter
      self.varCounter+=4
    return self.varLookup[varName]
  def getCmpLabel(self):
      neCmp = NameOp('ne_cmp'+`self.cmp`)
      endCmp = NameOp('end_cmp'+`self.cmp`)
      self.cmp += 1
      return (neCmp,endCmp)

if __name__ == "__main__":
  with open (sys.argv[1], "r") as myfile:
    inStr=myfile.read()

  ast = compiler.parse(inStr)
  #print ast
  myExplicate = ExplicateParser(ast)
  ast = myExplicate.explicate(ast)
  print "@@@@@@@@@@"
  #print ast

  parser = flatParser(ast)

  parser.flatAst(parser.ast)
  parser.printFlat()
  to86 = pyTo86(parser.flat,parser.tmp)
  to86.convert86()
  for line in to86.output: print line 
  ig = InterferenceGraph()

  output = ig.createLiveness(to86.output)
  #output
  #igcolor = ig.colorGraph()
  #ig.cleanUpCrew(to86.output,igcolor)

  outFileName = sys.argv[1].replace('.py','.s')
  fout = open(outFileName, 'w+')
  fout.write(output)
