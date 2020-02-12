from time import time
from sys import argv, exit

from RTree import RTree

def query_sequential(points, query):                                     # used to perform sequential queries using the given files of data points and range queries.
    result = 0
    for point in points:                                          # Here, we will make a sequential search by traversing all 1,00,000 data points for every single range query given in the range_query.txt file. Finally, we will get the number of data points lying inside a particular range query.
        if query['x1'] <= point['x'] <= query['x2'] and query['y1'] <= point['y'] <= query['y2']:
            result = result + 1
    return result

def format_data_point(data):                             # Used for converting one data row of "dataset.txt" file into the format used in the program i.e. (x , y). 
    data = data.split(' ')                              # Here, we are splitting every row of dataset.txt file by whitespace and create two different dictionaries from it i.e. x and y. So that we can store the coordinate’s values of 1,00,000 data points.
    return {'x': int(data[1]), 'y': int(data[2])}

def format_range_query(data):                          # Used for converting one data row of range_query.txt file into the format used in the program i.e. (x1 , x2 , y1 , y2). 
    try:
        data = data.split(' ')                         # Here, we are splitting every row of range_query.txt file by whitespace and create four different dictionaries from it i.e. x1, x2, y1 and y2. So that we can store the values of lower-left and upper-right coordinates of 100 range queries.
        return {'x1': int(data[0]), 'x2': int(data[1]), 'y1': int(data[2]), 'y2': int(data[3])}
    except: 
        return {}    

def main():                                          # runs the files mentioned through command line arguments as mentioned above. Otherwise, exists with an error. In addition, runs and tests RTree against sequential queries.
    try:
        filePoints = argv[1]                        # filePoints stores the second argument of [python3 main.py {dataset}.txt {range_query}.txt] i.e. dataset.txt.
        fileQuery = argv[2]                        # fileQuery stores the third argument of [python3 main.py {dataset}.txt {range_query}.txt] i.e. range_query.txt.
    except:                                       # in case, if error occurs print 'Incorrect Usage'
        print('Incorrect Usage.')
        exit(1)

    try:
        file = open(filePoints, "r")                                     # open the "dataset.txt" file
        rows = file.read().split('\n')                                   # first splitting the file by next line, then reading it
        points = list(map(format_data_point, rows[1:int(rows[0])+1]))    # storing the actual values of the data points in "points" list using map()
    except:                                                              # in case, if error occurs print 'filePoints: File Not Found'
        print('{}: File Not Found.'.format(filename))                  
        exit(1)

    try:
        file = open(fileQuery, "r")                                           # open the "range_query.txt" file
        queries = list(map(format_range_query, file.read().split('\n')))      # first splitting the file by next line, then reading it and using map() 
        queries = [q for q in queries if q != {}] 
    except:
        print('{}: File Not Found.')                                         # in case, if error occurs print 'fileQuery: File Not Found'
        exit(1)    

    print('------------------Building RTree------------------\n')
    rtree = RTree()                                                           # making an object of RTree class
    for point in points:
        rtree.insert(rtree.root, point)                                         # inserting a point in the RTree from root node
    start = time()                                                                  # initializing a time variable for getting total time taken through sequential search 
    for query in queries:
        query_sequential(points, query)                                             # running the sequential search function 100 times on 100000 data points
    t1 = time() - start                                                              # storing the total time taken to run 100 queries sequentially in "t1" variable
    print('Total time for sequential queries: {}'.format(t1))                        # printing the total time taken to run 100 queries sequentially
    print('Average time for every sequential query: {}\n'.format(t1/len(queries)))     # printing the average time taken to run a single query sequentially
    file = open("./query_results.txt", "w+")                                            # opening a new file i.e. "query_results.txt", where the final answers of all the 100 queries will be stored
    start = time()                                                                 # initializing a time variable for getting total time taken through RTree search 
    for query in queries:
        file.write("{}\n".format(rtree.query_rtree(rtree.root, query)))            # writing the final answers of all the 100 queries in "query_results.txt"
    t2 = time() - start                                                             # storing the total time taken to run 100 queries implementing RTree in "t2" variable
    file.close()                                                                   # closing the "query_results.txt" file
    print('Total time for R-Tree queries: {}'.format(t2))                          # printing the total time taken to run 100 queries implementing RTree
    print('Average time for every R-Tree query: {}\n'.format(t2/len(queries)))      # printing the average time taken to run a single query implementing RTree
    print('R-Tree is {} times faster than sequential query'.format(t1/t2))          # making a comparison between the time taken to run 100 queries sequentially and implementing RTree  
    
main()
