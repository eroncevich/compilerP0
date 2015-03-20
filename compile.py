#import compiler
import explicate
import sys
import x86AST
import uniquify
#from compiler.ast import *
from x86AST import *
from explicate import *
from uniquify import *

class flatParser:
  def __init__(self, ast):
    self.tmp = 0
    self.ast = ast
    self.flat = []
    self.ifTmp =0
    self.flat.append(Assign(Name("True"), Const(5)))
    self.flat.append(Assign(Name("False"), Const(1)))

  def flatAst(self, ast):
    if isinstance(ast,Module):
      self.flatAst(ast.node)

    elif isinstance(ast,Stmt):
      for stmt in ast.nodes:
        self.flatAst(stmt)

    elif isinstance(ast,Printnl):
      child = self.flatAst(ast.nodes[0])
      if isinstance(child, Const):
          newTmp = self.getNewTmp()
          self.flat.append(Assign(newTmp,child))
          child= newTmp
      self.flat.append(Printnl([child],None))

    elif isinstance(ast,Assign):
      varVal = self.flatAst(ast.expr)
      for node in ast.nodes:
        varName = self.flatAst(node)
        self.flat.append(Assign(varName, varVal))
        self.tmp += 1
      return varVal

    elif isinstance(ast,AssName):
      return Name(ast.name)

    elif isinstance(ast,Discard):
      child = self.flatAst(ast.expr)
      if isinstance(child,CallFunc):
        self.flat.append(child)

    elif isinstance(ast,Const):
      return ast

    elif isinstance(ast,Name):
      return ast

    elif isinstance(ast,Add):
        l = self.flatAst(ast.left)
        r = self.flatAst(ast.right)
        #if(isinstance(l,Const) and isinstance(r,Const)):
        #    return Const(l.value+r.value)

        newTmp = self.getNewTmp()
        self.flat.append(Assign(newTmp, Add((l,r))))
        return newTmp

    elif isinstance(ast,UnarySub):
      child = self.flatAst(ast.expr)
      if isinstance(child, Const):
        child = Const(-child.value)
        newTmp = child
      else:
        newTmp = self.getNewTmp()
        self.flat.append(Assign(newTmp,UnarySub(child)))
      return newTmp

    elif isinstance(ast,CallFunc):
      if ast.node.name == "input":
          ast.node.name = "input_int"
      argFlat = [self.flatAst(arg) for arg in ast.args]
      newTmp = self.getNewTmp()
      self.flat.append(Assign(newTmp, CallFunc(ast.node,argFlat)))
      newTmp2 = self.getNewTmp()
      self.flat.append(Assign(newTmp2, newTmp))
      return newTmp2

    elif isinstance(ast,Compare):
        l = self.flatAst(ast.expr)
        r = self.flatAst(ast.ops[0][1])
        newTmp = self.getNewTmp()
        self.flat.append(Assign(newTmp,Compare(l,[(ast.ops[0][0],r)])))
        return newTmp
    elif isinstance(ast,Not):
        newTmp = self.getNewTmp()
        child = self.flatAst(ast.expr)
        self.flat.append(Assign(newTmp,Not(child)))
        #self.flatAst(Compare(ConstOp(0),['==']))
        return newTmp

    elif isinstance(ast,List):
        newTmp = self.getNewTmp()
        self.flat.append(Assign(newTmp,List([self.flatAst(e) for e in ast.nodes])))
        return newTmp

    elif isinstance(ast,Dict):
        newTmp = self.getNewTmp()
        keys = [reversed((self.flatAst(l), self.flatAst(e))) for e,l in ast.items]

        #self.flat.append(Assign(newTmp,Dict([(self.flatAst(e), self.flatAst(l)) for e,l in ast.items])))
        self.flat.append(Assign(newTmp,Dict(keys)))
        return newTmp

    elif isinstance(ast,Subscript):
        bigObj= self.flatAst(ast.expr)
        child = self.flatAst(ast.subs[0])
        if "OP_ASSIGN" in ast.flags:
            return Subscript(bigObj,ast.flags,[child])
        else:
            newTmp = self.getNewTmp()
            self.flat.append(Assign(newTmp,Subscript(bigObj,ast.flags,[child])))
            return newTmp

    elif isinstance(ast,IfExp):
        condTmp = self.getNewTmp()
        newTmp = self.getNewTmp()
        test = self.flatAst(ast.test)
        self.flat.append(Assign(condTmp,self.flatAst(CallFunc(Name('is_true'), [test]))))

        (ifName,thenName,endName) = self.getIfTmp()

        self.flat.append(Name(ifName.name +' , '+condTmp.name))

        else_ = self.flatAst(ast.else_)
        self.flat.append(Assign(newTmp,else_))

        self.flat.append(thenName)
        then = self.flatAst(ast.then)
        self.flat.append(Assign(newTmp,then))


        self.flat.append(endName)
        return newTmp
    elif isinstance(ast,If):
        condTmp = self.getNewTmp()
        #newTmp = self.getNewTmp()
        test = self.flatAst(ast.tests[0][0])
        self.flat.append(Assign(condTmp,self.flatAst(CallFunc(Name('is_true'), [test]))))

        (ifName,thenName,endName) = self.getIfTmp()

        self.flat.append(Name(ifName.name +' , '+condTmp.name))

        else_ = self.flatAst(ast.else_)
        #self.flat.append(Assign(newTmp,else_))

        self.flat.append(thenName)
        then = self.flatAst(ast.tests[0][1])
        #self.flat.append(Assign(newTmp,then))

        self.flat.append(endName)
        return None #Should be a Stmt
    elif isinstance(ast,InjectFrom):
        child = self.flatAst(ast.arg)
        newTmp = self.getNewTmp()
        self.flat.append(Assign(newTmp, InjectFrom(ast.typ,child)))
        return newTmp
    elif isinstance(ast,ProjectTo):
        child = self.flatAst(ast.arg)
        newTmp = self.getNewTmp()
        self.flat.append(Assign(newTmp, ProjectTo(ast.typ,child)))
        return newTmp

    elif isinstance(ast, Let):
        rhs = self.flatAst(ast.rhs)
        self.flat.append(Assign(ast.var,rhs))
        newTmp1 = self.getNewTmp()
        child = self.flatAst(ast.body)
        self.flat.append(Assign(newTmp1,child))
        return newTmp1
    # elif isinstance(ast,IsType):
    #     child = self.flatAst(ast.var[0])
    #     newTmp = self.getNewTmp()
    #     funcName = Name("is_%s" % ast.typ )
    #     self.flat.append(Assign(newTmp, self.flatAst(CallFunc(funcName, [child]))))
    #     self.flat.append(Assign(newTmp, InjectFrom('bool',newTmp)))
    #     return newTmp
    elif isinstance(ast,IsType):
        childs = [self.flatAst(e) for e in ast.var]
        newTmp = self.getNewTmp()
        self.flat.append(Assign(newTmp, IsType(ast.typ, childs)))
        self.flat.append(Assign(newTmp, InjectFrom('bool',newTmp)))
        return newTmp
    elif isinstance(ast,ThrowErr):
        return ast

    else:
        print "***error:", ast
        pass

  def getNewTmp(self):
      newTmp = Name('tmp '+`self.tmp`)
      self.tmp += 1
      return newTmp
  def getIfTmp(self):
      ifName = Name('if '+`self.ifTmp`)
      thenName = Name('then '+`self.ifTmp`)
      endName = Name('end '+`self.ifTmp`)
      self.ifTmp += 1
      return (ifName,thenName,endName)

  def printFlat(self):
    print "*****Args*****"
    for args in self.flat:
      print args

class pyTo86:
  def __init__(self, flatAst, stackSize):
    self.flatAst = flatAst
    self.stackSize = stackSize
    self.output = []
    self.varLookup = {}
    self.varCounter = 4
    self.cmp =0
    self.flat = 0

  def convert86(self):
      for curLine in self.flatAst:
          if isinstance(curLine, Assign):
              if isinstance(curLine.nodes,Subscript):
                  subs = self.getFlatTmp()
                  self.convertLine(curLine.expr, subs)
                  self.output.append(FuncOp(NameOp("set_subscript"),[self.getConstOrName(curLine.nodes.expr),self.getConstOrName(curLine.nodes.subs[0]),subs],NameOp("*void")))
              else:
                  self.convertLine(curLine.expr, NameOp(curLine.nodes.name))
          elif isinstance(curLine, Printnl):
              self.output.append(PrintOp(self.getConstOrName(curLine.nodes[0])))
          elif isinstance(curLine,Name):
              line = curLine.name.split()
              if line[0] == "if":
                  condTmp = Name("%s %s" % (line[3],line[4]))
                  #print repr(self.getConstOrName(condTmp))
                  self.output.append(BinaryOp("cmp", ConstOp(0),self.getConstOrName(condTmp)))
                  self.output.append(JumpOp("jne",NameOp("then%s"%line[1])))
              elif line[0] == "then":
                  self.output.append(JumpOp("jmp", NameOp("end%s"%line[1])))
                  self.output.append(ClauseOp(NameOp("then%s"%line[1])))
              elif line[0] == "end":
                  self.output.append(ClauseOp(NameOp("end%s"%line[1])))
          elif isinstance(curLine, UnarySub):
              #check to delete
              self.output.append(UnaryOp("negl", NameOp(curLine.expr.name)))


  def convertLine(self,curLine,tmpName):
      if isinstance(curLine,Add):
          self.output.append(BinaryOp("movl", self.getConstOrName(curLine.left), tmpName))
          self.output.append(BinaryOp("addl", self.getConstOrName(curLine.right), tmpName))
      elif isinstance(curLine, Const):
          self.output.append(BinaryOp("movl", ConstOp(curLine.value), tmpName))
      elif isinstance(curLine, Name):
          self.output.append(BinaryOp("movl", NameOp(curLine.name), tmpName))
      elif isinstance(curLine, UnarySub):
          self.output.append(BinaryOp("movl", NameOp(curLine.expr.name), tmpName))
          self.output.append(UnaryOp("negl", tmpName))
      elif isinstance(curLine, CallFunc):
          self.output.append(FuncOp(NameOp(curLine.node.name),[self.getConstOrName(arg) for arg in curLine.args],tmpName))
      elif isinstance(curLine, InjectFrom):
          if 0:
              self.output.append(BinaryOp("movl",self.getConstOrName(curLine.arg),tmpName))
              self.output.append(BinaryOp("sarl",ConstOp(2),tmpName))
          else:
              funcName = NameOp("inject_%s"%(curLine.typ))
              self.output.append(FuncOp(funcName,[self.getConstOrName(curLine.arg)],tmpName))
      elif isinstance(curLine, ProjectTo):
          if curLine.typ == 'int' or curLine.typ == 'bool':
              self.output.append(BinaryOp("movl",self.getConstOrName(curLine.arg),tmpName))
              self.output.append(BinaryOp("sarl",ConstOp(2),tmpName))
          else:
              funcName = NameOp("project_%s"%(curLine.typ))
              self.output.append(FuncOp(funcName,[self.getConstOrName(curLine.arg)],tmpName))
      elif isinstance(curLine,Not):
          self.output.append(BinaryOp("movl", self.getConstOrName(curLine.expr),tmpName))
          self.output.append(UnaryOp("notl",tmpName))
          self.output.append(BinaryOp("addl",ConstOp(2), tmpName))
      elif isinstance(curLine,Compare):
          (neCmp,endCmp) = self.getCmpLabel()
          jumpType = "je" if curLine.ops[0][0] == '!=' else "jne"

          destVar = self.getConstOrName(curLine.ops[0][1])
          if isinstance (curLine.ops[0][1], Const):
              destVar = self.getFlatTmp()
              self.output.append(BinaryOp("movl", self.getConstOrName(curLine.ops[0][1]),destVar))

          self.output.append(BinaryOp("cmp",self.getConstOrName(curLine.expr),destVar))
          self.output.append(JumpOp(jumpType,neCmp))
          self.output.append(BinaryOp("movl", ConstOp(1) ,tmpName))
          self.output.append(JumpOp("jmp",endCmp))
          self.output.append(ClauseOp(neCmp))
          self.output.append(BinaryOp("movl", ConstOp(0) ,tmpName))
          self.output.append(ClauseOp(endCmp))
      elif isinstance(curLine,List):
          elem =0
          lenTmp = self.getFlatTmp()
          cursorTmp = self.getFlatTmp()
          projectTmp = self.getFlatTmp()
          self.convertLine(InjectFrom('int', Const(len(curLine.nodes))),lenTmp)
          self.output.append(FuncOp(NameOp("create_list"),[lenTmp],tmpName))
          self.convertLine(InjectFrom('big', Name(tmpName.name)),projectTmp)
          for e in curLine.nodes:
              self.convertLine(InjectFrom('int', Const(elem)), cursorTmp)
              self.output.append(FuncOp(NameOp("set_subscript"),[projectTmp,cursorTmp,self.getConstOrName(e)],NameOp("*void")))
              elem+=1
      elif isinstance(curLine,Dict):
          projectTmp = self.getFlatTmp()
          self.output.append(FuncOp(NameOp("create_dict"),[],tmpName))
          self.convertLine(InjectFrom('big', Name(tmpName.name)),projectTmp)
          for l,r in curLine.items:
              self.output.append(FuncOp(NameOp("set_subscript"),[projectTmp,self.getConstOrName(l),self.getConstOrName(r)],NameOp("*void")))
              #self.output.append(FuncOp(NameOp("set_subscript"),[projectTmp,self.getConstOrName(l),ConstOp(16)],self.getConstOrName(r)))
      elif isinstance(curLine,Subscript):
          if curLine.flags == 'OP_APPLY':
              self.output.append(FuncOp(NameOp("get_subscript"),[self.getConstOrName(curLine.expr),self.getConstOrName(curLine.subs[0])],tmpName))
      elif isinstance(curLine,IsType):
          #print "majesty", curLine.var[0]
          maskTmp = self.getFlatTmp()
          self.output.append(BinaryOp("movl", self.getConstOrName(curLine.var[0]),maskTmp))
          self.output.append(BinaryOp("andl",ConstOp(3),maskTmp))

          if curLine.typ == "int":
              self.output.append(BinaryOp("cmp",ConstOp(0),maskTmp))
          elif curLine.typ == "bool":
              self.output.append(BinaryOp("cmp",ConstOp(1),maskTmp))
          elif curLine.typ == "big":
              self.output.append(BinaryOp("cmp",ConstOp(3),maskTmp))
          elif curLine.typ == "small":
              self.output.append(BinaryOp("sarl",ConstOp(1),maskTmp))
              self.output.append(BinaryOp("cmp",ConstOp(0),maskTmp))
          else:
              print "Error wrong type"
              exit()
          self.output.append(BinaryOp("movl", ConstOp(1),maskTmp))
          self.output.append(BinaryOp("movl",ConstOp(0),tmpName))
          self.output.append(BinaryOp("cmove",maskTmp,tmpName))
          #need to implement cmovl

      else:
          #print "Assign Error:",curLine
          pass

  def getConstOrName(self, line):
    if isinstance(line, Name):
      return  NameOp(line.name)
    elif isinstance(line,Const):
      return ConstOp(line.value)
    else:
      print "convert None Type", line
      return None

  def getCmpLabel(self):
      neCmp = NameOp('ne_cmp'+`self.cmp`)
      endCmp = NameOp('end_cmp'+`self.cmp`)
      self.cmp += 1
      return (neCmp,endCmp)
  def getFlatTmp(self):
      flatTmp = NameOp('flat '+`self.flat`)
      self.flat += 1
      return flatTmp

if __name__ == "__main__":
  with open (sys.argv[1], "r") as myfile:
    inStr=myfile.read()

  f = open('/dev/null', 'w')
  #sys.stdout = f #Uncomment to turn off output

  ast = compiler.parse(inStr)
  print ast

  myUnique = Uniquify(ast)
  myUnique.getLocals(ast)
  print ast

  myUnique.unique(ast)
  print "@@@@@@@"
  print ast

  myExplicate = ExplicateParser(ast)
  ast = myExplicate.explicate(ast)
  #print ast

  parser = flatParser(ast)

  parser.flatAst(parser.ast)
  #parser.printFlat()
  to86 = pyTo86(parser.flat,parser.tmp)
  to86.convert86()
  #for line in to86.output: print line
  ig = InterferenceGraph()

  output = ig.createLiveness(to86.output)
  #output
  #igcolor = ig.colorGraph()
  #ig.cleanUpCrew(to86.output,igcolor)

  outFileName = sys.argv[1].replace('.py','.s')
  fout = open(outFileName, 'w+')
  fout.write(output)
