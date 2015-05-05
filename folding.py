from compiler.ast import *
from uniquify import *

class ConstantFold:

    def __init__(self, ast):
        self.ast = ast
        self.varMap = {}

    def constructAddNode(self, s, l):
        if len(l) == 0:
            return Const(s)
        else:
            return Add((l.pop(0), self.constructAddNode(s, l)))

    def addConsts(self, lists, node):
        folded_sum = 0
        if lists[0]:
            for const in lists[0]:
                folded_sum += const
            if lists[1]:
                node = self.constructAddNode(folded_sum, lists[1])
            else:
                node = Const(folded_sum)
        return node

    def fold(self, ast):
        if isinstance(ast,Module):
            self.fold(ast.node)
            return ast

        elif isinstance(ast,Function):
            self.fold(ast.code)
            return [[],[]]

        elif isinstance(ast,Stmt):
            for stmt in ast.nodes:
                self.fold(stmt)
            return [[],[]]

        elif isinstance(ast,Printnl):
            lists = self.fold(ast.nodes[0])
            ast.nodes[0] = self.addConsts(lists, ast.nodes[0])

            return [[],[]]

        elif isinstance(ast,Assign):
            lists = self.fold(ast.expr)
            ast.expr = self.addConsts(lists, ast.expr)

            return [[], []]

        elif isinstance(ast,AssName):
            return [[], []]
        elif isinstance(ast,Discard):
            return [[], []]
        elif isinstance(ast,Const):
            return [[], []]
        elif isinstance(ast,Name):
            return [[], []]
        elif isinstance(ast,Add):
            lists = [[],[]]
            l = [[], []]
            if isinstance(ast.left, Add):
                lists = self.fold(ast.left)
            elif isinstance(ast.left, Const):
                lists[0].append(ast.left.value)
            elif isinstance(ast.left, UnarySub):
                node = ast.left.expr
                if isinstance(node, Add):
                    l = self.fold(node)
                    l[0] = map(lambda e: -e, l[0])
                    l[1] = map(lambda e: UnarySub(e), l[1])
                elif isinstance(node, Const):
                    lists[0].append(-node.value)
                else:
                    lists[1].append(UnarySub(node))
            else:
                l = [[], [ast.left]]

            l2 = [[], []]

            if isinstance(ast.right, Add):
                l2 = self.fold(ast.right)
            elif isinstance(ast.right, Const):
                l2 = [[ast.right.value], []]
            elif isinstance(ast.right, UnarySub):
                node = ast.right.expr
                if isinstance(node, Add):
                    l2 = self.fold(node)
                    l2[0] = map(lambda e: -e, l2[0])
                    l2[1] = map(lambda e: UnarySub(e), l2[1])
                elif isinstance(node, Const):
                    l2 = [[-node.value], []]
                else:
                    l2 = [[], [UnarySub(node)]]
            else:
                l2 = [[], [ast.right]]

            if not lists:
                lists = l
            else:
                lists[0] += l[0]
                lists[1] += l[1]

            lists[0] += l2[0]
            lists[1] += l2[1]

            return lists


        elif isinstance(ast,UnarySub):
            return [[], []]
        elif isinstance(ast,CallFunc):
            return [[], []]

        elif isinstance(ast,Compare):
            return [[], []]
        elif isinstance(ast,Or):
            return [[], []]
        elif isinstance(ast,And):
            return [[], []]
        elif isinstance(ast,Not):
            return [[], []]
        elif isinstance(ast,List):
            return [[], []]
        elif isinstance(ast,Dict):
            return [[], []]
        elif isinstance(ast,Subscript):
            return [[], []]
        elif isinstance(ast,IfExp):
            testLists = self.fold(ast.test)
            ast.test = self.addConsts(testLists, ast.test)

            self.fold(ast.then)
            self.fold(ast.else_)

            return [[], []]
        elif isinstance(ast,If):
            temp = ast.tests[0]
            l = [temp[0], temp[1]]
            ast.tests[0] = l
            testLists = self.fold(ast.tests[0][0])
            ast.tests[0][0] = self.addConsts(testLists, ast.tests[0][0])

            self.fold(ast.tests[0][1])
            self.fold(ast.else_)

            return [[], []]
        elif isinstance(ast,While):
            return [[], []]
        elif isinstance(ast,Lambda):
            self.fold(ast.code)
            return [[], []]
        elif isinstance(ast, Function):
            self.fold(ast.code)
            return [[], []]
        elif isinstance(ast, FuncLocals):
            self.fold(ast.func)
            return [[], []]


        else:
            print "Error toFunc:",ast

    def propigation(self, ast):
        print ast
        if isinstance(ast,Module):
            self.propigation(ast.node)
            return ast

        elif isinstance(ast,Function):
            self.propigation(ast.code)
            return None

        elif isinstance(ast,Stmt):
            for stmt in ast.nodes:
                self.propigation(stmt)
            return None

        elif isinstance(ast,Printnl):
            retVal = self.propigation(ast.nodes[0])
            if retVal:
                ast.nodes[0] = retVal

            return None

        elif isinstance(ast,Assign):
            retVal = self.propigation(ast.expr)
            if isinstance(ast.expr, Const):
                print "!!!!!!!!!!!!"
                print ast.nodes[0]
                if isinstance(ast.nodes[0], AssName):
                    print "@@@@@@@@@@@@"
                    print ast.nodes[0]
                    self.varMap[ast.nodes[0].name] = ast.expr.value
            elif retVal:
                if isinstance(ast.nodes[0], AssName):
                    if isinstance(ast.expr, Name):
                        self.varMap[ast.nodes[0].name] = retVal.value

                ast.expr = retVal

            return None

        elif isinstance(ast,AssName):
            return None
        elif isinstance(ast,Discard):
            return None
        elif isinstance(ast,Const):
            return None
        elif isinstance(ast,Name):
            if self.varMap.has_key(ast.name):
                return Const(self.varMap[ast.name])
            else:
                return None
        elif isinstance(ast,Add):
            left = self.propigation(ast.left)
            right = self.propigation(ast.right)
            if left:
                ast.left = left
            if right:
                ast.right = right

            return None


        elif isinstance(ast,UnarySub):
            expr = self.propigation(ast.expr)
            if expr:
                ast.expr = expr
            return None
        elif isinstance(ast,CallFunc):
            return None

        elif isinstance(ast,Compare):
            return None
        elif isinstance(ast,Or):
            return None
        elif isinstance(ast,And):
            return None
        elif isinstance(ast,Not):
            return None
        elif isinstance(ast,List):
            return None
        elif isinstance(ast,Dict):
            return None
        elif isinstance(ast,Subscript):
            if isinstance(ast.subs[0], Name):
                if self.varMap.has_key(ast.subs[0].name):
                    return Const(self.varMap[ast.subs[0].name])
            return None
        elif isinstance(ast,IfExp):
            # testLists = self.propigation(ast.test)
            # ast.test = self.addConsts(testLists, ast.test)

            # self.propigation(ast.then)
            # self.propigation(ast.else_)

            return None
        elif isinstance(ast,If):
            # temp = ast.tests[0]
            # l = [temp[0], temp[1]]
            # ast.tests[0] = l
            # testLists = self.propigation(ast.tests[0][0])
            # ast.tests[0][0] = self.addConsts(testLists, ast.tests[0][0])

            # self.propigation(ast.tests[0][1])
            # self.propigation(ast.else_)

            return None
        elif isinstance(ast,While):
            return None
        elif isinstance(ast,Lambda):
            self.propigation(ast.code)
            return None
        elif isinstance(ast, Function):
            self.propigation(ast.code)
            return None
        elif isinstance(ast, FuncLocals):
            self.propigation(ast.func)
            return None


        else:
            print "Error toFunc:",ast
