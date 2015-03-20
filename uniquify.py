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

    def replaceFunc(self,ast):
        if isinstance(ast,Module):
            return Module(None,self.replaceFunc(ast.node))
        elif isinstance(ast,Function):
            #return FuncLocals({}, Function(None,ast.name,ast.argnames,ast.defaults,ast.flags,ast.doc,self.replaceFunc(ast.code)))
            return FuncLocals({}, Assign([AssName(ast.name, 'OP_ASSIGN')],Lambda(ast.argnames,[], 0, self.replaceFunc(ast.code))))
            #return Function(None,ast.name,ast.argnames,ast.defaults,ast.flags,ast.doc,self.replaceFunc(ast.code))
        elif isinstance(ast,Stmt):
            return Stmt([self.replaceFunc(stmt) for stmt in ast.nodes])
        elif isinstance(ast,Printnl):
            return Printnl([self.replaceFunc(ast.nodes[0])],ast.dest)
        elif isinstance(ast,Assign):
            return Assign([self.replaceFunc(ast.nodes[0])], self.replaceFunc(ast.expr))
        elif isinstance(ast,AssName):
            return ast
        elif isinstance(ast,Discard):
            return Discard(self.replaceFunc(ast.expr))
        elif isinstance(ast,Const):
            return ast
        elif isinstance(ast,Name):
            return ast
        elif isinstance(ast,Add):
            return Add(ast.left,ast.right)
        elif isinstance(ast,UnarySub):
            return UnarySub(ast.expr)
        elif isinstance(ast,CallFunc):
            return ast
        elif isinstance(ast,Compare):
            return Compare(self.replaceFunc(ast.expr), [(ast.ops[0][0], self.replaceFunc(ast.ops[0][1]))])
        elif isinstance(ast,Or):
            return Or([self.replaceFunc(ast.nodes[0]),self.replaceFunc(ast.nodes[1])])
        elif isinstance(ast,And):
            return And([self.replaceFunc(ast.nodes[0]),self.replaceFunc(ast.nodes[1])])
        elif isinstance(ast,Not):
            return Not(self.replaceFunc(ast.expr))
        elif isinstance(ast,List):
            return List([self.replaceFunc(e) for e in ast.nodes])
        elif isinstance(ast,Dict):
            Dict([(self.replaceFunc(e), self.replaceFunc(l)) for e,l in ast.items])
        elif isinstance(ast,Subscript):
            return Subscript(self.replaceFunc(ast.expr), ast.flags, [self.replaceFunc(ast.subs[0])])
        elif isinstance(ast,IfExp):
            IfExp(self.replaceFunc(ast.test), self.replaceFunc(ast.then), self.replaceFunc(ast.else_))
        elif isinstance(ast,If):
            return If([(self.replaceFunc(ast.tests[0][0]), self.replaceFunc(ast.tests[0][1]))], self.replaceFunc(ast.else_))
        elif isinstance(ast,Lambda):
            #return Lambda(ast.argnames,[], 0, self.replaceFunc(ast.code))
            return FuncLocals({},Lambda(ast.argnames,[], 0, Stmt([Return(self.replaceFunc(ast.code))])))
            #return ast
        else:
            print "Error toFunc:",ast


    def getLocals(self,ast):
        if isinstance(ast,Module):
            return self.getLocals(ast.node)
        elif isinstance(ast,FuncLocals):
            varMap = {}
            localVars = self.getLocals(ast.func)
            localId = self.unique_count
            self.unique_count+=1
            for local in localVars:
                varMap[local] = local + " a" + str(localId)

            ast.local = varMap
            return Set()
        elif isinstance(ast,Function):
            localVars = Set([ast.name])
            for arg in ast.argnames:
                localVars.add(arg)
            localVars|=self.getLocals(ast.code)
            localId = self.unique_count
            return localVars

        elif isinstance(ast,Stmt):
            localVars = Set()
            for stmt in ast.nodes:
                print stmt
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
            return localVars
        elif isinstance(ast,Return):
            return self.getLocals(ast.value)
        else:
            print "Error locals:",ast


    def unique(self, ast, localVars={}):
        if isinstance(ast,Module):
            self.unique(ast.node,localVars)
        elif isinstance(ast,FuncLocals):
            for key in ast.local:
                localVars[key]= ast.local[key]
            self.unique(ast.func,localVars)
            #ast.func = child

        elif isinstance(ast,Function):
            ast.name = localVars[ast.name]
            ast.argnames = [localVars[arg] for arg in ast.argnames]
            self.unique(ast.code, localVars)
            #ast = Lambda(ast.argnames,[], 0, ast.code)
            #return ast
            #return Assign([self.explicate(ast.nodes[0])], self.explicate(ast.expr))

        elif isinstance(ast,Stmt):
            for stmt in ast.nodes:
                self.unique(stmt,localVars)
        elif isinstance(ast,Printnl):
            self.unique(ast.nodes, localVars)
        elif isinstance(ast,Assign):
            self.unique(ast.nodes[0], localVars)
            self.unique(ast.expr, localVars)
        elif isinstance(ast,AssName):
            ast.name = localVars[ast.name]
        elif isinstance(ast,Discard):
            self.unique(ast.expr, localVars)
        elif isinstance(ast,Const):
            pass
        elif isinstance(ast,Name):
            ast.name = localVars[ast.name]
        elif isinstance(ast,Add):
            self.unique(ast.left, localVars)
            self.unique(ast.right, localVars)
        elif isinstance(ast,UnarySub):
            self.unique(ast.expr, localVars)
        elif isinstance(ast,CallFunc):
            self.unique(ast.node, localVars)
            for arg in ast.args:
                self.unique(arg, localVars)
        elif isinstance(ast,Compare):
            self.unique(ast.expr, localVars)
            self.unique(ast.ops[0][1], localVars)
        elif isinstance(ast,Or):
            for arg in ast.nodes:
                self.unique(arg, localVars)
        elif isinstance(ast,And):
            for arg in ast.nodes:
                self.unique(arg, localVars)
        elif isinstance(ast,Not):
            self.unique(ast.expr, localVars)
        elif isinstance(ast,List):
            for arg in ast.nodes:
                self.unique(arg, localVars)
        elif isinstance(ast,Dict):
            for e,l in ast.items:
                self.unique(e, localVars)
                self.unique(l, localVars)
        elif isinstance(ast,Subscript):
            self.unique(ast.expr, localVars)
            self.unique(ast.subs[0], localVars)
        elif isinstance(ast,IfExp):
            self.unique(ast.test, localVars)
            self.unique(ast.then, localVars)
            self.unique(ast.else_, localVars)
        elif isinstance(ast,If):
            self.unique(ast.tests[0][0], localVars)
            self.unique(ast.tests[0][1], localVars)
        elif isinstance(ast,Lambda):
            ast.argnames = [localVars[arg] for arg in ast.argnames]
            self.unique(ast.code, localVars)
            #ast = Lambda(ast.argnames,[], 0, Stmt([Return(ast.code)]))
            #return ast
        elif isinstance(ast,Return):
            self.unique(ast.value)
        else:
            print "Error Unique:",ast
