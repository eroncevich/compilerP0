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
      print "Print"
      self.flatAst(ast.nodes[0])
    elif isinstance(ast,Assign):
      print "Assign"
      self.flatAst(ast.nodes[0])
      self.flatAst(ast.expr)
    elif isinstance(ast,AssName):
      print ast
    elif isinstance(ast,Discard):
      print "Discard"
    elif isinstance(ast,Const):
      print "Const:", ast.value
      return ast
    elif isinstance(ast,Name):
      print "Name"
      return ast
    elif isinstance(ast,Add):
      print "Add"
      l = self.flatAst(ast.left)
      r = self.flatAst(ast.right)
      self.tmp += 1

    elif isinstance(ast,UnarySub):
      print "Neg"
      self.flatAst(ast.expr)
    elif isinstance(ast,CallFunc):
      print "CallFunc"
      print ast.node
      print ast.args
    else:
      print "Ended"

def setStack(size):
  fout.write(".globl main\n")
  fout.write("main:\n")
  fout.write("pushl %ebp\n")
  fout.write("movl %esp, %ebp\n")
  fout.write("subl $%d, %%ebp\n" % size)

if __name__ == "__main__":
  fout = open('test.s', 'w+')

  ast = compiler.parse("x=-5\nprint x+2+input()")
  parser = flatParser(ast)
  print ast

  parser.flatAst(parser.ast)
  #setStack(4)
