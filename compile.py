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
    self.output+=("\n.globl main\nmain:\n")
    self.output+=("pushl %ebp\n")
    self.output+=("movl %esp, %ebp\n")
    self.output+=("subl $%d, %%ebp\n" % self.stackSize)
    #print self.output

  def convert86(self):
    #self.output+=sesetStack
    for curLine in self.flatAst:
      if isinstance(curLine, Assign):
        if curLine.nodes not in self.varLookup:
          self.varLookup[curLine.nodes] = self.varCounter
          self.varCounter+=4
        print curLine.nodes
        print self.varLookup
        #print self.varLookup(curLine.nodes)
        self.convertLine(curLine.expr, self.varLookup[curLine.nodes])
        self.output += ("movl %%eax, -%d(%%ebp)\n" % self.varLookup[curLine.nodes])
        #self.output
        #self.output+="movl "
        #self.varLookup[curLine.name] = self.varCounter
        #self.varCounter += 1
      #if isinstance(curLine,Add):
        #print "hi"
      elif isinstance(curLine, Printnl):
        print curLine.nodes[0]
        self.convertLine(curLine.nodes[0], 0)
        self.output += ("pushl %eax\ncall print_int_nl\n")

  def convertLine(self,curLine,pos):
    if isinstance(curLine,Add):
      self.convertLine(curLine.left, 0)
      if (isinstance(curLine.right, Const)):
        self.output += ("addl $%d, %%eax\n" % curLine.right.value)
      else:
        self.output += ("addl -%d(%%ebp), %%eax\n" % self.varLookup[curLine.right])
      print "Add"
    elif isinstance(curLine,Const):
      print "const"
      # self.output+=("movl $%d,-%d(%%ebp)\n"% (curLine.value,pos) )
      self.output += ("movl $%d, %%eax\n" % curLine.value)
    elif isinstance(curLine,Name):
      print curLine.name
      print self.varLookup
      self.output += ("movl -%d(%%ebp), %%eax\n" % self.varLookup[curLine])
      print "Name"
    elif isinstance(curLine,UnarySub):
      self.convertLine(curLine.expr, 0)
      self.output += ("negl %eax\n")
      print "Sub"
    elif isinstance(curLine,CallFunc):
      print "Input"
      self.output += ("call input\n")

  def endStack(self):
    self.output+=("movl $0,%eax\n")
    self.output+=("leave\n")
    self.output+=("ret\n")


if __name__ == "__main__":
  fout = open('test.s', 'w+')
  # inStr = "y=6\nx=-input()\nprint x + input()"
  inStr = "print 1"
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
  print to86.output
  fout.write(to86.output)
