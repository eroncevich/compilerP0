from heapify import *
from explicate import *
class Typecheck:
    def __init__(self):
        self.typeMap = [{}]
        self.counter =0

    def typeAnalyze(self,ast):
        if isinstance(ast,Module):
            self.typeAnalyze(ast.node)
            return self.typeMap
        elif isinstance(ast,Stmt):
            for stmt in ast.nodes:
                print stmt
                self.typeMap.append(self.typeMap[self.counter].copy())
                self.counter+=1
                self.typeAnalyze(stmt)
                print "-->",self.typeMap[self.counter]
            return None
        elif isinstance(ast,Printnl):
            return 
        elif isinstance(ast,Assign):
            key =  self.typeAnalyze(ast.nodes[0])
            self.typeMap[self.counter][key]=self.typeAnalyze(ast.expr)
        elif isinstance(ast,AssName):
            return ast.name
        elif isinstance(ast,Discard):
            return 
        elif isinstance(ast,Const):
            #print "const"
            if ast.value == 0.25 or ast.value == 1.25:
                return "bool"
            return "int"
        elif isinstance(ast,Name):
            #print "name"
            return self.typeMap[self.counter][ast.name]
        elif isinstance(ast,Add):
            #print "add"
            left = self.typeAnalyze(ast.left)
            right = self.typeAnalyze(ast.right)
            if left == right:
                return left
            return "unknown"
        elif isinstance(ast,UnarySub):
            return self.typeAnalyze(ast.expr)
        elif isinstance(ast,CallFunc):
            if ast.node.name == "input":
                return "int"
            return "unknown"
        elif isinstance(ast,Compare):
            return

        elif isinstance(ast,Or):
            return

        elif isinstance(ast,And):
            return

        elif isinstance(ast,Not):
            return

        elif isinstance(ast,List):
            return "big"

        elif isinstance(ast,Dict):
            return "big"

        elif isinstance(ast,Subscript):
            if ast.flags == 'OP_ASSIGN':
                if isinstance(ast.expr, Name):
                    return ast.expr.name
                return None
            return "unknown"

        elif isinstance(ast,IfExp):
            return 
        elif isinstance(ast,IsType):
            return 
        elif isinstance(ast,If): 
            self.typeAnalyze(ast.tests[0][0])
            startMap = self.typeMap[self.counter].copy()
            self.typeAnalyze(ast.tests[0][1])
            ifMap= self.typeMap[self.counter]
            self.typeMap[self.counter] = startMap
            self.typeAnalyze(ast.else_)
            elseMap= self.typeMap[self.counter].copy()
            for key in elseMap:
                if ifMap.has_key(key) and elseMap[key]!=ifMap[key]:
                    self.typeMap[self.counter][key] = 'unknown'
            return None
        elif isinstance(ast,While):
            self.typeAnalyze(ast.test)
            self.typeAnalyze(ast.body)
            return None
        elif isinstance(ast,FuncLocals):
            self.typeMap[self.counter] = {}
            for arg in ast.func.argnames:
                self.typeMap[self.counter][arg] = "unknown"
            return self.typeAnalyze(ast.func.code)
        elif isinstance(ast,Return):
            return 
        elif isinstance(ast,CallPointer):
            return
        else:
            print "Error typecheck:",ast
