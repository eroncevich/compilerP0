from sets import Set
from x86AST import *
ig = InterferenceGraph()
ops = [BinaryOp("movl", ConstOp(4), NameOp("z")), BinaryOp("movl", ConstOp(0), NameOp("w")), BinaryOp("movl", ConstOp(1), NameOp("z")), BinaryOp("movl", NameOp("w"), NameOp("x")), BinaryOp("addl", NameOp("z"), NameOp("x")), BinaryOp("movl", NameOp("w"), NameOp("y")), BinaryOp("addl", NameOp("x"), NameOp("y")), BinaryOp("movl", NameOp("y"), NameOp("w")), BinaryOp("addl", NameOp("x"), NameOp("w"))]
ig.createLiveness(ops)
ig.createInterferenceGraph(ops);
