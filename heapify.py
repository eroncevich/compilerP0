import uniquify
from uniquify import *
import copy
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
        self.lambdaNum =-1
        self.freeVars={}
        self.needsHeaped = Set()

    def heapAlloc(self,ast,curLocals = Set()): #finds what variables need to be heaped
        if isinstance(ast,Module):
            ast = Module(None,self.heapAlloc(ast.node, curLocals))
            self.ast = copy.deepcopy(ast)
            return ast
        elif isinstance(ast,FuncLocals):
            #print ast.local,ast.free
            for arg in ast.free:
                if arg in curLocals:
                    #print arg, "eh", ast.name
                    self.needsHeaped|= Set([arg])
                
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
            # if ast.name not in curLocals:
                # print ast.name
                # return Subscript(ast, 'OP_APPLY', [Const(3)])
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
        elif isinstance(ast,While):
            return While(self.heapAlloc(ast.test,curLocals), self.heapAlloc(ast.body,curLocals), None)
        elif isinstance(ast,Lambda):
            return Lambda(ast.argnames,[], 0, self.heapAlloc(ast.code,curLocals))
        elif isinstance(ast,Return):
            return Return(self.heapAlloc(ast.value,curLocals))
        else:
            print "Error alloc:",ast


    def closure(self,ast,curLocals = Set()):
        if isinstance(ast,Module):
            #self.ast =ast.copy()
            Module(None,self.closure(ast.node, curLocals))
            self.ast.node.nodes.pop()
            return Module(None,self.ast.node)
        elif isinstance(ast,FuncLocals):
            if ast.name == "empty":
                ast.name = self.getLambdaName()

            if ast.name == "main body":
                ast.func.code.nodes.insert(0,Assign([AssName(ast.local['False'],'OP_ASSIGN')],Const(.25)))
                ast.func.code.nodes.insert(0,Assign([AssName(ast.local['True'],'OP_ASSIGN')],Const(1.25)))

            for arg in ast.local.values():
                if arg in self.needsHeaped: #and arg not in ast.free?                    
                    if arg in ast.func.argnames:
                        # ast.func.code.nodes.insert(1,Assign([AssName(arg, 'OP_ASSIGN')],Name(arg)))
                        ast.func.code.nodes.insert(0,Assign([AssName(arg,'OP_HEAP')],List([Name(arg)])))
                    else:
                        ast.func.code.nodes.insert(0,Assign([AssName(arg,'OP_HEAP')],List([Const(7777777)])))
                    #pass

            for index, arg in enumerate(sorted(ast.free)):
                ast.func.code.nodes.insert(0,Assign([AssName(arg,'OP_HEAP')],Subscript(Name('fvs'),'OP_APPLY', [Const(index)])))
            ast.func.argnames.insert(0,'fvs')
            self.freeVars[ast.name] = ast.free
            self.ast.node.nodes.insert(0,FuncLocals(ast.local,ast.free,self.closure(ast.func,ast.free),ast.name))
            

            #print "hey", ast
            return CallFunc(Name("create_closure"), [ast.name, List([Name(arg) for arg in sorted(ast.free)])], None, None)
        elif isinstance(ast,Stmt):
            return Stmt([self.closure(stmt,curLocals) for stmt in ast.nodes])
        elif isinstance(ast,Printnl):
            return Printnl([self.closure(ast.nodes[0],curLocals)],ast.dest)
        elif isinstance(ast,Assign):
            if isinstance(ast.nodes[0], AssName) and ast.nodes[0].flags == 'OP_HEAP':
                return Assign([self.closure(ast.nodes[0],curLocals)], ast.expr)
            return Assign([self.closure(ast.nodes[0],curLocals)], self.closure(ast.expr,curLocals))
        elif isinstance(ast,AssName):
            if ast.name in self.needsHeaped and ast.flags !='OP_HEAP':
                return Subscript(Name(ast.name), 'OP_ASSIGN', [Const(0)])
            if ast.flags == 'OP_HEAP':
                ast.flags = 'OP_ASSIGN'
            return ast
        elif isinstance(ast,Discard):
            return Discard(self.closure(ast.expr,curLocals))
        elif isinstance(ast,Const):
            return ast
        elif isinstance(ast,Name):
            if ast.name in self.needsHeaped:
                return Subscript(ast, 'OP_APPLY', [Const(0)])
            return ast
        elif isinstance(ast,Add):
            return Add((self.closure(ast.left,curLocals),self.closure(ast.right,curLocals)))
        elif isinstance(ast,UnarySub):
            return UnarySub(self.closure(ast.expr,curLocals))
        elif isinstance(ast,CallFunc):

            if isinstance(ast.node,Name) and ast.node.name == "input":
                return ast
            #issue here, ast.node is used twice, could fix with Let
            node = self.closure(ast.node)
            #print '!',node
            #return CallPointer(CallFunc(Name('get_fun_ptr'), [self.closure(ast.node)], None,None),[CallFunc(Name("get_free_vars"), [self.closure(ast.node)])]+[self.closure(arg) for arg in ast.args])
            return CallPointer(CallFunc(Name('get_fun_ptr'), [node], None,None),[CallFunc(Name("get_free_vars"), [node])]+[self.closure(arg) for arg in ast.args])
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
            #print ast.locals[ast.else_]
            return If([(self.closure(ast.tests[0][0],curLocals), self.closure(ast.tests[0][1],curLocals))], self.closure(ast.else_,curLocals))
        elif isinstance(ast,While):
            return While(self.closure(ast.test,curLocals), self.closure(ast.body,curLocals), None)
        elif isinstance(ast,Lambda):
            return Lambda(ast.argnames,[], 0, self.closure(ast.code,curLocals))
        elif isinstance(ast,Return):
            return Return(self.closure(ast.value,curLocals))
        else:
            print "Error heapify:",ast

    def getLambdaName(self):
        self.lambdaNum+=1
        return "lambda %i" % self.lambdaNum