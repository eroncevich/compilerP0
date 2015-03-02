from sets import Set
from pprint import pprint

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
    def __init__(self, name, args, var):
        self.name = name
        self.args = args
        self.var = var
    def __repr__(self):
        return "FuncOp(%s,%s,%s)" % (self.name, self.args, self.var)
    def __str__(self):
        return "call %s %s -> %s" % (str(self.name),[str(arg) for arg in self.args], str(self.var))

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
        count = 0
        for line in reversed(x86code):
            self.live.append(self.live[count].copy())
            count += 1
            if isinstance(line, BinaryOp):
                if line.name == "addl":
                    if isinstance(line.src, NameOp):
                        self.live[count].add(line.src.name)
                    if isinstance(line.dest, NameOp):
                        self.live[count].add(line.dest.name)
                elif line.name == "movl":
                    if isinstance(line.dest, NameOp):
                        self.live[count] = self.live[count] - Set([line.dest.name])
                    if isinstance(line.src, NameOp):
                        self.live[count].add(line.src.name)
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
                self.live[count] -= Set([line.var.name])
                for arg in line.args:
                    if isinstance(arg,NameOp):
                        self.live[count].add(arg.name)
            elif isinstance(line,JumpOp):
                if line.name == "jmp":
                    self.live[count] = labels[line.label.name]
                else:
                    self.live[count] = self.live[count] | labels[line.label.name]

            elif isinstance(line,ClauseOp):
                labels[line.label.name]= self.live[count].copy()

            else:
                print "missing liveness",line
        self.live.reverse()
        self.live = self.live[1:]
        return self.createInterferenceGraph(x86code)

    def createInterferenceGraph(self, x86code):
        def addEdge(src,dest):
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
            print x86code[count],self.live[count]
            if isinstance(x86code[count], BinaryOp):
                if isinstance(x86code[count].dest,ConstOp):
                    t = ""
                else:
                    t = x86code[count].dest.name
                s = ""
                if isinstance(x86code[count].src, NameOp):
                    s = x86code[count].src.name
                if not self.interference.has_key(t):
                    self.interference[t] = Set([])
                for var in self.live[count]:
                    if x86code[count].name == "movl":
                        if var != t and var != s:# and t in line:
                            addEdge(t,var)
                    elif x86code[count].name == "addl":
                        if var != t:# and t in line:
                            addEdge(t,var)
                    elif x86code[count].name == "cmp":
                        if t and var !=t:
                            addEdge(t,var)
                        if s and var !=s:
                            addEdge(s,var)
                    elif x86code[count].name == "sarl":
                        if var != t:
                            addEdge(t,var)
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
            elif isinstance(x86code[count], FuncOp): #need to check
                callerSave = ['^eax', '^ecx', '^edx']
                for r in callerSave:
                    for var in self.live[count]:
                        addEdge(r,var)
                for arg in x86code[count].args:
                    if isinstance(arg,NameOp):
                        for var in self.live[count]:
                            if var != arg.name:
                                addEdge(arg.name,var)
                        for r in callerSave:
                            addEdge(arg.name,r)
                for var in self.live[count]:
                    if var != x86code[count].var.name:
                        addEdge(x86code[count].var.name,var)
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
                        break

            for node in self.interference[curNode]:
                saturation[node]+=1
            uncolored.remove(curNode)

        #print color
        #print saturation
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
                if isinstance(coloredSrc, NameOp) and coloredSrc.name>5 and isinstance(coloredDest,NameOp) and coloredDest.name>5:
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
                x86colored.append(FuncOp(line.name, line.args, line.var))
            elif isinstance(line,JumpOp):
                x86revision.append(line)
                x86colored.append(JumpOp(line.name,line.label))
            elif isinstance(line,ClauseOp):
                x86revision.append(line)
                x86colored.append(ClauseOp(line.label))
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
            if self.iterations>8:
                return ""
            else:
                return self.createLiveness(x86revision)

        else:
            return self.prettyPrint(x86revision,color)

    def getArg(self, name,color):
        if isinstance(name, NameOp):
            if self.inputLookup.has_key(name.name):
                return self.inputLookup[name.name]
            colorid = color[name.name]
            if colorid>5:
                if colorid>self.maxcolor:
                    self.maxcolor=colorid
                return "-%d(%%ebp)"%((colorid-5)*4)
            else:
                return "%" + self.registerColors[colorid]
        else:
            return "$%d"% name.value

    def prettyPrint(self,x86revision,color):
        #print color
        finalString = ""
        for line in x86revision:
            if isinstance(line, FuncOp):
                for arg in reversed(line.args):
                    finalString+="\tpushl %s\n" % (self.getArg(arg,color))
                #self.inputLookup[line.var] = '%eax'
                finalString+="\tcall %s\n" % str(line.name)
                finalString+="\tmovl %%eax,%s\n"% (self.getArg(line.var,color))
                finalString+="\taddl $%d, %%esp\n" %(4*len(line.args))
            elif isinstance(line, PrintOp):
                arg = self.getArg(line.name, color)
                finalString+="\tpushl %s\n" % arg
                finalString+="\tcall print_any\n"
                finalString+="\tpopl %s\n" % arg
            elif isinstance(line, BinaryOp):
                leftArg = self.getArg(line.src, color)
                rightArg = self.getArg(line.dest, color)
                #if line.name == "movl" and rightArg == leftArg:
                #    continue
                #else:
                    #print line.src.name, line.dest
                finalString+="\t%s %s, %s\n" %(line.name, leftArg,rightArg)

            elif isinstance(line,UnaryOp):
                finalString+="\t%s %s\n" %(line.name, self.getArg(line.param, color))
            elif isinstance(line,JumpOp):
                finalString+="\t%s\n" % str(line)
            elif isinstance(line,ClauseOp):
                finalString+="\t%s\n" % str(line)
            else:
                print "Unnaccounted Print", line

        header=(".globl main\nmain:\n")
        header+=("\tpushl %ebp\n")
        header+=("\tmovl %esp, %ebp\n")
        if self.maxcolor <6:
            self.maxcolor = 0
        else:
            header+=("\tsubl $%d, %%esp\n") % ((self.maxcolor-5)*4)
        finalString = header+finalString
        finalString+=("\tmovl $0,%eax\n")
        finalString+=("\tleave\n")
        finalString+=("\tret\n")
        return finalString
