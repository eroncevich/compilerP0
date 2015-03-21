import uniquify
from uniquify import *

class Heapify:
    def __init__(self, ast):
        self.tmp = 0
        self.ast = ast
        self.varMap = {}
        self.unique_count = 0

    def heapAlloc(self,ast,curLocals = Set()):
        if isinstance(ast,Module):
            return Module(None,self.heapAlloc(ast.node, curLocals))
        elif isinstance(ast,FuncLocals):
            #print ast.local,ast.free
            for arg in ast.free:
                if arg in curLocals:
                    ast.func.code.nodes.insert(0, Assign([AssName(arg, 'OP_ASSIGN')], List([Name(arg)])))
                
            localVars = Set()
            for arg in ast.local.values():
                localVars |= Set([arg])
            return FuncLocals(ast.local,ast.free,self.heapAlloc(ast.func,localVars))
        elif isinstance(ast,Stmt):
            return Stmt([self.heapAlloc(stmt,curLocals) for stmt in ast.nodes])
        elif isinstance(ast,Printnl):
            return Printnl([self.heapAlloc(ast.nodes[0],curLocals)],ast.dest)
        elif isinstance(ast,Assign):
            return Assign([self.heapAlloc(ast.nodes[0],curLocals)], self.heapAlloc(ast.expr,curLocals))
        elif isinstance(ast,AssName):
            return ast
        elif isinstance(ast,Discard):
            return Discard(self.heapAlloc(ast.expr,curLocals))
        elif isinstance(ast,Const):
            return ast
        elif isinstance(ast,Name):
            if ast.name not in curLocals:
                return Subscript(ast, 'OP_APPLY', [Const(0)])
            return ast
        elif isinstance(ast,Add):
            return Add((self.heapAlloc(ast.left,curLocals),self.heapAlloc(ast.right,curLocals)))
        elif isinstance(ast,UnarySub):
            return UnarySub(self.heapAlloc(ast.expr,curLocals))
        elif isinstance(ast,CallFunc):
            return ast
        elif isinstance(ast,Compare):
            return Compare(self.heapAlloc(ast.expr,curLocals), [(ast.ops[0][0], self.heapAlloc(ast.ops[0][1],curLocals))])
        elif isinstance(ast,Or):
            return Or([self.heapAlloc(ast.nodes[0],curLocals),self.heapAlloc(ast.nodes[1],curLocals)])
        elif isinstance(ast,And):
            return And([self.heapAlloc(ast.nodes[0],curLocals),self.heapAlloc(ast.nodes[1],curLocals)])
        elif isinstance(ast,Not):
            return Not(self.heapAlloc(ast.expr,curLocals))
        elif isinstance(ast,List):
            return List([self.heapAlloc(e,curLocals) for e in ast.nodes])
        elif isinstance(ast,Dict):
            return Dict([(self.heapAlloc(e,curLocals), self.heapAlloc(l,curLocals)) for e,l in ast.items])
        elif isinstance(ast,Subscript):
            return Subscript(self.heapAlloc(ast.expr,curLocals), ast.flags, [self.heapAlloc(ast.subs[0],curLocals)])
        elif isinstance(ast,IfExp):
            return IfExp(self.heapAlloc(ast.test,curLocals), self.heapAlloc(ast.then,curLocals), self.heapAlloc(ast.else_,curLocals))
        elif isinstance(ast,If):
            return If([(self.heapAlloc(ast.tests[0][0],curLocals), self.heapAlloc(ast.tests[0][1],curLocals))], self.heapAlloc(ast.else_,curLocals))
        elif isinstance(ast,Lambda):
            return Lambda(ast.argnames,[], 0, self.heapAlloc(ast.code,curLocals))
        elif isinstance(ast,Return):
            return Return(self.heapAlloc(ast.value,curLocals))
        else:
            print "Error heapify:",ast


    def closure(self,ast,curLocals = Set()):
        if isinstance(ast,Module):
            return Module(None,self.heapAlloc(ast.node, curLocals))
        elif isinstance(ast,FuncLocals):
            #print ast.local,ast.free
            for arg in ast.free:
                if arg in curLocals:
                    ast.func.code.nodes.insert(0, Assign([AssName(arg, 'OP_ASSIGN')], List([Name(arg)])))
                
            localVars = Set()
            for arg in ast.local.values():
                localVars |= Set([arg])
            return FuncLocals(ast.local,ast.free,self.heapAlloc(ast.func,localVars))
        elif isinstance(ast,Stmt):
            return Stmt([self.heapAlloc(stmt,curLocals) for stmt in ast.nodes])
        elif isinstance(ast,Printnl):
            return Printnl([self.heapAlloc(ast.nodes[0],curLocals)],ast.dest)
        elif isinstance(ast,Assign):
            return Assign([self.heapAlloc(ast.nodes[0],curLocals)], self.heapAlloc(ast.expr,curLocals))
        elif isinstance(ast,AssName):
            return ast
        elif isinstance(ast,Discard):
            return Discard(self.heapAlloc(ast.expr,curLocals))
        elif isinstance(ast,Const):
            return ast
        elif isinstance(ast,Name):
            if ast.name not in curLocals:
                return Subscript(ast, 'OP_APPLY', [Const(0)])
            return ast
        elif isinstance(ast,Add):
            return Add((self.heapAlloc(ast.left,curLocals),self.heapAlloc(ast.right,curLocals)))
        elif isinstance(ast,UnarySub):
            return UnarySub(self.heapAlloc(ast.expr,curLocals))
        elif isinstance(ast,CallFunc):
            return ast
        elif isinstance(ast,Compare):
            return Compare(self.heapAlloc(ast.expr,curLocals), [(ast.ops[0][0], self.heapAlloc(ast.ops[0][1],curLocals))])
        elif isinstance(ast,Or):
            return Or([self.heapAlloc(ast.nodes[0],curLocals),self.heapAlloc(ast.nodes[1],curLocals)])
        elif isinstance(ast,And):
            return And([self.heapAlloc(ast.nodes[0],curLocals),self.heapAlloc(ast.nodes[1],curLocals)])
        elif isinstance(ast,Not):
            return Not(self.heapAlloc(ast.expr,curLocals))
        elif isinstance(ast,List):
            return List([self.heapAlloc(e,curLocals) for e in ast.nodes])
        elif isinstance(ast,Dict):
            return Dict([(self.heapAlloc(e,curLocals), self.heapAlloc(l,curLocals)) for e,l in ast.items])
        elif isinstance(ast,Subscript):
            return Subscript(self.heapAlloc(ast.expr,curLocals), ast.flags, [self.heapAlloc(ast.subs[0],curLocals)])
        elif isinstance(ast,IfExp):
            return IfExp(self.heapAlloc(ast.test,curLocals), self.heapAlloc(ast.then,curLocals), self.heapAlloc(ast.else_,curLocals))
        elif isinstance(ast,If):
            return If([(self.heapAlloc(ast.tests[0][0],curLocals), self.heapAlloc(ast.tests[0][1],curLocals))], self.heapAlloc(ast.else_,curLocals))
        elif isinstance(ast,Lambda):
            return Lambda(ast.argnames,[], 0, self.heapAlloc(ast.code,curLocals))
        elif isinstance(ast,Return):
            return Return(self.heapAlloc(ast.value,curLocals))
        else:
            print "Error heapify:",ast