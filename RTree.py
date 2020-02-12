

# This program refers to the code in "Core-Functions-R-Tree (Python)" on iLearn



from sys import maxsize
from math import ceil

from Node import Node

class RTree:     # It is the main class for implementing RTree in python. As it first adds the data points in an MBR and finally returns the number of data points lying in an MBR after execution of various vital functions necessary for the stability of a RTree i.e. handle_overflow, split, is_covered, is_intersect, choose_subtree, and peri_increase.
    def __init__(self):
        self.root = Node()
        self.B = 4          # declaring the common B value for each MBR

    def query_rtree(self, node, query):   # returns number of data points lying in an MBR (range query).
        num = 0
        if node.leaf_node_check():    # if the passed node is a leaf node, then it will return number of data points stored at the node that are covered by range query using is_covered().  
            for point in node.data_points:            # for-loop to retrieve all the data points in a node
                if self.covering_check(point, query):        # check if the data point lies in the query or not
                    num = num + 1                      # increase num by 1, if point lies in the given query
            return num
        else:    # if the node is not leaf, then again run the query() for each child node of the passed node, if it is intersecting with the given query. Finally, return the number of data points in a range query (MBR).
            for child in node.child_nodes:      # for-loop to retrieve all the child nodes of a node
                if self.intersection_check(child, query):     # check if the child node is colliding with the query or not
                    num = num + self.query_rtree(child, query)          # run the query_rtree() again, until we get the leaf node to know the exact number of point lies in the given query
            return num

    def intersection_check(self, node, query):   # checks if two MBRs are intersecting or not. If the boundaries of any of the two MBRs will be colliding with each other, then we will find:
        # |center1_x - center2_x| <= length1 / 2 + length2 / 2 and:
        # |center1_y - center2_y| <= width1 / 2 + width2 / 2
        center1_x = (node.MBR['x2'] + node.MBR['x1']) / 2          # center's x coordinate of mbr1 = (upper x of mbr1 + upper x of mbr1) / 2
        center1_y = (node.MBR['y2'] + node.MBR['y1']) / 2          # center's y coordinate of mbr1 = (upper y of mbr1 + upper y of mbr1) / 2
        length1 = node.MBR['x2'] - node.MBR['x1']                  # length of mbr1 = upper x of mbr1 - upper x of mbr1
        width1 = node.MBR['y2'] - node.MBR['y1']                   # width of mbr1 = upper y of mbr1 - upper y of mbr1
        center2_x = (query['x2'] + query['x1']) / 2                # center's x coordinate of mbr2 = (upper x of mbr2 + upper x of mbr2) / 2
        center2_y = (query['y2'] + query['y1']) / 2                # center's y coordinate of mbr2 = (upper y of mbr2 + upper y of mbr2) / 2
        length2 = query['x2'] - query['x1']                        # length of mbr2 = upper x of mbr2 - upper x of mbr2
        width2 = query['y2'] - query['y1']                         # width of mbr2 = upper y of mbr2 - upper y of mbr2
        if abs(center1_x - center2_x) <= length1 / 2 + length2 / 2 and\
                abs(center1_y - center2_y) <= width1 / 2 + width2 / 2:
            return True
        else:
            return False

    def covering_check(self, point, query):    # checks that an MBR is covering a given data point or not.  

        x1, x2, y1, y2 = query['x1'], query['x2'], query['y1'], query['y2']
        if x1 <= point['x'] <= x2 and y1 <= point['y'] <= y2:    # If the value of x and y coordinates will lie between x1 & x2 and y1 & y2 respectively. Then, the query is covering the given data point, otherwise not. 
            return True
        else:
            return False

    def insert(self, u, p):    # Basically, used to insert a data point in a desired MBR.
        if u.leaf_node_check():    # If the target node (u) is a leaf node, then it will directly add the data point and check for the overflow condition of the node. 
            self.data_point_add(u, p)
            if u.overflow_check():
                self.overflow_handling(u)
        else:     # if the target node (u) is not a leaf node, then it will choose an optimal subtree and again perform the insert(). Finally, update the MBR.
            v = self.subtree_select(u, p)
            self.insert(v, p)
            self.mbr_updation(v)


    # return the child whose MBR requires the minimum increase in perimeter to cover p
    def subtree_select(self, u, p):    # returns the child node whose MBR requires the minimum increase in the perimeter to cover a data point p.
        if u.leaf_node_check():    # if the node u will be a leaf node, then it will simply return u. 
            return u
        else:    # if u is not a leaf node, then for each child node of u check is the minimum increase is greater than perimeter increase of the child or not. If yes, then return that child as the best child.   
            min_increase = maxsize
            best_child = None
            for child in u.child_nodes:
                if min_increase > self.perimeter_increased(child, p):
                    min_increase = self.perimeter_increased(child, p)
                    best_child = child
            # return self.subtree_select(best_child, p)
            return best_child

    def perimeter_increased(self, node, p):   # returns increase of perimeter by subtracting the original perimeter from the new perimeter.
        # new perimeter - original perimeter = increase of perimeter
        # (max([x1, x2, p['x']]) - min([x1, x2, p['x']]) + max([y1, y2, p['y']]) - min([y1, y2, p['y']])) is the new perimeter. 
        # node.perimeter() is the original perimeter.
        origin_mbr = node.MBR
        x1, x2, y1, y2 = origin_mbr['x1'], origin_mbr['x2'], origin_mbr['y1'], origin_mbr['y2']
        increase = (max([x1, x2, p['x']]) - min([x1, x2, p['x']]) +
                    max([y1, y2, p['y']]) - min([y1, y2, p['y']])) - node.perimeter_mbr()
        return increase

    def overflow_handling(self, u):    # Used to manage the overflow condition (when value of B exceeds 4) of an MBR by splitting and adding new child nodes to it.
        u1, u2 = self.split_node(u)    # Firstly, we will split the overflowed node into 2 sub nodes using split(). 
        # if u is root, create a new root with s1 and s2 as its' children
        if u.root_node_check():    # If u is root node, create a new root with s1 & s2 as its' children and update the MBR.
            new_root = Node()
            self.child_node_add(new_root, u1)
            self.child_node_add(new_root, u2)
            self.root = new_root
            self.mbr_updation(new_root)
        # if u is not root, delete u, and set s1 and s2 as u's parent's new children
        else:    # If u is not root node, delete u, and set s1 and s2 as u's parent's new children, then again check the overflow condition for parent node. Finally, update the MBR.         
            w = u.parent
            # copy the information of s1 into u
            w.child_nodes.remove(u)
            self.child_node_add(w, u1)
            self.child_node_add(w, u2)
            if w.overflow_check():
                self.overflow_handling(w)
            self.mbr_updation(w)

    def split_node(self, u):    # It just splits an node into two nodes. 
        # split u into s1 and s2
        best_s1 = Node()
        best_s2 = Node()
        best_perimeter = maxsize
        # u is a leaf node
        if u.leaf_node_check():    # If it is a leaf node, it creates two different kinds of divides.
            m = u.data_points.__len__()
            # create two different kinds of divides
            divides = [sorted(u.data_points, key=lambda data_point: data_point['x']),           # divide 1 will take the sorted x coordinates of data point
                       sorted(u.data_points, key=lambda data_point: data_point['y'])]           # divide 2 will take the sorted y coordinates of data point
            for divide in divides:
                for i in range(ceil(0.4 * self.B), m - ceil(0.4 * self.B) + 1):
                    s1 = Node()
                    s1.data_points = divide[0: i]
                    self.mbr_updation(s1)
                    s2 = Node()
                    s2.data_points = divide[i: divide.__len__()]
                    self.mbr_updation(s2)
                    if best_perimeter > s1.perimeter_mbr() + s2.perimeter_mbr():           # if best_perimeter value will be greater than the sum of perimeters of s1 and s2
                        best_perimeter = s1.perimeter_mbr() + s2.perimeter_mbr()           # then best_perimeter will be the sum of perimeters of s1 and s2 
                        best_s1 = s1                                                       # then best_s1 will be s1 
                        best_s2 = s2                                                       # then best_s2 will be s2

        # u is an internal node
        else:     # if it is not a leaf node, it creates four different kinds of divides.
            # create four different kinds of divides
            m = u.child_nodes.__len__()
            divides = [sorted(u.child_nodes, key=lambda child_node: child_node.MBR['x1']),      # divide 1 will take the sorted x1 coordinates of mbr
                       sorted(u.child_nodes, key=lambda child_node: child_node.MBR['x2']),      # divide 2 will take the sorted x2 coordinates of mbr
                       sorted(u.child_nodes, key=lambda child_node: child_node.MBR['y1']),      # divide 3 will take the sorted y1 coordinates of mbr
                       sorted(u.child_nodes, key=lambda child_node: child_node.MBR['y2'])]      # divide 4 will take the sorted y2 coordinates of mbr
            for divide in divides:
                for i in range(ceil(0.4 * self.B), m - ceil(0.4 * self.B) + 1):
                    s1 = Node()
                    s1.child_nodes = divide[0: i] 
                    self.mbr_updation(s1)
                    s2 = Node()
                    s2.child_nodes = divide[i: divide.__len__()]
                    self.mbr_updation(s2)
                    if best_perimeter > s1.perimeter_mbr() + s2.perimeter_mbr():
                        best_perimeter = s1.perimeter_mbr() + s2.perimeter_mbr()
                        best_s1 = s1
                        best_s2 = s2

        for child in best_s1.child_nodes:
            child.parent = best_s1
        for child in best_s2.child_nodes:
            child.parent = best_s2

        return best_s1, best_s2

    def child_node_add(self, node, child):    # adds a new child node of an existing node.
        node.child_nodes.append(child)
        child.parent = node
        # self.mbr_updation(node)
        if child.MBR['x1'] < node.MBR['x1']:
            node.MBR['x1'] = child.MBR['x1']
        if child.MBR['x2'] > node.MBR['x2']:
            node.MBR['x2'] = child.MBR['x2']
        if child.MBR['y1'] < node.MBR['y1']:
            node.MBR['y1'] = child.MBR['y1']
        if child.MBR['y2'] > node.MBR['y2']:
            node.MBR['y2'] = child.MBR['y2']

    def data_point_add(self, node, data_point):    # Used to directly add data points in a node of RTree.
        node.data_points.append(data_point)
        self.mbr_updation(node)
        if data_point['x'] < node.MBR['x1']:
            node.MBR['x1'] = data_point['x'] 
        if data_point['x'] > node.MBR['x2']:
            node.MBR['x2'] = data_point['x']
        if data_point['y'] < node.MBR['y1']:
            node.MBR['y1'] = data_point['y']
        if data_point['y'] > node.MBR['y2']:
            node.MBR['y2'] = data_point['y']

    def mbr_updation(self, node):    # Used for updating the MBR after performing some functions on it.
        # print("mbr_updation")
        x_list = []                   # initializing a list for x coordinates
        y_list = []                   # initializing a list for y coordinates
        if node.leaf_node_check():              # if node is a leaf node, then we will add x and y coordinates of points in the above declared lists
            x_list = [point['x'] for point in node.data_points]
            y_list = [point['y'] for point in node.data_points]
        else:                                   # if node is not a leaf node, then we will add upper x and lower x coordinates of child node in the above declared lists
            x_list = [child.MBR['x1'] for child in node.child_nodes] + [child.MBR['x2'] for child in node.child_nodes]
            y_list = [child.MBR['y1'] for child in node.child_nodes] + [child.MBR['y2'] for child in node.child_nodes]
        new_mbr = {                  # now, just store minimum and maximum values of x_list and y_list in 'x1', 'x2', 'y1', and 'y2'.
            'x1': min(x_list),       
            'x2': max(x_list),
            'y1': min(y_list),
            'y2': max(y_list)
        }
        node.MBR = new_mbr          # finally, put new mbr's values in the initial mbr values of the node
