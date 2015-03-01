import compiler
from compiler.ast import *

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
    def __init__(self, ast):
        self.tmp = 0
        self.ast = ast
        #self.flat = []
    def explicate(self,ast):
        if isinstance(ast,Module):
            return Module(ast.doc,self.explicate(ast.node))
        elif isinstance(ast,Stmt):
            return Stmt([self.explicate(stmt) for stmt in ast.nodes])
        elif isinstance(ast,Printnl):
            return Printnl([self.explicate(ast.nodes[0])],ast.dest)
        elif isinstance(ast,Assign):
            return Assign([ast.nodes[0]], self.explicate(ast.expr))
        elif isinstance(ast,AssName):
            return ast
        elif isinstance(ast,Discard):
            return Discard(self.explicate(ast.expr))
        elif isinstance(ast,Const):
            return InjectFrom('int', ast)
        elif isinstance(ast,Name):
            if ast.name == "True":
                return InjectFrom('bool', Const(1))
            elif ast.name == "False":
                return InjectFrom('bool', Const(0))
            return ast
        elif isinstance(ast,Add):
            l = self.explicate(ast.left)
            r = self.explicate(ast.right)

            name1 = self.getNewTmp()
            name2 = self.getNewTmp()


            leftWord = (Or([IsType('int',name1),IsType('bool',name1)]))
            rightWord = (Or([IsType('int',name2),IsType('bool',name2)]))
            leftBig = IsType('big', name1)
            rightBig = IsType('big', name2)
            ifExp = IfExp(self.explicate(And([leftWord,rightWord])),InjectFrom('int', Add((ProjectTo('int',name1),ProjectTo('int',name2)))),
                IfExp(self.explicate(And([leftBig,rightBig])),InjectFrom('big',(Add((ProjectTo('big',name1),ProjectTo('big',name2))))), ThrowErr('add_error')))

            return Let(name1, l,Let(name2,r,ifExp))

        elif isinstance(ast,UnarySub):
            child = self.explicate(ast.expr)
            name = self.getNewTmp()

            orStmt= self.explicate(Or([IsType('int',name),IsType('bool',name)]))

            ifExp = IfExp(orStmt,InjectFrom('int', UnarySub(ProjectTo('int',name))), ThrowErr('unarysub_error'))
            return Let(name,child,ifExp)

        elif isinstance(ast,CallFunc):
            return ast
            #TODO: explicate over args

        elif isinstance(ast,Compare):
            l = self.explicate(ast.expr)
            r = self.explicate(ast.ops[0][1])

            name1 = self.getNewTmp()
            name2 = self.getNewTmp()
            op = ast.ops[0][0]

            if op == '==' or op == '!=':
                funcName = Name('equals' if op == '==' else 'not_equals')
                leftWord = (Or([IsType('int',name1),IsType('bool',name1)]))
                rightWord = (Or([IsType('int',name2),IsType('bool',name2)]))
                leftBig = IsType('big', name1)
                rightBig = IsType('big', name2)

                ifExp = IfExp(self.explicate(And([leftWord,rightWord])),InjectFrom('bool', Compare(name1,[(op, name2)])),
                IfExp(self.explicate(And([leftBig,rightBig])),InjectFrom('int',CallFunc(funcName,[ProjectTo('big',name1),ProjectTo('big',name2)])), InjectFrom('bool', Const(0))))

                return Let(name1,l,Let(name2,r,ifExp))
            elif op == 'is':
                return Compare(l,[(op,r)])
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
            return Not(InjectFrom('int', CallFunc(Name('is_true'), [self.explicate(ast.expr)])))

        elif isinstance(ast,List):
            return InjectFrom('int',List([self.explicate(e) for e in ast.nodes]))

        elif isinstance(ast,Dict):
            return Dict([(self.explicate(e), self.explicate(l)) for e,l in ast.items])

        elif isinstance(ast,Subscript):
            return Subscript(self.explicate(ast.expr), ast.flags, [self.explicate(ast.subs[0])])

        elif isinstance(ast,IfExp):
            return IfExp(self.explicate(ast.test), self.explicate(ast.then), self.explicate(ast.else_))
        elif isinstance(ast,IsType):
            return IsType(ast.typ,self.explicate(ast.var))
        else:
          print "Error:",ast
    def getNewTmp(self):
      newTmp = Name('expl '+`self.tmp`)
      self.tmp += 1
      return newTmp