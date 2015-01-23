import compiler
import sys
from compiler.ast import *


class flatParser:
  def __init__(self, ast):
    self.tmp = 0
    self.ast = ast
    self.flat = []

  def flatAst(self, ast):
    if isinstance(ast,Module):
      #print "Module"
      # return Module(None, flatAst(ast.node))
      self.flatAst(ast.node)
    elif isinstance(ast,Stmt):
      for stmt in ast.nodes:
        self.flatAst(stmt)
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

  def convert86(self):
    for curLine in self.flatAst:
      if isinstance(curLine, Assign):
        self.convertLine(curLine.expr, curLine.nodes.name)
      elif isinstance(curLine, Printnl):
        #self.output += self.getConstOrNamePrint(curLine.nodes[0])
        self.output += ("\tmovl %s, %%eax\n" % self.getConstOrName(curLine.nodes[0]))
        self.output += ("\tpushl %eax\n\tcall print_int_nl\n\tpopl %eax\n")

  def convertLine(self,curLine,tmpName):
    if isinstance(curLine,Add):
      self.output += ("\tmovl %s, %%eax\n" % self.getConstOrName(curLine.left))
      self.output += ("\taddl %s, %%eax\n" % self.getConstOrName(curLine.right))
      self.output += ("\tmovl %%eax, -%d(%%ebp)\n" % self.getAddr(tmpName))
    elif isinstance(curLine,Const):
      self.output+=("\tmovl $%d,-%d(%%ebp)\n"% (curLine.value,self.getAddr(tmpName)) )
    elif isinstance(curLine,Name):
      self.output+=("\tmovl -%d(%%ebp),%%eax\n"% self.getAddr(curLine.name))
      self.output+=("\tmovl %%eax,-%d(%%ebp)\n"%self.getAddr(tmpName))
    elif isinstance(curLine,UnarySub):
      self.output += self.getConstOrNameSub(curLine.expr, tmpName)
    elif isinstance(curLine,CallFunc):
      self.output += ("\tcall input\n")
      self.output += ("\tmovl %%eax, -%d(%%ebp)\n" % self.getAddr(tmpName))

  def getConstOrName(self, line):
    if isinstance(line, Name):
      return "-%d(%%ebp)" % self.getAddr(line.name)
    else:
      return "$%d" % line.value

  def getConstOrNameSub(self, line, tmpName):
    if isinstance(line, Name):
      return "\tmovl -%d(%%ebp), %%eax\n\tnegl %%eax\n\tmovl %%eax, -%d(%%ebp)\n" % (self.getAddr(line.name), self.getAddr(tmpName))
    else:
      return "\tmovl $-%d, -%d(%%ebp)\n" % (line.value, self.getAddr(tmpName))

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
  #print ast

  parser.flatAst(parser.ast)
  #parser.printFlat()
  to86 = pyTo86(parser.flat,parser.tmp)
  to86.startStack()
  to86.convert86()
  to86.endStack()
  #print "\n"
  #print to86.output
  outFileName = sys.argv[1].replace('.py','.s')
  fout = open(outFileName, 'w+')
  fout.write(to86.output)
