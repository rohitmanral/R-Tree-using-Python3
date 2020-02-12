

# This program refers to the code in "Core-Functions-R-Tree (Python)" on iLearn



from math import ceil

class Node:    # Node class is used to extract perimeter, underflow & overflow conditions, and type (root &leaf) of every node in a RTree.  
    def __init__(self):   # Here, I am initializing all the required lists, values of MBR's coordinates, and setting the value of B to 4.
        self.id = 0
        self.B = 4
        self.child_nodes = []
        self.data_points = []
        self.parent = None
        self.MBR = {                # initially declared lower x, upper x, lower y, and upper y values for an mbr
            'x1': -1,
            'y1': -1,
            'x2': -1,
            'y2': -1,
        }

    def perimeter_mbr(self):   # it returns the perimeter (addition of length and breadth) of an MBR.
        return (self.MBR['x2'] - self.MBR['x1']) + (self.MBR['y2'] - self.MBR['y1'])

    def underflow_check(self):    # Checks that a node is in underflow condition i.e. B < 2.
        if self.leaf_node_check():          # when node is leaf, it will return true, if length of data points would be smaller than smallest integer not less than B/2
            if self.data_points.__len__() < ceil(self.B / 2):
                return True
            else:
                return False
        else:                              # when node is not leaf, it will return true, if length of child nodes will be smaller than smallest integer not less than B/2.
            if self.child_nodes.__len__() < ceil(self.B / 2):
                return True
            else:
                return False

    def overflow_check(self):    # Checks that a node is in overflow condition i.e. B > 4.
        if self.leaf_node_check():           # when node is leaf, it will return true, if length of data points will be greater than B. 
            if self.data_points.__len__() > self.B:
                return True
            else:
                return False
        else:                              # when node is not leaf, it will return true, if length of child nodes will be greater than B.
            if self.child_nodes.__len__() > self.B:
                return True
            else:
                return False

    def root_node_check(self):    # Checks that a node is root node or not. If a node will not have any parent node.


        if self.parent is None:     # if a node does not have any parent node, then it is a root node
            return True
        else:
            return False

    def leaf_node_check(self):   # Checks that a node is leaf node or not. It will return true when length of the child nodes of a node is 0.


        if self.child_nodes.__len__() == 0:            # if a node does not have any child node, then it is a leaf node
            return True
        else:
            return False
