import compiler
from compiler.ast import *


class flatParser:
  def __init__(self, ast):
    self.tmp = 0
    self.ast = ast
    self.flat = []

  def flatAst(self, ast):
    if isinstance(ast,Module):
      print "Module"
      # return Module(None, flatAst(ast.node))
      self.flatAst(ast.node)
    elif isinstance(ast,Stmt):
      for stmt in ast.nodes:
        print "****Stmt Start****"
        # return Stmt(self.flatAst(stmt))
        self.flatAst(stmt)
        print "****Stmt End****"
    elif isinstance(ast,Printnl):
      child = self.flatAst(ast.nodes[0])
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
      print "Discard"
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

      newTmp = Name('tmp '+`self.tmp`)
      self.flat.append(Assign(newTmp, Add((l,r))))
      self.tmp += 1
      return newTmp

    elif isinstance(ast,UnarySub):
      child = self.flatAst(ast.expr)
      newTmp = Name('tmp '+`self.tmp`)
      self.flat.append(Assign(newTmp, UnarySub(child)))
      self.tmp += 1
      return newTmp
    elif isinstance(ast,CallFunc):
      newTmp = Name('tmp '+`self.tmp`)
      self.flat.append(Assign(newTmp, ast))
      self.tmp += 1
      return newTmp
    else:
      print "Ended"
  def printFlat(self):
    print "*****Args*****"
    for args in self.flat:
      print args

class pyTo86:
  def __init__(self, flatAst, stackSize):
    self.flatAst = flatAst
    self.stackSize = stackSize*4
    self.output = ""
    self.varLookup = {}
    self.varCounter = 4

  def startStack(self):
    self.output+=(".globl main\nmain:\n")
    self.output+=("\tpushl %ebp\n")
    self.output+=("\tmovl %esp, %ebp\n")
    self.output+=("\tsubl $%d, %%esp\n" % self.stackSize)
    #print self.output

  def convert86(self):
    for curLine in self.flatAst:
      if isinstance(curLine, Assign):
        print curLine.nodes.name
        self.convertLine(curLine.expr, curLine.nodes.name)
        #self.output
        #self.output+="movl "
        #self.varLookup[curLine.name] = self.varCounter
        #self.varCounter += 1
  def convertLine(self,curLine,tmpName):
    if isinstance(curLine,Add):
      print "Add"
    elif isinstance(curLine,Const):
      self.output+=("\tmovl $%d,-%d(%%ebp)\n"% (curLine.value,self.getAddr(tmpName)) )
    elif isinstance(curLine,Name):
      self.output+=("\tmovl -%d(%%ebp),%%eax\n"% self.getAddr(curLine.name))
      self.output+=("\tmovl %%eax,-%d(%%ebp)\n"%self.getAddr(tmpName))
    elif isinstance(curLine,UnarySub):
      print "Sub"
    elif isinstance(curLine,CallFunc):
      print "Input"

  def getAddr(self,varName):
    print varName
    if varName not in self.varLookup:
      self.varLookup[varName] = self.varCounter
      self.varCounter+=4
    return self.varLookup[varName]

  def endStack(self):
    self.output+=("\tmovl $0,%eax\n")
    self.output+=("\tleave\n")
    self.output+=("\tret\n")


if __name__ == "__main__":
  fout = open('test.s', 'w+')
  inStr = "x=2\ny=x\nx=4"
  ast = compiler.parse(inStr)
  parser = flatParser(ast)
  print inStr, "\n"
  print ast

  parser.flatAst(parser.ast)
  parser.printFlat()
  to86 = pyTo86(parser.flat,parser.tmp)
  to86.startStack()
  to86.convert86()
  to86.endStack()
  print "\n"
  print to86.output
  fout.write(to86.output)
