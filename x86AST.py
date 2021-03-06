from sets import Set
from pprint import pprint
#import 

class Node(object):
    def __init__(self):
        pass

class NameOp(Node):
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return "NameOp(%s)" % self.name
    def __str__(self):
        return "%s" % self.name

class LabelOp(Node):
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return "LabelOp(%s)" % self.name
    def __str__(self):
        return "%s" % self.name

class RegOp(Node):
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return "RegOp(%%%s)" % self.name
    def __str__(self):
        return "%%%s" % self.name

class ConstOp(Node):
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return "ConstOp(%d)" % self.value
    def __str__(self):
        return "$%d" % self.value

class FuncOp(Node):
    def __init__(self, name, args, var, star =''):
        self.name = name
        self.args = args
        self.var = var
        self.star = star
    def __repr__(self):
        return "FuncOp(%s,%s,%s,%s)" % (self.name, self.args, self.var, self.star)
    def __str__(self):
        return "call %s %s %s -> %s" % (self.star,str(self.name),[str(arg) for arg in self.args], str(self.var))

class PrintOp(Node):
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        if isinstance(self.name, ConstOp):
            return "PrintOp(ConstOp(%s))" % self.name
        elif isinstance(self.name, NameOp):
            return "PrintOps(NameOp(%s))" % self.name
    def __str__(self):
        return "print %s" % self.name

class BinaryOp(Node):
    def __init__(self, name, src, dest):
        self.name = name
        self.src = src
        self.dest = dest
    def __repr__(self):
        return "BinaryOp(%s, %s, %s)" % (self.name, repr(self.src), repr(self.dest))
    def __str__(self):
        return "%s %s, %s" % (self.name, str(self.src), str(self.dest))

class UnaryOp(Node):
    def __init__(self, name, param):
        self.name = name
        self.param = param
    def __repr__(self):
        return "UnaryOp(%s, %s)" % (self.name, repr(self.param))
    def __str__(self):
        return "%s %s" % (self.name, str(self.param))
class JumpOp(Node):
    def __init__(self, name,label):
        self.name = name
        self.label = label
    def __repr__(self):
        return "JumpOp(%s,%s)" % (self.name,repr(self.label))
    def __str__(self):
        return "%s %s" % (self.name, str(self.label))
class ClauseOp(Node):
    def __init__(self, label):
        self.label = label
    def __repr__(self):
        return "ClauseOp(%s)" % (repr(self.label))
    def __str__(self):
        return "%s:" % (str(self.label))

class FuncStartOp(Node):
    def __init__(self, name,args):
        self.name = name
        self.args = args
    def __repr__(self):
        return "FuncStartOp(%s, %s)" % (self.name,repr(self.args))
    def __str__(self):
        return "%s,%s" % (self.name, str(self.args))

class ReturnOp(Node):
    def __init__(self, ret):
        self.ret = ret
    def __repr__(self):
        return "ReturnOp(%s)" % (repr(self.ret))
    def __str__(self):
        return "ret %s" % (str(self.ret))

class EndOp(Node):
    def __repr__(self):
        return "EndOp()"
    def __str__(self):
        return "FuncEnd"


class InterferenceGraph:
    def __init__(self):
        self.interference = {}
        self.live = [Set()]
        self.names = Set()
        self.spillTmp = 0
        self.priority = Set()
        self.registerColors = {0:"eax", 1:"ebx", 2:"ecx", 3:"edx", 4:"esi",5:"edi"}
        self.maxcolor=0
        self.iterations =0
        self.inputLookup = {}
        self.argLookup = {}
        self.finalString = ""

    def resetGraph(self):
        self.interference = {}
        self.live = [Set()]
        self.names = Set()
        self.maxcolor=0
        self.inputLookup = {}

    def getConstOrName(self, op):
        if isinstance(op,ConstOp):
            return op.value
        elif isinstance(op,NameOp):
            return op.name
        else:
            print "Not Const or Name"

    def createLiveness(self, x86code):
        labels = {}
        whileLineNums = {}
        count = 0
        x86reversed = x86code[::-1]
        #for line in reversed(x86code):
        while count <len(x86code):
            
            line = x86reversed[count]
            if len(self.live)==count+1:
                self.live.append(self.live[count].copy())
            else:
                self.live[count+1]=self.live[count].copy()
            count += 1
            #print "Count",count, self.live[1]
            if isinstance(line, BinaryOp):
                if line.name == "addl":
                    if isinstance(line.src, NameOp):
                        self.live[count].add(line.src.name)
                    if isinstance(line.dest, NameOp):
                        self.live[count].add(line.dest.name)
                elif line.name == "movl" or line.name == "cmove":
                    if isinstance(line.dest, NameOp):
                        self.live[count] = self.live[count] - Set([line.dest.name])
                    if isinstance(line.src, NameOp):
                        self.live[count].add(line.src.name)
                    if line.name == "cmove":
                        self.priority.add(line.dest.name)
                elif line.name == "cmp":
                    if isinstance(line.dest, NameOp):
                        self.live[count].add(line.dest.name)
                    if isinstance(line.src, NameOp):
                        self.live[count].add(line.src.name)
                elif line.name == "sarl":
                    if isinstance(line.dest, NameOp):
                        self.live[count].add(line.dest.name)
                    if isinstance(line.src, NameOp):
                        self.live[count].add(line.src.name)
                elif line.name == "andl":
                    if isinstance(line.dest, NameOp):
                        self.live[count].add(line.dest.name)
                    if isinstance(line.src, NameOp):
                        self.live[count].add(line.src.name)
                else:
                    print "Unsupported Binary Live"
            elif isinstance(line, UnaryOp):
                if line.name == "negl":
                    if isinstance(line.param, NameOp):
                        self.live[count].add(line.param.name)
                elif line.name == "notl":
                    if isinstance(line.param, NameOp):
                        self.live[count].add(line.param.name)
                else:
                    print "Unsupported Unary Live"
            elif isinstance(line, PrintOp):
                if isinstance(line.name, NameOp):
                    self.live[count].add(line.name.name)
                else:
                    print "Unsupported Print Live"
            elif isinstance(line,FuncOp):
                #print line.var
                if line.star == '*':
                    self.live[count].add(line.name.name)
                if line.var.name != "*void":
                    self.live[count] -= Set([line.var.name])
                for arg in line.args:
                    if isinstance(arg,NameOp):
                        self.live[count].add(arg.name)
            elif isinstance(line,JumpOp):
                #if line.label re.sub("^while")
                if not labels.has_key(line.label.name) or whileLineNums.has_key(line.label.name) : #while loop, needs to repeat
                    labels[line.label.name]= self.live[count].copy()
                    whileLineNums[line.label.name] = count
                else:
                    if line.name == "jmp":
                        self.live[count] = labels[line.label.name]
                    else:
                        self.live[count] = self.live[count] | labels[line.label.name]

            elif isinstance(line,ClauseOp):
                if whileLineNums.has_key(line.label.name):
                    #print "yoyoyoyo"
                    #print self.live[count]
                    #print labels[line.label.name]
                    if self.live[count]== labels[line.label.name]:
                        #print "winner is you"
                        pass
                    else:
                        labels[line.label.name] = self.live[count].copy()
                        #print "label says ", labels[line.label.name]
                        count = whileLineNums[line.label.name]
                        #print x86reversed[count], count
                        self.live[count] = labels[line.label.name].copy()
                else:
                    labels[line.label.name]= self.live[count].copy()
            elif isinstance(line,ReturnOp):
                if isinstance(line.ret, NameOp):
                    self.live[count] = Set([line.ret.name])
                else:
                    self.live[count] = Set()

            elif isinstance(line,FuncStartOp):
                self.live[count] = Set()

            elif isinstance(line,EndOp):
                self.live[count] = Set()

            else:
                print "missing liveness",line
        self.live.reverse()
        self.live = self.live[1:]
        return self.createInterferenceGraph(x86code)

    def createInterferenceGraph(self, x86code):
        def addEdge(src,dest):
            if src == "" or dest == "":
                print "************"
            if not self.interference.has_key(src):
                self.interference[src] = Set([])
            self.interference[src].add(dest)
            if not self.interference.has_key(dest):
                self.interference[dest] = Set([])
            self.interference[dest].add(src)

        self.interference['^eax'] = Set([])
        self.interference['^ecx'] = Set([])
        self.interference['^edx'] = Set([])
        somelen = len(x86code)
        for count in range(0,somelen):
            #print x86code[count],self.live[count]
            if isinstance(x86code[count], BinaryOp):
                if isinstance(x86code[count].dest,ConstOp):
                    t = ""
                else:
                    t = x86code[count].dest.name
                s = ""
                if isinstance(x86code[count].src, NameOp):
                    s = x86code[count].src.name
                if t and not self.interference.has_key(t):
                    self.interference[t] = Set([])
                if s and not self.interference.has_key(s):
                    self.interference[s] = Set([])
                for var in self.live[count]:
                    if x86code[count].name == "movl" or x86code[count].name == "cmove":
                        if var != t and var != s:
                            addEdge(t,var)
                    elif x86code[count].name == "addl":
                        if var != t:
                            addEdge(t,var)
                    elif x86code[count].name == "cmp":
                        if t and var !=t:
                            addEdge(t,var)
                        if s and var !=s:
                            addEdge(s,var)
                    elif x86code[count].name == "sarl":
                        if var != t:
                            addEdge(t,var)
                    elif x86code[count].name == "andl": #should force to use eax
                        if var != t:
                            addEdge(t,var)
                            addEdge('^eax',var)
                    else:
                        print "Unsuported Binary interference"

            elif isinstance(x86code[count], PrintOp):
                callerSave = ['^eax', '^ecx', '^edx']
                for r in callerSave:
                    addEdge(x86code[count].name.name,r)
                    for var in self.live[count]:
                        addEdge(r,var)
            elif isinstance(x86code[count], UnaryOp):
                t = x86code[count].param.name
                if not self.interference.has_key(t):
                    self.interference[t] = Set([])
                for var in self.live[count]:
                    if var!= t:
                        addEdge(t,var)
            elif isinstance(x86code[count], FuncOp): #needs possibly unnecessary extra edges, #for voids, treat as *void
                callerSave = ['^eax', '^ecx', '^edx']
                t= x86code[count].var.name
                if t!= "*void" and not self.interference.has_key(t):
                    self.interference[t] = Set([])
                for r in callerSave:
                    for var in self.live[count]:
                        if t== "*void" or var != t:
                            addEdge(r,var)
                for arg in x86code[count].args:
                    if isinstance(arg,NameOp):
                        for var in self.live[count]:
                            if var != arg.name:
                                addEdge(arg.name,var)
                        for r in callerSave:
                            if t== "*void" or arg.name != t:
                                addEdge(arg.name,r)
                if t!= "*void":
                    for var in self.live[count]:
                        if var != t:
                            addEdge(t,var)
                if x86code[count].star == '*':
                    for var in self.live[count]:
                        if var != x86code[count].name.name:
                            addEdge(x86code[count].name.name,var)
            elif isinstance(x86code[count], ReturnOp):
                if isinstance(x86code[count].ret, NameOp):
                    if not self.interference.has_key(x86code[count].ret.name):
                        self.interference[x86code[count].ret.name]= Set([])
            elif isinstance(x86code[count], FuncStartOp):
                pass
            elif isinstance(x86code[count], EndOp):
                pass
            else:
                #print "interference",x86code[count] 
                pass
        #pprint(self.interference)
        return self.colorGraph(x86code);

    def colorGraph(self, x86code):
        color = {}
        saturation ={}
        color["^eax"]= 0
        color["^ecx"] = 2
        color["^edx"] = 3
        for node in self.interference:
            saturation[node] = 0
        for c in color:
            for node in self.interference[c]:
                saturation[node]+=1

        uncolored = Set()
        for node in self.interference:
            #print node
            if node[0]!='^':
                uncolored.add(node)
        while len(uncolored):
            curNode = self.findMax(uncolored,saturation)

            neighbors = self.interference[curNode]

            sortedNeighbors = map(lambda e: color[e] if color.has_key(e) else -1, neighbors)
            if len(sortedNeighbors)==0:
                color[curNode]=0
            else:
                coolList = [0]*(max(sortedNeighbors)+1+1)
                for el in sortedNeighbors:

                    if el>-1:
                        coolList[el]=1
                for i in range(0, len(coolList)):
                    if coolList[i]==0:
                        color[curNode] = i
                        if i>self.maxcolor:
                            self.maxcolor=i
                        break

            for node in self.interference[curNode]:
                saturation[node]+=1
            uncolored.remove(curNode)

        return self.cleanUpCrew(x86code,color)


    def findMax(self, uncolored, saturation):
        maxSat = 0
        maxNode = list(uncolored)[0]
        for node in uncolored:
            if node in self.priority:
                return node
            if saturation[node]>maxSat:
                maxSat = saturation[node]
                maxNode = node
        return maxNode

    def cleanUpCrew(self, x86code, color):
        x86revision = []
        spillage = False
        x86colored = []
        def getRegVal(param):
            if isinstance(param, NameOp):
                if self.argLookup.has_key(param.name):
                    return NameOp(77)
                if param.name not in color:
                    return -1
                colorId =color[param.name]
                return NameOp(colorId)
            elif isinstance(param, ConstOp):
                return param

        for line in x86code:
            if isinstance(line, BinaryOp):
                coloredSrc = getRegVal(line.src)
                coloredDest =getRegVal(line.dest)
                if coloredDest==-1: #removed useless unreferenced variables
                    continue
                if line.name == "cmove":
                    if coloredSrc.name>5:
                        print line
                        print "Error on left cmove"
                        #Shouldn't come up
                    if coloredDest.name>5:
                        newTmp = "temp %d" %self.spillTmp
                        x86revision.append(BinaryOp("movl", line.dest,NameOp(newTmp)))
                        x86revision.append(BinaryOp(line.name, line.src,NameOp(newTmp)))
                        x86revision.append(BinaryOp("movl", NameOp(newTmp), line.dest))
                        self.priority.add(newTmp)
                        self.spillTmp +=1
                        #print "spill here"
                        spillage = True
                    else:
                        x86revision.append(line)
                        x86colored.append(BinaryOp(line.name, coloredSrc, coloredDest))
                elif isinstance(coloredSrc, NameOp) and coloredSrc.name>5 and isinstance(coloredDest,NameOp) and coloredDest.name>5:
                    newTmp = "temp %d" %self.spillTmp
                    x86revision.append(BinaryOp("movl", line.src,NameOp(newTmp)))
                    x86revision.append(BinaryOp(line.name, NameOp(newTmp), line.dest))
                    self.priority.add(newTmp)
                    self.spillTmp +=1
                    spillage = True
                else:
                    x86revision.append(line)
                    x86colored.append(BinaryOp(line.name, coloredSrc, coloredDest))
            elif isinstance(line, UnaryOp):
                x86revision.append(line)
                x86colored.append(UnaryOp(line.name, getRegVal(line.param)))
            elif isinstance(line, PrintOp):
                x86revision.append(line)
                x86colored.append(PrintOp(getRegVal(line.name)))
            elif isinstance(line, FuncOp):
                x86revision.append(line)
                x86colored.append(FuncOp(line.name, line.args, line.var,line.star))
            elif isinstance(line,JumpOp):
                x86revision.append(line)
                x86colored.append(JumpOp(line.name,line.label))
            elif isinstance(line,ClauseOp):
                x86revision.append(line)
                x86colored.append(ClauseOp(line.label))
            elif isinstance(line,ReturnOp):
                x86revision.append(line)
                x86colored.append(ReturnOp(line.ret))
            elif isinstance(line,FuncStartOp):
                revision = FuncStartOp(line.name,line.args)
                x86revision.append(revision)
                # for index,arg in enumerate(line.args):
                #     curArg = getRegVal(arg)
                #     if isinstance(curArg,NameOp) and curArg.name>5:
                #         spillage = True
                #         newTmp = "temp %d" %self.spillTmp
                #         self.spillTmp +=1
                #         revision.args[index] = NameOp(newTmp)
                #         self.priority.add(newTmp)
                #         x86revision.append(BinaryOp("movl", NameOp(newTmp),arg))

                #x86colored.append(FuncStartOp(line.name, line.args))

            elif isinstance(line,EndOp):
                x86revision.append(line)
                x86colored.append(EndOp())
            else:
                print "Unnaccounted for Type",line

        # print x86colored
        #for line in x86colored:
        #   print repr(line)
        # print "*****"
        # for line in x86revision:
        #     print line

        if spillage:
            self.resetGraph()
            self.iterations+=1
            if self.iterations>20:
                return ""
            else:
                return self.createLiveness(x86revision)

        else:
            return self.prettyPrint(x86revision,color)

    def getArg(self, name,color):
        if isinstance(name, NameOp):
            if self.argLookup.has_key(name.name):
                stackId = self.argLookup[name.name]
                #del self.argLookup[name.name]
                if 1:#color[name.name] >5:
                    self.inputLookup[name.name] = "%d(%%ebp)" % stackId
                    return self.inputLookup[name.name]
                else:
                    print "here"
                    del self.argLookup[name.name]
                    otherArg = self.getArg(name,color)
                    #self.argLookup[name.name] = stackId
                    self.finalString+="\tmovl %d(%%ebp), %s\n" %(stackId, otherArg)
                    return otherArg

            if self.inputLookup.has_key(name.name):
                return self.inputLookup[name.name]
            colorid = color[name.name]
            if colorid>5:
                return "-%d(%%ebp)"%((colorid-5)*4)
            else:
                return "%" + self.registerColors[colorid]
        elif isinstance(name,LabelOp):
            return "$%s"% name.name
        else:
            return "$%d"% name.value

    def prettyPrint(self,x86revision,color):

        #print color
        #self.finalString = ""
        for line in x86revision:
            if isinstance(line, FuncOp):
                if line.star == '*':
                    self.finalString+="\tpushl %ebx\n"
                    self.finalString+="\tpushl %esi\n"
                    self.finalString+="\tpushl %edi\n"
                for arg in reversed(line.args):
                    curArg =self.getArg(arg,color)
                    self.finalString+="\tpushl %s\n" % (curArg)
                if line.star == '*':
                    self.finalString+="\tcall *%s\n" % self.getArg(line.name,color)
                else:
                    self.finalString+="\tcall %s\n" % str(line.name)
                
                self.finalString+="\taddl $%d, %%esp\n" %(4*len(line.args))
                if line.star == '*':
                    self.finalString+="\tpopl %edi\n"
                    self.finalString+="\tpopl %esi\n"
                    self.finalString+="\tpopl %ebx\n"
                if not line.var.name =="*void":
                    self.finalString+="\tmovl %%eax,%s\n"% (self.getArg(line.var,color))
                
            elif isinstance(line, PrintOp):
                arg = self.getArg(line.name, color)
                self.finalString+="\tpushl %s\n" % arg
                self.finalString+="\tcall print_any\n"
                self.finalString+="\tpopl %s\n" % arg
            elif isinstance(line, BinaryOp):
                leftArg = self.getArg(line.src, color)
                stepString = self.finalString
                rightArg = self.getArg(line.dest, color)
                self.finalString=stepString

                self.finalString+="\t%s %s, %s\n" %(line.name, leftArg,rightArg)

            elif isinstance(line,UnaryOp):
                self.finalString+="\t%s %s\n" %(line.name, self.getArg(line.param, color))
            elif isinstance(line,JumpOp):
                self.finalString+="\t%s\n" % str(line)
            elif isinstance(line,ClauseOp):
                self.finalString+="\t%s\n" % str(line)
            elif isinstance(line,ReturnOp):
                self.finalString+= "\tmovl %s, %%eax\n" % self.getArg(line.ret,color)
                self.finalString+=("\tleave\n")
                self.finalString+=("\tret\n")   
            elif isinstance(line,EndOp):
                self.finalString+=("\tmovl $0,%eax\n")
                self.finalString+=("\tleave\n")
                self.finalString+=("\tret\n")
            elif isinstance(line,FuncStartOp):
                self.finalString+=("%s:\n") % line.name
                self.finalString+=("\tpushl %ebp\n")
                self.finalString+=("\tmovl %esp, %ebp\n")
                if self.maxcolor <6:
                    self.maxcolor = 0
                else:
                    self.finalString+=("\tsubl $%d, %%esp\n") % ((self.maxcolor-5)*4)
                for index,arg in enumerate(line.args):
                    if color.has_key(arg.name):
                        #self.finalString+="\tmovl %d(%%ebp), %s\n" %(index*4+8, self.getArg(arg,color))
                        #print "\tmovl %d(%%ebp), %s\n" %(index*4+8, self.getArg(arg,color))
                        pass
            else:
                print "Unnaccounted Print", line

        
       
        #finalString = header+finalString
        return self.finalString
