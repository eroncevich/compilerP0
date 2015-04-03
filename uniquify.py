import compiler
from compiler.ast import *
from sets import Set

class FuncLocals:
    def __init__(self, local,free, func, name):
        self.local = local
        self.free = free
        self.func = func
        self.name = name
    def __repr__(self):
        return "FuncLocals(\'%s\',\'%s\',%s, %s)" % (repr(self.local),repr(self.free),repr(self.func), self.name)

class Uniquify:
    def __init__(self, ast):
        self.tmp = 0
        self.ast = ast
        self.varMap = {}
        self.unique_count = 0
        ast.node= Stmt([Function(None,'main body', [], [], 0, None, ast.node)])
        self.trueSet =1

    def replaceFunc(self,ast):
        if isinstance(ast,Module):
            return Module(None,self.replaceFunc(ast.node))
        elif isinstance(ast,Function):
            #return FuncLocals({},Set(), Assign([AssName(ast.name, 'OP_ASSIGN')],Lambda(ast.argnames,[], 0, self.replaceFunc(ast.code))))
            #print ast.name
            return Assign([AssName(ast.name, 'OP_ASSIGN')], FuncLocals({},Set(),Lambda(ast.argnames,[], 0, self.replaceFunc(ast.code)), ast.name))
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
            return Add((self.replaceFunc(ast.left),self.replaceFunc(ast.right)))
        elif isinstance(ast,UnarySub):
            return UnarySub(self.replaceFunc(ast.expr))
        elif isinstance(ast,CallFunc):
            #return ast
            return CallFunc(self.replaceFunc(ast.node),[self.replaceFunc(arg) for arg in ast.args], None,None)
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
            return Dict([(self.replaceFunc(e), self.replaceFunc(l)) for e,l in ast.items])
        elif isinstance(ast,Subscript):
            return Subscript(self.replaceFunc(ast.expr), ast.flags, [self.replaceFunc(ast.subs[0])])
        elif isinstance(ast,IfExp):
            return IfExp(self.replaceFunc(ast.test), self.replaceFunc(ast.then), self.replaceFunc(ast.else_))
        elif isinstance(ast,If):
            return If([(self.replaceFunc(ast.tests[0][0]), self.replaceFunc(ast.tests[0][1]))], self.replaceFunc(ast.else_))
        elif isinstance(ast,Lambda):
            return FuncLocals({},Set(),Lambda(ast.argnames,[], 0, Stmt([Return(self.replaceFunc(ast.code))])),"empty")
        elif isinstance(ast,Return):
            return Return(self.replaceFunc(ast.value))
        else:
            print "Error toFunc:",ast


    def getLocals(self,ast):
        if isinstance(ast,Module):
            return self.getLocals(ast.node)
        elif isinstance(ast,FuncLocals):
            varMap = {}
            localId = self.unique_count
            self.unique_count+=1
            localVars = Set()
            if isinstance(ast.func,Lambda) and self.trueSet: #We assume True and False set at beginning
                localVars|=Set(['True'])
                localVars|=Set(['False'])
                self.trueSet =0

            localVars |= self.getLocals(ast.func)
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
                #print stmt
                localVars|=self.getLocals(stmt)
            return localVars
        elif isinstance(ast,Printnl):
            return self.getLocals(ast.nodes[0])
            #return Set()
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
            print "pres"
            localVars = Set()
            localVars|= self.getLocals(ast.node)
            for arg in ast.args:
                localVars|= self.getLocals(arg)
            return localVars
            #return Set()
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


    def unique(self, ast, localVars={}, curLocals={}):
        if isinstance(ast,Module):
            self.unique(ast.node,localVars, curLocals)
        elif isinstance(ast,FuncLocals):
            localVars = localVars.copy()
            for key in ast.local:
                localVars[key]= ast.local[key]

            oldLocals = curLocals
            curLocals = ast.local

            freeVars = self.unique(ast.func,localVars, curLocals)
            ast.free = freeVars
            newVars = Set()
            for var in freeVars:
                if var not in oldLocals.values():
                    newVars |= Set([var])
            return newVars

        elif isinstance(ast,Function):
            print "You shouldn't have done that"

        elif isinstance(ast,Stmt):
            freeVars = Set()
            for stmt in ast.nodes:
                freeVars|= self.unique(stmt,localVars, curLocals)
                #freeVars
            return freeVars
        elif isinstance(ast,Printnl):
            return self.unique(ast.nodes[0], localVars, curLocals)
        elif isinstance(ast,Assign):
            if isinstance(ast.expr, FuncLocals) and ast.expr.name != "empty":
                #print "hi"
                if ast.nodes[0].name == "main body":
                    ast.expr.name = "main body"
                else:
                    ast.expr.name = localVars[ast.nodes[0].name]

            self.unique(ast.nodes[0], localVars, curLocals)
            freeVars = self.unique(ast.expr, localVars, curLocals)
            return freeVars
        elif isinstance(ast,AssName):
            #shouln't need to return here
            if ast.name == 'main body':
                return
            ast.name = localVars[ast.name]
        elif isinstance(ast,Discard):
            return self.unique(ast.expr, localVars, curLocals)
        elif isinstance(ast,Const):
            return Set()
        elif isinstance(ast,Name):
            #if(ast)

            tmp = ast.name
            ast.name = localVars[ast.name]
            if not curLocals.has_key(tmp):
                return Set([ast.name])
            else:
                return Set()
        elif isinstance(ast,Add):

            freeVars =self.unique(ast.left, localVars, curLocals) | self.unique(ast.right, localVars, curLocals)
            return freeVars
        elif isinstance(ast,UnarySub):
            return self.unique(ast.expr, localVars, curLocals)
        elif isinstance(ast,CallFunc):
            if isinstance(ast.node, Name):
                if ast.node.name == 'input' and len(ast.args)==0:
                    return Set()
            freeVars = self.unique(ast.node, localVars, curLocals)
            for arg in ast.args:
                freeVars |= self.unique(arg, localVars, curLocals)
            return freeVars
        elif isinstance(ast,Compare):
            return self.unique(ast.expr, localVars, curLocals)| self.unique(ast.ops[0][1], localVars, curLocals)
        elif isinstance(ast,Or):
            freeVars = Set()
            for arg in ast.nodes:
                freeVars |= self.unique(arg, localVars, curLocals)
            return freeVars
        elif isinstance(ast,And):
            freeVars = Set()
            for arg in ast.nodes:
                freeVars |= self.unique(arg, localVars, curLocals)
            return freeVars
        elif isinstance(ast,Not):
            return self.unique(ast.expr, localVars, curLocals)
        elif isinstance(ast,List):
            freeVars = Set()
            for arg in ast.nodes:
                freeVars |= self.unique(arg, localVars, curLocals)
            return freeVars
        elif isinstance(ast,Dict):
            freeVars = Set()
            for e,l in ast.items:
                freeVars |=self.unique(e, localVars, curLocals)
                freeVars |=self.unique(l, localVars, curLocals)
            return freeVars
        elif isinstance(ast,Subscript):
            return self.unique(ast.expr, localVars, curLocals) | self.unique(ast.subs[0], localVars, curLocals)
        elif isinstance(ast,IfExp):
            return self.unique(ast.test, localVars, curLocals) | self.unique(ast.then, localVars, curLocals) |self.unique(ast.else_, localVars, curLocals)
        elif isinstance(ast,If):
            return self.unique(ast.tests[0][0], localVars, curLocals) | self.unique(ast.tests[0][1], localVars, curLocals)
        elif isinstance(ast,Lambda):
            ast.argnames = [localVars[arg] for arg in ast.argnames]
            freeVars = self.unique(ast.code, localVars, curLocals)
            return freeVars
        elif isinstance(ast,Return):
            freeVars= self.unique(ast.value, localVars,curLocals)
            return freeVars
        else:
            print "Error Unique:",ast
