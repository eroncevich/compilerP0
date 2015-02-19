from sets import Set


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
    def __init__(self, name, var):
        self.name = name
        self.var = var
    def __repr__(self):
        return "FuncOp(%s,%s)" % (self.name, self.var)
    def __str__(self):
        return "call %s" % self.name

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

    def createLiveness(self, x86code):
        count = 0
        for line in reversed(x86code):
            self.live.append(self.live[count].copy())
            count += 1
            if isinstance(line, BinaryOp):
                if line.name == "addl":
                    if isinstance(line.src, NameOp):
                        self.live[count].add(line.src.name)
                        #self.names.add(line.src.name)
                    if isinstance(line.dest, NameOp):
                        self.live[count].add(line.dest.name)
                if line.name == "movl":
                    if isinstance(line.src, NameOp):
                        self.live[count].add(line.src.name)
                    if isinstance(line.dest, NameOp):
                        self.live[count] = self.live[count] - Set([line.dest.name])
            if isinstance(line, UnaryOp):
                if line.name == "negl":
                    if isinstance(line.param, NameOp):
                        self.live[count].add(line.param.name)
            if isinstance(line, PrintOp):
                if isinstance(line.name, NameOp):
                    self.live[count].add(line.name.name)
        self.live.reverse()
        self.live = self.live[1:]
        #print "liveness"
        return self.createInterferenceGraph(x86code)
        #return self.live

    def createInterferenceGraph(self, x86code):
        def addEdge(src,dest):
            #if not self.interference.has_key(src):
            #    self.interference[src] = Set([])
            self.interference[src].add(dest)
            if not self.interference.has_key(dest):
                self.interference[dest] = Set([])
            self.interference[dest].add(src)

        self.interference['^eax'] = Set([])
        self.interference['^ecx'] = Set([])
        self.interference['^edx'] = Set([])
        somelen = len(x86code)
        for count in range(0,somelen):
            #print "0"
            #print x86code[count],self.live[count]
            if isinstance(x86code[count], BinaryOp):

                t = x86code[count].dest.name
                s = ""
                if isinstance(x86code[count].src, NameOp):
                    s = x86code[count].src.name
                if not self.interference.has_key(t):
                    self.interference[t] = Set([])
                #line = self.live[count]
                for var in self.live[count]:
                    if x86code[count].name == "movl":
                        if var != t and var != s:# and t in line:
                            addEdge(t,var)
                    elif x86code[count].name == "addl":
                        if var != t and t:# in line:
                            addEdge(t,var)

            if isinstance(x86code[count], PrintOp):
                #for line in self.live[count:]:
                #print x86code[count], self.live[count]
                callerSave = ['^eax', '^ecx', '^edx']
                for r in callerSave:
                    addEdge(x86code[count].name.name,r)
                    for var in self.live[count]:
                        addEdge(r,var)
            if isinstance(x86code[count], UnaryOp):
                #print"2"
                t = x86code[count].param.name
                if not self.interference.has_key(t):
                    self.interference[t] = Set([])
                #for line in self.live[count:]:
                for var in self.live[count]:
                    if var!= t:
                        addEdge(t,var)
                #print"3"
            if isinstance(x86code[count], FuncOp): #need to check
                #print "2"

                #for line in self.live[count:]:
                callerSave = ['^eax', '^ecx', '^edx']
                for r in callerSave:
                    for var in self.live[count]:
                        addEdge(r,var)
              #print "3"
            #print "1"
        #print self.interference
        #print "interference"
        return self.colorGraph(x86code);

    def colorGraph(self, x86code):
        #print self.interference
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
        #print "uncolored", uncolored
        while len(uncolored):
            curNode = self.findMax(uncolored,saturation)

            neighbors = self.interference[curNode]
            #print neighbors

            sortedNeighbors = map(lambda e: color[e] if color.has_key(e) else -1, neighbors)
            #sortedNeighbors.sort()
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
            #print color[curNode]



            #while len(sortedNeighbors) > 0 and sortedNeighbors[0] == -1:
            #    sortedNeighbors = sortedNeighbors[1:]
            #counter = 0
            #for el in sortedNeighbors:
            #    if counter == el:
            #        counter+=1
            #    elif counter< el:
            #        break
            #color[curNode] = counter
            for node in self.interference[curNode]:
                saturation[node]+=1
            uncolored.remove(curNode)



        #print color
        #print saturation
        #print uncolored
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
        #print color
        def getRegVal(param):
            if isinstance(param, NameOp):
                if param.name not in color:
                    return -1
                colorId =color[param.name]
                #if colorId>5:
                #    print "spillage"
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
                #if x86.colored[-1].src
            elif isinstance(line, UnaryOp):
                x86revision.append(line)
                x86colored.append(UnaryOp(line.name, getRegVal(line.param)))
            elif isinstance(line, PrintOp):
                x86revision.append(line)
                x86colored.append(PrintOp(getRegVal(line.name)))
            elif isinstance(line, FuncOp):
                x86revision.append(line)
                x86colored.append(FuncOp("input", line.var))
            else:
                print "Unnaccounted for Type"
            #x86colored.append(line)

        # print x86colored
        # for line in x86colored:
        #     print repr(line)
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
            #if not color.has_key(name.name):
            #    colorid = 0
            #else:
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
        finalString = ""
        for line in x86revision:
            if isinstance(line, FuncOp):
                self.inputLookup[line.var] = '%eax'
                finalString+="\tpushl %eax\n\tcall input\n"
            elif isinstance(line, PrintOp):
                arg = self.getArg(line.name, color)
                finalString+="\tpushl %s\n" % arg
                finalString+="\tcall print_int_nl\n"
                finalString+="\tpopl %s\n" % arg
            elif isinstance(line, BinaryOp):
                finalString+="\t%s %s, %s\n" %(line.name, self.getArg(line.src, color),self.getArg(line.dest, color))
            elif isinstance(line,UnaryOp):
                finalString+="\t%s %s\n" %(line.name, self.getArg(line.param, color))

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
