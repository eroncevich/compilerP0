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
    self.active = {}
    self.live = [Set()]
    self.names = Set()

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
    return self.live

  def createInterferenceGraph(self, x86code):
      for count in range(0,len(x86code)):
          if isinstance(x86code[count], BinaryOp):
              if x86code[count].name == "movl":
                  self.active[x86code[count].dest.name].add(self.live[count][0])
                  #create edge from u,t
                  #create edge from t,u
          #print x86code[count],self.live[count]
          print self.active
