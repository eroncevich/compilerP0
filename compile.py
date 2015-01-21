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
      return ast
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

  def setStack(self):
    self.output+=(".globl main\nmain:\n")
    self.output+=("pushl %ebp\n")
    self.output+=("movl %esp, %ebp\n")
    self.output+=("subl $%d, %%ebp\n" % self.stackSize)
    print self.output

  def convert86(self):
    self.output+=setStack
    for curLine in self.flatAst:
      if isinstance(curLine, Assign):
        self.output
        self.output+="movl "
      if isinstance(curLine,Add):
        print "hi"
  def convertLine(self,curLine):
    if isinstance(curLine,Add):
      print "hi"


if __name__ == "__main__":
  fout = open('test.s', 'w+')
  inStr = "print 3+2+1"
  ast = compiler.parse(inStr)
  parser = flatParser(ast)
  print inStr, "\n"
  print ast

  parser.flatAst(parser.ast)
  parser.printFlat()
  to86 = pyTo86(parser.flat,parser.tmp)
  to86.setStack()
