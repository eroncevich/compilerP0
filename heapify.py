import uniquify
from uniquify import *
class ClosureConversion:
    def __init__(self, globalName,fvs):
        self.globalName = globalName
        self.fvs = fvs
    def __repr__(self):
        return "ClosureConversion(\'%s\',%s)" % (repr(self.globalName),repr(self.fvs))
class CallPointer:
    def __init__(self, node,args):
        self.node = node
        self.args = args
    def __repr__(self):
        return "CallPointer(%s,%s)" % (repr(self.node),repr(self.args))


class Heapify:
    def __init__(self, ast):
        self.tmp = 0
        self.ast = ast
        self.varMap = {}
        self.unique_count = 0
        self.lambdaNum =0
        self.freeVars={}

    def heapAlloc(self,ast,curLocals = Set()):
        if isinstance(ast,Module):
            self.ast = Module(None,self.heapAlloc(ast.node, curLocals))
            return ast
        elif isinstance(ast,FuncLocals):
            #print ast.local,ast.free
            for arg in ast.free:
                if arg in curLocals:
                    ast.func.code.nodes.insert(0, Assign([AssName(arg, 'OP_ASSIGN')], List([Name(arg)])))
                
            localVars = Set()
            for arg in ast.local.values():
                localVars |= Set([arg])
            return FuncLocals(ast.local,ast.free,self.heapAlloc(ast.func,localVars), ast.name)
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
            Module(None,self.closure(ast.node, curLocals))
            self.ast.node.nodes.pop()
            return Module(None,self.ast.node)
        elif isinstance(ast,FuncLocals):
            if ast.name == "empty":
                ast.name = self.getLambdaName()

            for index, arg in enumerate(sorted(ast.free)):
                ast.func.code.nodes.insert(0,Assign([AssName(arg,'OP_ASSIGN')],Subscript(Name('fvs'),'OP_APPLY', [Const(index)])))
            ast.func.argnames.insert(0,'fvs')
            self.freeVars[ast.name] = ast.free
            self.ast.node.nodes.insert(0,FuncLocals(ast.local,ast.free,self.closure(ast.func,curLocals),ast.name))
            #return ClosureConversion(ast.name, ast.free)
            return CallFunc(Name("create_closure"), [ast.name, List([Name(arg) for arg in sorted(ast.free)])], None, None)
        elif isinstance(ast,Stmt):
            return Stmt([self.closure(stmt,curLocals) for stmt in ast.nodes])
        elif isinstance(ast,Printnl):
            return Printnl([self.closure(ast.nodes[0],curLocals)],ast.dest)
        elif isinstance(ast,Assign):
            return Assign([self.closure(ast.nodes[0],curLocals)], self.closure(ast.expr,curLocals))
        elif isinstance(ast,AssName):
            return ast
        elif isinstance(ast,Discard):
            return Discard(self.closure(ast.expr,curLocals))
        elif isinstance(ast,Const):
            return ast
        elif isinstance(ast,Name):
            if ast.name not in curLocals:
                return Subscript(ast, 'OP_APPLY', [Const(0)])
            return ast
        elif isinstance(ast,Add):
            return Add((self.closure(ast.left,curLocals),self.closure(ast.right,curLocals)))
        elif isinstance(ast,UnarySub):
            return UnarySub(self.closure(ast.expr,curLocals))
        elif isinstance(ast,CallFunc):
            if ast.node == "input":
                return ast
            return CallPointer(CallFunc(Name('get_fun_ptr'), ast.node, None,None),[CallFunc(Name("get_free_vars"), ast.node)]+ast.args)
        elif isinstance(ast,Compare):
            return Compare(self.closure(ast.expr,curLocals), [(ast.ops[0][0], self.closure(ast.ops[0][1],curLocals))])
        elif isinstance(ast,Or):
            return Or([self.closure(ast.nodes[0],curLocals),self.closure(ast.nodes[1],curLocals)])
        elif isinstance(ast,And):
            return And([self.closure(ast.nodes[0],curLocals),self.closure(ast.nodes[1],curLocals)])
        elif isinstance(ast,Not):
            return Not(self.closure(ast.expr,curLocals))
        elif isinstance(ast,List):
            return List([self.closure(e,curLocals) for e in ast.nodes])
        elif isinstance(ast,Dict):
            return Dict([(self.closure(e,curLocals), self.closure(l,curLocals)) for e,l in ast.items])
        elif isinstance(ast,Subscript):
            return Subscript(self.closure(ast.expr,curLocals), ast.flags, [self.closure(ast.subs[0],curLocals)])
        elif isinstance(ast,IfExp):
            return IfExp(self.closure(ast.test,curLocals), self.closure(ast.then,curLocals), self.closure(ast.else_,curLocals))
        elif isinstance(ast,If):
            return If([(self.closure(ast.tests[0][0],curLocals), self.closure(ast.tests[0][1],curLocals))], self.closure(ast.else_,curLocals))
        elif isinstance(ast,Lambda):
            return Lambda(ast.argnames,[], 0, self.closure(ast.code,curLocals))
        elif isinstance(ast,Return):
            return Return(self.closure(ast.value,curLocals))
        else:
            print "Error heapify:",ast

    def getLambdaName(self):
        return "lambda %i" % self.lambdaNum