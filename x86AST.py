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
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return "FuncOp(%s)" % self.name
    def __str__(self):
        return "call %s" % self.name

class PrintOp(Node):
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return "PrintOp(%s)" % self.name
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
        self.registerColors = {"eax":0, "ebx":1, "ecx":2, "edx":3, "esi":4,"edi":5}

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
        self.createInterferenceGraph(x86code)
        #return self.live

    def createInterferenceGraph(self, x86code):
        for count in range(0,len(x86code)):
            print x86code[count],self.live[count]
            if isinstance(x86code[count], BinaryOp):
                t = x86code[count].dest.name
                s = ""
                if isinstance(x86code[count].src, NameOp):
                    s = x86code[count].src.name
                if not self.interference.has_key(t):
                    self.interference[t] = Set([])
                for line in self.live[count:]:
                    for var in line:
                        if x86code[count].name == "movl":
                            if var != t and var != s and t in line:
                                self.interference[t].add(var)
                        elif x86code[count].name == "addl":
                            if var != t and t in line:
                                self.interference[t].add(var)
            if isinstance(x86code[count], PrintOp):
                if not self.interference.has_key('^eax'):
                    self.interference['^eax'] = Set([])
                    self.interference['^ecx'] = Set([])
                    self.interference['^edx'] = Set([])
                for line in self.live[count:]:
                    callerSave = ['^eax', '^ecx', '^edx']
                    for r in callerSave:
                        for var in line:
                            self.interference[r].add(var)
                            self.interference[var].add(r)
            if isinstance(x86code[count], UnaryOp):
                t = x86code[count].param.name
                if not self.interference.has_key(t):
                    self.interference[t] = Set([])
                for line in self.live[count:]:
                    for var in line:
                        if var!= t and t in line:
                            self.interference[t].add(var)

            #TODO: Need to add the third case (call label)
        print self.interference
    def colorGraph(self):
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
            sortedNeighbors.sort()
            #print sortedNeighbors

            while len(sortedNeighbors) > 0 and sortedNeighbors[0] == -1:
                sortedNeighbors = sortedNeighbors[1:]
            counter = 0
            for el in sortedNeighbors:
                if counter == el:
                    counter+=1
                elif counter< el:
                    break
            color[curNode] = counter
            for node in self.interference[curNode]:
                saturation[node]+=1
            uncolored.remove(curNode)



        print color
        print saturation
        print uncolored
        return color


    def findMax(self, uncolored, saturation):
        maxSat = 0
        maxNode = list(uncolored)[0]
        for node in uncolored:
            if saturation[node]>maxSat:
                maxSat = saturation[node]
                maxNode = node
        return maxNode

    def cleanUpCrew(self, x86code, color):
        def getRegVal(param):
            if isinstance(param, NameOp):
                colorId =color[param.name]
                #if colorId<6:
                #    return NameOp(self.registerColors[colorId])
                #else:
                return NameOp(colorId)
            elif isinstance(param, ConstOp):
                return param
        x86colored = []
        for line in x86code:
            if isinstance(line, BinaryOp):
                x86colored.append(BinaryOp(line.name, getRegVal(line.src), getRegVal(line.dest)))
            if isinstance(line, UnaryOp):
                x86colored.append(UnaryOp(line.name, getRegVal(line.param)))
            if isinstance(line, PrintOp):
                pass
            #x86colored.append(line)
        print x86colored
