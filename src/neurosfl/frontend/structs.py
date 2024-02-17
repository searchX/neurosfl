# Represents classes for the tree, this will be later used by backend to parse and generate code

class Node:
    """Base class for all nodes
    """
    def __init__(self):
        pass

class StartNode(Node):
    """Start node for the tree (used to mark the start of the tree)
    """
    def __init__(self, data):
        self.data = data

    def __str__(self) -> str:
        return str(self.data)

class UnaryOp(Node):
    """Unary operation node (Not used in the current implementation, but can be used in future for negation etc.)
    """
    def __init__(self, op, expr):
        self.op = op
        self.expr = expr

    def __str__(self) -> str:
        return f"{self.op} {self.expr}"

class BinaryOp(Node):
    """Binary operation node, used for logical and comparison operations
    """
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def __str__(self) -> str:
        return f"({self.left} {self.op} {self.right})"

class LogicalOp(BinaryOp):
    """Logical operation node
    """
    def __init__(self, left, op, right):
        super().__init__(left, op, right)

    def __str__(self) -> str:
        return f"({self.left} {self.op} {self.right})"
    
class ComparisonOp(BinaryOp):
    """Comparison operation node
    """
    def __init__(self, left, op, right):
        super().__init__(left, op, right)

    def __str__(self) -> str:
        return f"_({self.left} {self.op} {self.right})"

class StringLiteral(Node):
    """String literal node, represents a string value
    """
    def __init__(self, value):
        self.value = value

    def __str__(self) -> str:
        return f"{self.value}"

class NumberLiteral(Node):
    """Number literal node represents a number value
    """
    def __init__(self, value):
        self.value = value

    def __str__(self) -> str:
        return f"{self.value}"