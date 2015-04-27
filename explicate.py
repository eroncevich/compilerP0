import compiler
from compiler.ast import *
import heapify
from heapify import *

class GetTag(Node):
    def __init__(self, arg):
        self.arg = arg
class InjectFrom(Node):
    def __init__(self, typ, arg):
        self.typ = typ
        self.arg = arg
    def __repr__(self):
        return "InjectFrom(\'%s\',%s)" % (self.typ,self.arg)
class ProjectTo(Node):
    def __init__(self, typ, arg):
        self.typ = typ
        self.arg = arg
    def __repr__(self):
        return "ProjectTo(\'%s\',%s)" % (self.typ,self.arg)
class Let(Node):
    def __init__(self, var, rhs, body):
        self.var = var
        self.rhs = rhs
        self.body = body
    def __repr__(self):
        return "Let(%s,%s,%s)" % (self.var,self.rhs,self.body)
class ThrowErr(Node):
    def __init__(self,strName):
        self.strName = strName
    def __repr__(self):
        return "ThrowErr(\'%s\')" % (self.strName)
class IsType(Node):
    def __init__(self,typ, var):
        self.typ = typ
        self.var = var
    def __repr__(self):
        return "IsType(%s,%s)" % (self.typ,self.var)


class ExplicateParser:
    def __init__(self, ast,myMap):
        self.tmp = 0
        self.ast = ast
        self.typeMap = myMap
        self.counter = -1
        self.curType = "unknown"
        self.big = "big"
        self.int = "int"
        self.bool = "bool"
        #self.flat = []
    def explicate(self,ast):
        if isinstance(ast,Module):
            return Module(ast.doc,self.explicate(ast.node))
        elif isinstance(ast,Stmt):
            curStmt = []
            for stmt in ast.nodes:
                self.counter +=1
                #print "#", self.typeMap[self.counter]
                #print "-->", stmt
                curStmt.append(self.explicate(stmt))
            #return Stmt([ for stmt in ast.nodes])
            return Stmt(curStmt)
        elif isinstance(ast,Printnl):
            return Printnl([self.explicate(ast.nodes[0])],ast.dest)
        elif isinstance(ast,Assign):
            return Assign([self.explicate(ast.nodes[0])], self.explicate(ast.expr))
        elif isinstance(ast,AssName):
            return ast
        elif isinstance(ast,Discard):
            return Discard(self.explicate(ast.expr))
        elif isinstance(ast,Const):
            self.curType = self.int
            return Const(int(ast.value*4))
        elif isinstance(ast,Name):
            self.curType = self.typeMap[self.counter][ast.name] if self.typeMap[self.counter].has_key(ast.name) else "unknown"
            #print ast.name
            #self.curType = self.typeMap[self.counter][ast.name]

            return ast
        elif isinstance(ast,Add):
            l = self.explicate(ast.left)
            lType = self.curType
            r = self.explicate(ast.right)
            rType = self.curType

            #print lType, rType

            if (lType == 'int' or lType =='bool') and (rType == 'int' or rType=='bool'):
                self.curType = "int"
                return InjectFrom('int', Add((ProjectTo('int',l),ProjectTo('int',r))))
            if lType == "big" and rType == "big":
                self.curType = "int"
                return InjectFrom('big',CallFunc(Name("add"),[ProjectTo('big',l),ProjectTo('big',r)]))


            #if lType == "unknown" or rType =="unknown":
            name1 = self.getNewTmp()
            name2 = self.getNewTmp()

            correctType = IsType('small',[name1,name2])
            correctBig = IsType('big',[name1,name2])
            ifExp = IfExp(correctType,InjectFrom('int', Add((ProjectTo('int',name1),ProjectTo('int',name2)))),
                IfExp(correctBig,InjectFrom('big',CallFunc(Name("add"),[ProjectTo('big',name1),ProjectTo('big',name2)])), ThrowErr('add_error')))

            return Let(name1, l,Let(name2,r,ifExp))
            #return 
            #return ifExp

        elif isinstance(ast,UnarySub):
            child = self.explicate(ast.expr)
            #cType = self.curType

            if self.curType == "int":
                self.curType = "int"
                return InjectFrom('int', UnarySub(ProjectTo('int',child)))

            name = self.getNewTmp()

            orStmt= self.explicate(Or([IsType('int',[name]),IsType('bool',[name])]))

            ifExp = IfExp(orStmt,InjectFrom('int', UnarySub(ProjectTo('int',name))), ThrowErr('unarysub_error'))
            return Let(name,child,ifExp)

        elif isinstance(ast,CallFunc):
            arglist = []
            for arg in ast.args:
                if not isinstance(arg,str):
                    arglist+= [self.explicate(arg)]
                else:
                    arglist+=[arg]

            if ast.node.name == "create_closure":
                return InjectFrom('big',CallFunc(ast.node,arglist, None,None))
            else:
                return CallFunc(ast.node,arglist, None,None)

        elif isinstance(ast,Compare):
            l = self.explicate(ast.expr)
            lType = self.curType
            r = self.explicate(ast.ops[0][1])
            rType = self.curType

            name1 = self.getNewTmp()
            name2 = self.getNewTmp()
            op = ast.ops[0][0]

            if op == '==' or op == '!=':
                funcName = Name('equal' if op == '==' else 'not_equal')
                leftWord = IsType('small',[name1])
                rightWord = IsType('small',[name2])
                leftBig = IsType('big', [name1])
                rightBig = IsType('big', [name2])
                if op == '==':
                    exception = InjectFrom('bool', Const(0))
                else:
                    exception = InjectFrom('bool', Const(1))

                #print lType, rType

                if (lType == 'int' or lType =='bool') and (rType == 'int' or rType=='bool'):
                    self.curType = self.bool
                    return InjectFrom('bool', Compare(ProjectTo('int',l),[(op, ProjectTo('int',r))]))
                if lType =='big' and rType== 'big':
                    self.curType = self.bool
                    return InjectFrom('bool',CallFunc(funcName,[ProjectTo('big',l),ProjectTo('big',r)]))

                ifExp = IfExp(self.explicate(And([leftWord,rightWord])),InjectFrom('bool', Compare(ProjectTo('int',name1),[(op, ProjectTo('int',name2))])),
                IfExp(self.explicate(And([leftBig,rightBig])),InjectFrom('bool',CallFunc(funcName,[ProjectTo('big',name1),ProjectTo('big',name2)])), exception))

                return Let(name1,l,Let(name2,r,ifExp))
            elif op == 'is':
                return InjectFrom('bool',Compare(l,[(op,r)]))
            else:
                print "Error Compare"
                exit()


        elif isinstance(ast,Or):
            l = self.explicate(ast.nodes[0])
            r = self.explicate(ast.nodes[1])

            name = self.getNewTmp()
            ifExp = IfExp(InjectFrom('bool',CallFunc(Name('is_true'), [name])), name, r)
            return Let(name, l, ifExp)
        elif isinstance(ast,And):
            l = self.explicate(ast.nodes[0])
            r = self.explicate(ast.nodes[1])

            name = self.getNewTmp()

            return Let(name, l, IfExp(InjectFrom('bool',CallFunc(Name('is_true'), [name])), r, name))

        elif isinstance(ast,Not):
            return InjectFrom('bool',Not(CallFunc(Name('is_true'), [self.explicate(ast.expr)])))
            #compare = Compare(CallFunc(Name('is_true'), [self.explicate(ast.expr)], self.explicate(Const(0))))
            #return InjectFrom('bool', )

        elif isinstance(ast,List):
            tmpList = List([self.explicate(e) for e in ast.nodes])
            self.curType = self.big
            return InjectFrom('big',tmpList)

        elif isinstance(ast,Dict):
            tmpDict = Dict([(self.explicate(e), self.explicate(l)) for e,l in ast.items])
            self.curType = self.big
            return InjectFrom('big',tmpDict)

        elif isinstance(ast,Subscript):
            tmpExpr = self.explicate(ast.expr)
            tmpList = self.explicate(ast.subs[0])
            self.curType = "unknown"
            return Subscript(tmpExpr, ast.flags, [tmpList])

        elif isinstance(ast,IfExp):
            return IfExp(self.explicate(ast.test), self.explicate(ast.then), self.explicate(ast.else_))
        elif isinstance(ast,IsType):
            return IsType(ast.typ,[self.explicate(e) for e in ast.var])
        elif isinstance(ast,If):
            return If([(self.explicate(ast.tests[0][0]), self.explicate(ast.tests[0][1]))], self.explicate(ast.else_))
        elif isinstance(ast,While):
            return While(self.explicate(ast.test), self.explicate(ast.body), None)
        elif isinstance(ast,FuncLocals):
            return Function(None, ast.name,ast.func.argnames, [],0,None, self.explicate(ast.func.code))
        elif isinstance(ast,Return):
            return Return(self.explicate(ast.value))
        elif isinstance(ast,CallPointer):
            #print ast.args
            arglist = []
            for arg in ast.args:
                if not isinstance(arg,str):
                    arglist+= [self.explicate(arg)]
                else:
                    arglist+=[arg]
            return CallPointer(self.explicate(ast.node), arglist)
        else:
            print "Error explicate:",ast
    def getNewTmp(self):
      newTmp = Name('expl '+`self.tmp`)
      self.tmp += 1
      return newTmp