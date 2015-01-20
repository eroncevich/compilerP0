import compiler
from compiler.ast import *

fout = open('test.s', 'w+')

ast = compiler.parse("print -input() +2")
print ast

def flatAst(ast):
  if isinstance(ast,Module):
    print "Module"
    flatAst(ast.node)
  elif isinstance(ast,Stmt):
    for stmt in ast.nodes:
      print "****Stmt Start****"
      flatAst(stmt)
      print "****Stmt End****"
  elif isinstance(ast,Printnl):
    print "Print"
    flatAst(ast.nodes[0])
  elif isinstance(ast,Assign):
    print "Assign"
    flatAst(ast.nodes[0])
    flatAst(ast.expr)
  elif isinstance(ast,AssName):
    print ast
  elif isinstance(ast,Discard):
    print "Discard"
  elif isinstance(ast,Const):
    print "Const:", ast.value
  elif isinstance(ast,Name):
    print "Name"
  elif isinstance(ast,Add):
    print "Add"
    flatAst(ast.left)
    flatAst(ast.right)
  elif isinstance(ast,UnarySub):
    print "Neg"
    flatAst(ast.expr)
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


flatAst(ast)
#setStack(4)
