from compiler.ast import *

class ConstantFold:

    def __init__(self, ast):
        self.ast = ast

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
            return [[], []]
        elif isinstance(ast, Function):
            self.fold(ast.code)
            return [[], []]


        else:
            print "Error toFunc:",ast
