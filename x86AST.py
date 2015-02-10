# class Module(Node):
#     def __init__(self, doc, node):
#         self.doc = doc
#         self.node = node

# class Stmt(Node):
#     def __init__(self, nodes):
#         self.nodes = nodes
# class Printnl(Node):
#     def __init__(self, nodes, dest):
#         self.nodes = nodes
#         self.dest = dest
# class Assign(Node):
#     def __init__(self, nodes, expr):
#         self.nodes = nodes
#         self.expr = expr
# class AssName(Node):
#     def __init__(self, name, flags):
#         self.name = name
#         self.flags = flags
# class Discard(Node):
#     def __init__(self, expr):
#         self.expr = expr
# class Const(Node):
#     def __init__(self, value):
#         self.value = value
# class Name(Node):
#     def __init__(self, name):
#         self.name = name
# class Add(Node):
#     def __init__(self, (left, right)):
#         self.left = left
#         self.right = right
# class UnarySub(Node):
#     def __init__(self, expr):
#         self.expr = expr
# class CallFunc(Node):
#     def __init__(self, node, args):
#         self.node = node
#         self.args = args

class Node(object):
    def __init__(self):
        pass

class Memory(Node):
    def __init__(self, position):
        self.position = position
    def __repr__(self):
        return "Memory(-%d)" % self.position
    def __str__(self):
        return "-%d(%%ebp)" % self.position

class Register(Node):
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return "Register(%d)" % self.name
    def __str__(self):
        return "%%%s" % self.name

class Constant(Node):
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return "Constant(%d)" % self.value
    def __str__(self):
        return "$%d" % self.value

class BinaryInstruction(Node):
    def __init__(self, name, src, dest):
        self.name = name
        self.src = src
        self.dest = dest
    def __repr__(self):
        return "BinaryInstruction(%s, %s, %s)" % (self.name, repr(self.src), repr(self.dest))
    def __str__(self):
        return "%s %s, %s" % (self.name, str(self.src), str(self.dest))

class UnaryInstruction(Node):
    def __init__(self, name, dest):
        self.name = name
        self.dest = dest
    def __repr__(self):
        return "UnaryInstruction(%s, %s)" % (self.name, repr(self.dest))
    def __str__(self):
        return "%s %s" % (self.name, str(self.dest))
