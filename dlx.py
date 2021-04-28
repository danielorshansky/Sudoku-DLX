import math

class Node: # a node in a circular quadruply linked list
    def __init__(self, header = None):
        self.left = self.right = self
        self.up = self.down = self
        self.column = self.row = None
        self.header = header if header else self

class Header(Node): # a header node for each column
    def __init__(self):
        super().__init__()
        self.count = 0 # the number of nodes with a value of 1
    
    def cover(self):
        self.left.right = self.right
        self.right.left = self.left
        node = self.down
        while node != self:
            node.left.right = node.right
            node.right.left = node.left
            node = node.down
    
    def uncover(self):
        self.left.right = self
        self.right.left = self
        node = self.down
        while node != self:
            node.left.right = node
            node.right.left = node
            node = node.down

class DLX:
    def __init__(self):
        self.root = Header()
    
    def create_links(board, n): # pass the board and size of n x n sudoku
        box_size = math.sqrt(n)
        headers = [Header() for _ in range(n ** 2 * 4)]
        for header in headers:
            header.right = self.root
            header.left = self.root.left
            self.root.left.right = header
            self.root.left = header
        
        for row in range(n):
            for column in range(n):
                value = board[row][column]
                if value != 0: # if the value is set, create the appropriate constraints for its position and value
                    cell = Node(headers[n * row + column]) # node for the row-column constraint
                    row = Node(headers[n ** 2 + row * n + value - 1]) # node for the row-number constraint
                    column = Node(headers[n ** 2 * 2 + column * n + value - 1]) # node for the column-number constraint
                    box = Node(headers[n ** 2 * 3 + (row // box_size * box_size + column // box_size) * n + value - 1]) # node for the box-number constraint
                    nodes = [cell, row, column, box]
                    for index, node in enumerate(nodes):
                        node.right = nodes[index + 1] # link nodes to each other
                        node.left = nodes[index - 1]
                        node.header.count += 1 # add one to the count of the header
                        node.up = node.header.up # link to nodes in the column
                        node.down = node.header
                        node.header.up.down = node
                        node.header.up = node
                else: # if the value is not set, create all the constraints for its position
                    for x in range(n): # loop through all possible values
                        cell = Node(headers[n * row + column]) # nodes for the row-column constraints
                        row = Node(headers[n ** 2 + row * n + x]) # nodes for the row-number constraints
                        column = Node(headers[n ** 2 * 2 + column * n + x]) # nodes for the column-number constraints
                        box = Node(headers[n ** 2 * 3 + (row // box_size * box_size + column // box_size) * n + x]) # nodes for the box-number constraints
                        nodes = [cell, row, column, box]
                        for index, node in enumerate(nodes):
                            node.right = nodes[index + 1] # link nodes to each other
                            node.left = nodes[index - 1]
                            node.header.count += 1 # add one to the count of the header
                            node.up = node.header.up # link to nodes in the column
                            node.down = node.header
                            node.header.up.down = node
                            node.header.up = node
        return matrix
