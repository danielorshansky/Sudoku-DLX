# this implements dancing links and Knuth's algorithm x
# this is specifically designed for sudoku but the same concepts can be applied to all exact-cover problems

import math
import random

class Node: # a node in a circular quadruply linked list
    def __init__(self, header = None):
        self.left = self.right = self
        self.up = self.down = self
        self.column = None
        self.header = header if header else self
        self.data = None

class Header(Node): # a header node for each column
    def __init__(self):
        super().__init__()
        self.count = 0 # the number of nodes with a value of 1
    
    def cover(self): # cover a column
        self.left.right = self.right # unlink the column headers
        self.right.left = self.left
        vertical_node = self.down
        while vertical_node != self:
            horizontal_node = vertical_node.right
            while horizontal_node != vertical_node: # unlink the nodes in the rows
                horizontal_node.down.up = horizontal_node.up
                horizontal_node.up.down = horizontal_node.down
                horizontal_node.header.count -= 1 # remove one from header count
                horizontal_node = horizontal_node.right
            vertical_node = vertical_node.down
    
    def uncover(self): # uncover a column
        self.left.right = self # relink the column headers
        self.right.left = self
        vertical_node = self.down
        while vertical_node != self:
            horizontal_node = vertical_node.right
            while horizontal_node != vertical_node: # relink the nodes in the rows
                horizontal_node.down.up = self
                horizontal_node.up.down = self
                horizontal_node.header.count += 1 # add one back to header count
                horizontal_node = horizontal_node.right
            vertical_node = vertical_node.down

class DLX:
    def __init__(self):
        self.root = Header()
        self.solutions = []
    
    def get_minimum(self): # find the column with the minimum nodes
        header = self.root.right
        minimum = None
        while header != self.root:
            if header.count == 0:
                header.left.right = header.right
                header.right.left = header.left
            elif header.count == 1:
                return header
            elif not minimum:
                minimum = header
            elif header.count < minimum.count:
                minimum = header
            header = header.right
        return minimum
    
    def create_links(self, board, n): # pass the board and size of n x n sudoku
        box_size = int(math.sqrt(n))
        headers = [Header() for _ in range(n ** 2 * 4)]
        for header in headers: # generate and link all headers
            header.right = self.root
            header.left = self.root.left
            self.root.left.right = header
            self.root.left = header
        
        for row in range(n):
            for column in range(n):
                value = board[row][column]
                if value != 0: # if the value is set, create the appropriate constraints for its position and value
                    cell_constraint = Node(headers[n * row + column]) # node for the row-column constraint
                    row_constraint = Node(headers[n ** 2 + row * n + value - 1]) # node for the row-number constraint
                    column_constraint = Node(headers[n ** 2 * 2 + column * n + value - 1]) # node for the column-number constraint
                    box_constraint = Node(headers[n ** 2 * 3 + (row // box_size * box_size + column // box_size) * n + value - 1]) # node for the box-number constraint
                    nodes = [cell_constraint, row_constraint, column_constraint, box_constraint]
                    for index, node in enumerate(nodes):
                        node.right = nodes[(index + 1) % 4] # link nodes to each other
                        node.left = nodes[index - 1]
                        node.up = node.header.up # link to nodes in the column
                        node.down = node.header
                        node.header.up.down = node
                        node.header.up = node
                        node.header.count += 1 # add one to the count of the header
                        node.data = [row, column, value] # set the data of the node
                else: # if the value is not set, create all the constraints for its position
                    for x in random.sample(range(n), n): # loop through all possible values
                        cell_constraint = Node(headers[n * row + column]) # nodes for the row-column constraints
                        row_constraint = Node(headers[n ** 2 + row * n + x]) # nodes for the row-number constraints
                        column_constraint = Node(headers[n ** 2 * 2 + column * n + x]) # nodes for the column-number constraints
                        box_constraint = Node(headers[n ** 2 * 3 + (row // box_size * box_size + column // box_size) * n + x]) # nodes for the box-number constraints
                        nodes = [cell_constraint, row_constraint, column_constraint, box_constraint]
                        for index, node in enumerate(nodes):
                            node.right = nodes[(index + 1) % 4]  # link nodes to each other
                            node.left = nodes[index - 1]
                            node.up = node.header.up # link to nodes in the column
                            node.down = node.header
                            node.header.up.down = node
                            node.header.up = node
                            node.header.count += 1 # add one to the count of the header
                            node.data = [row, column, x + 1] # set the data of the node
    
    def search(self):
        if self.root.right == self.root: # if there are no columns left, it is solved
            return True

        header = self.get_minimum()
        if header == None: # if all columns left are empty, it is solved
            return False
        header.cover() # cover the minimum columns

        vertical_node = header.down
        while vertical_node != header: # iterate through the rows
            self.solutions.append(vertical_node)

            horizontal_node = vertical_node.right
            while horizontal_node != vertical_node: # iterate through every node in the row and cover the node
                horizontal_node.header.cover()
                horizontal_node = horizontal_node.right

            solved = self.search() # move to the next level
            if solved:
                return True
            else:
                return False

            vertical_node = self.solutions.pop() # if the solution is not possible, uncover the column and remove the row from the solution

            header = vertical_node.column

            horizontal_node = vertical_node.right
            while horizontal_node != vertical_node: # uncover each node
                horizontal_node.header.uncover()
                horizontal_node = horizontal_node.right

            vertical_node = vertical_node.down

        header.uncover() # uncover the column

        return False
