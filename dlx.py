import math

class Node: # a node in a circular quadruply linked list
    def __init__(self, header = None):
        self.left = self.right = self
        self.up = self.down = self
        self.column = self.row = None
        self.header = header if header else self
        self.row = None

class Header(Node): # a header node for each column
    def __init__(self):
        super().__init__()
        self.count = 0 # the number of nodes with a value of 1
    
    def cover(self): # cover a column
        self.left.right = self.right
        self.right.left = self.left
        vertical_node = self.down
        while vertical_node != self:
            horizontal_node = vertical_node.right
            while horizontal_node != vertical_node:
                horizontal_node.down.up = horizontal_node.up
                horizontal_node.up.down = horizontal_node.down
                horizontal_node.header.count -= 1
                horizontal_node = horizontal_node.right
            vertical_node = vertical_node.down
    
    def uncover(self): # uncover a column
        self.left.right = self
        self.right.left = self
        vertical_node = self.down
        while vertical_node != self:
            horizontal_node = vertical_node.right
            while horizontal_node != vertical_node:
                horizontal_node.down.up = self
                horizontal_node.up.down = self
                horizontal_node.header.count += 1
                horizontal_node = horizontal_node.right
            vertical_node = vertical_node.down

class DLX:
    def __init__(self):
        self.root = Header()
        self.solutions = []
    
    def get_minimum(self): # find the column with the minimum 1s
        header = self.root.right.right
        minimum = self.root.right.count
        while header != self.root:
            if header.count == 0:
                header.left.right = header.right
                header.right.left = header.left
                continue
            if header.count == 1:
                return header
            if header.count < minimum:
                minimum = header
            header = header.right
    
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
                        node.up = node.header.up # link to nodes in the column
                        node.down = node.header
                        node.header.up.down = node
                        node.header.up = node
                        node.header.count += 1 # add one to the count of the header
                        node.row = row * n ** 2 + column * n + value - 1 # set the value of the row
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
                            node.up = node.header.up # link to nodes in the column
                            node.down = node.header
                            node.header.up.down = node
                            node.header.up = node
                            node.header.count += 1 # add one to the count of the header
                            node.row = row * n ** 2 + column * n + x # set the value of the row
    
    def search(self):
        if self.root.right == self.root: # if there are no columns left, return the solution
            return self.solutions
        header = self.get_minimum()
        header.cover() # cover the minimum columns
        vertical_node = header.down
        while vertical_node != header: # iterate through the rows
            self.solutions.append(vertical_node)
            horizontal_node = vertical_node.right
            while horizontal_node != vertical_node: # iterate through every node in the row and cover the node
                horizontal_node.header.cover()
                horizontal_node = horizontal_node.right
            vertical_node = vertical_node.down
