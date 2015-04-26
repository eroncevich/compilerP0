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
                print "-->", stmt
                self.typeMap.append(self.typeMap[self.counter].copy())
                self.typeAnalyze(stmt)
                print self.typeMap[self.counter]
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
            print "add"
            left = self.typeAnalyze(ast.left)
            right = self.typeAnalyze(ast.right)
            if left == right:
                return left
            return "unknown"
        elif isinstance(ast,UnarySub):
            print "UnarySub"
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
            return 

        elif isinstance(ast,Dict):
            return

        elif isinstance(ast,Subscript):
            return 

        elif isinstance(ast,IfExp):
            return 
        elif isinstance(ast,IsType):
            return 
        elif isinstance(ast,If):
            return
        elif isinstance(ast,While):
            return
        elif isinstance(ast,FuncLocals):
            return self.typeAnalyze(ast.func.code)
        elif isinstance(ast,Return):
            return 
        elif isinstance(ast,CallPointer):
            return
        else:
            print "Error typecheck:",ast