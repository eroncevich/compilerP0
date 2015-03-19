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
        self.unique_count = 0

    def getLocals(self,ast):
        if isinstance(ast,Module):
            return self.getLocals(ast.node)
        elif isinstance(ast,Function):
            varMap = {}
            localVars = Set([ast.name])
            for arg in ast.argnames:
                localVars.add(arg)
            localVars|=self.getLocals(ast.code)
            for local in localVars:
                varMap[local] = local + " a" + str(self.unique_count)
                self.unique_count += 1

            ast = FuncLocals(varMap, ast)
            print varMap
            return ast
        elif isinstance(ast,Stmt):
            localVars = Set()
            for index, stmt in enumerate(ast.nodes):
                if isinstance(stmt, Function):
                    ast.nodes[index] = self.getLocals(stmt)
                else:
                    localVars|=self.getLocals(stmt)
            return localVars
        elif isinstance(ast,Printnl):
            return Set()
        elif isinstance(ast,Assign):
            return self.getLocals(ast.nodes[0]) |self.getLocals(ast.expr)
        elif isinstance(ast,AssName):
            return Set([ast.name])
        elif isinstance(ast,Discard):
            return self.getLocals(ast.expr)
        elif isinstance(ast,Const):
            return Set()
        elif isinstance(ast,Name):
            return Set()
        elif isinstance(ast,Add):
            leftVars = self.getLocals(ast.left)
            rightVars = self.getLocals(ast.right)
            return leftVars | rightVars
        elif isinstance(ast,UnarySub):
            return self.getLocals(ast.expr)
        elif isinstance(ast,CallFunc):
            return Set()
        elif isinstance(ast,Compare):
            return self.getLocals(ast.expr) | self.getLocals(ast.ops[0][1])
        elif isinstance(ast,Or):
            return self.getLocals(ast.nodes[0]) |self.getLocals(ast.nodes[1])
        elif isinstance(ast,And):
            return self.getLocals(ast.nodes[0]) |self.getLocals(ast.nodes[1])
        elif isinstance(ast,Not):
            return self.getLocals(ast.expr)
        elif isinstance(ast,List):
            localVars = Set()
            for e in ast.nodes:
                localVars|=self.getLocals(e)
            return Set()
        elif isinstance(ast,Dict):
            localVars = Set()
            for l,e in ast.items:
                localVars|=self.getLocals(e)
            return Set()
        elif isinstance(ast,Subscript):
            return Set()
        elif isinstance(ast,IfExp):
            return self.getLocals(ast.test)| self.getLocals(ast.then)| self.getLocals(ast.else_)
        elif isinstance(ast,If):
            return self.getLocals(ast.tests[0][0])| self.getLocals(ast.tests[0][1]) | self.getLocals(ast.else_)
        elif isinstance(ast,Lambda):
            localVars = Set()
            for arg in ast.argnames:
                localVars.add(arg)
            localVars|=self.getLocals(ast.code)
            ast = FuncLocals(localVars,ast)
            return Set()
        else:
            print "Error Unique:",ast


    def unique(self, ast, locals={}):
        if isinstance(ast,Module):
            return self.getLocals(ast.node)
        elif isinstance(ast,Function):
            varMap = {}
            localVars = Set([ast.name])
            for arg in ast.argnames:
                localVars.add(arg)
            localVars|=self.getLocals(ast.code)
            for local in localVars:
                varMap[local] = local + " a" + str(self.unique_count)
                self.unique_count += 1

            ast = FuncLocals(varMap, ast)
            print varMap
            return ast
        elif isinstance(ast,Stmt):
            localVars = Set()
            for index, stmt in enumerate(ast.nodes):
                if isinstance(stmt, Function):
                    ast.nodes[index] = self.getLocals(stmt)
                else:
                    localVars|=self.getLocals(stmt)
            return localVars
        elif isinstance(ast,Printnl):
            return Set()
        elif isinstance(ast,Assign):
            return self.getLocals(ast.nodes[0]) |self.getLocals(ast.expr)
        elif isinstance(ast,AssName):
            return Set([ast.name])
        elif isinstance(ast,Discard):
            return self.getLocals(ast.expr)
        elif isinstance(ast,Const):
            return Set()
        elif isinstance(ast,Name):
            return Set()
        elif isinstance(ast,Add):
            leftVars = self.getLocals(ast.left)
            rightVars = self.getLocals(ast.right)
            return leftVars | rightVars
        elif isinstance(ast,UnarySub):
            return self.getLocals(ast.expr)
        elif isinstance(ast,CallFunc):
            return Set()
        elif isinstance(ast,Compare):
            return self.getLocals(ast.expr) | self.getLocals(ast.ops[0][1])
        elif isinstance(ast,Or):
            return self.getLocals(ast.nodes[0]) |self.getLocals(ast.nodes[1])
        elif isinstance(ast,And):
            return self.getLocals(ast.nodes[0]) |self.getLocals(ast.nodes[1])
        elif isinstance(ast,Not):
            return self.getLocals(ast.expr)
        elif isinstance(ast,List):
            localVars = Set()
            for e in ast.nodes:
                localVars|=self.getLocals(e)
            return Set()
        elif isinstance(ast,Dict):
            localVars = Set()
            for l,e in ast.items:
                localVars|=self.getLocals(e)
            return Set()
        elif isinstance(ast,Subscript):
            return Set()
        elif isinstance(ast,IfExp):
            return self.getLocals(ast.test)| self.getLocals(ast.then)| self.getLocals(ast.else_)
        elif isinstance(ast,If):
            return self.getLocals(ast.tests[0][0])| self.getLocals(ast.tests[0][1]) | self.getLocals(ast.else_)
        elif isinstance(ast,Lambda):
            localVars = Set()
            for arg in ast.argnames:
                localVars.add(arg)
            localVars|=self.getLocals(ast.code)
            ast = FuncLocals(localVars,ast)
            return Set()
        else:
            print "Error Unique:",ast
