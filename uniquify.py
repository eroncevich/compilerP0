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
        ast.node= Stmt([Function(None,'main body', [], [], 0, None, ast.node)])

    def getLocals(self,ast):
        if isinstance(ast,Module):
            return self.getLocals(ast.node)
        elif isinstance(ast,Function):
            varMap = {}
            localVars = Set([ast.name])
            for arg in ast.argnames:
                localVars.add(arg)
            localVars|=self.getLocals(ast.code)
            localId = self.unique_count
            self.unique_count+=1
            for local in localVars:
                varMap[local] = local + " a" + str(localId)

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


    def unique(self, ast, localVars={}):
        if isinstance(ast,Module):
            self.unique(ast.node,localVars)
        elif isinstance(ast,FuncLocals):
            for key in ast.local:
                localVars[key]= ast.local[key]
            self.unique(ast.func,localVars)
        elif isinstance(ast,Function):
            ast.name = localVars[ast.name]
            print ast.argnames
            ast.argnames = [localVars[arg] for arg in ast.argnames]
            print ast.argnames
            self.unique(ast.code, localVars)

        elif isinstance(ast,Stmt):
            for stmt in ast.nodes:
                self.unique(stmt,localVars)
        elif isinstance(ast,Printnl):
            self.unique(ast.nodes, localVars)
        elif isinstance(ast,Assign):
            print "AST"
        elif isinstance(ast,AssName):
            print "AST"
        elif isinstance(ast,Discard):
            print "AST"
        elif isinstance(ast,Const):
            print "AST"
        elif isinstance(ast,Name):
            print "AST"
        elif isinstance(ast,Add):
            print "AST"
        elif isinstance(ast,UnarySub):
            print "AST"
        elif isinstance(ast,CallFunc):
            print "AST"
        elif isinstance(ast,Compare):
            print "AST"
        elif isinstance(ast,Or):
            print "AST"
        elif isinstance(ast,And):
            print "AST"
        elif isinstance(ast,Not):
            print "AST"
        elif isinstance(ast,List):
            print "AST"
        elif isinstance(ast,Dict):
            print "AST"
        elif isinstance(ast,Subscript):
            print "AST"
        elif isinstance(ast,IfExp):
            print "AST"
        elif isinstance(ast,If):
            print "AST"
        elif isinstance(ast,Lambda):
            print "AST"
        else:
            print "Error Unique:",ast
