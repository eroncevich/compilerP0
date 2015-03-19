import compiler
from compiler.ast import *
from sets import Set

class FuncLocals:
    def __init__(self, local, func):
        self.local = local
        self.func = func
    def __repr__(self):
        return "FuncLocals(\'%s\',%s)" % (repr(self.local),repr(self.func))

class Uniquify:
    def __init__(self, ast):
        self.tmp = 0
        self.ast = ast
        self.varMap = {}

    def getLocals(self,ast):
        if isinstance(ast,Module):
            return self.getLocals(ast.node)
        elif isinstance(ast,Function):
            localVars = Set(ast.name)
            for arg in ast.argnames:
                localVars.add(arg)
            localVars|=self.getLocals(ast.code)
            ast.local = localVars
            ast = FuncLocals(localVars,ast)
            return Set()
        elif isinstance(ast,Stmt):
            localVars = Set()
            for stmt in ast.nodes:
                localVars|=self.getLocals(stmt) 
            return localVars
        elif isinstance(ast,Printnl):
            return Set()
        elif isinstance(ast,Assign):
            return self.getLocals(ast.nodes[0])
        elif isinstance(ast,AssName):
            return Set(ast.name)
        elif isinstance(ast,Discard):
            return self.getLocals(ast.expr)
        elif isinstance(ast,Const):
            return Set()
        elif isinstance(ast,Name):
            return Set()
        elif isinstance(ast,Add):
            leftVars = self.getLocals(ast.left)
            rightVars = self.getLocals(ast.right)
            return lefVars | rightVars
        elif isinstance(ast,UnarySub):
            return self.getLocals(ast.expr)
        elif isinstance(ast,CallFunc):
            return Set()
        elif isinstance(ast,Compare):
            print "AST"
            pass
        elif isinstance(ast,Or):
            print "AST"
            pass
        elif isinstance(ast,And):
            print "AST"
            pass
        elif isinstance(ast,Not):
            print "AST"
            pass
        elif isinstance(ast,List):
            print "AST"
            pass
        elif isinstance(ast,Dict):
            print "AST"
            pass
        elif isinstance(ast,Subscript):
            print "AST"
            pass
        elif isinstance(ast,IfExp):
            print "AST"
            pass
        elif isinstance(ast,If):
            print "AST"
            pass
        elif isinstance(ast,Lambda):
            pass
        else:
            print "Error:",ast