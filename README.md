# R-Tree-using-Python3
Implementing R-Tree using standard libraries of python programming language &amp; analysing the working of R-Tree.

The objective of this project is to implement the R-tree. The rest of the document explains the details of this project: 

[Dataset]: You will be given a dataset which contains 2D points. The dataset will be provided 
in a text file as the following format: 
n
id 1 x 1 y 1 
id 2 x 2 y 2 ...
id n x n y n 
Specifically, the first line gives the number of points in the dataset. Then, every subsequent line gives a point’s id, x-, and y-coordinates. Your program should build an R-tree in memory from the dataset. 
[Range Query]: You will be given a set of 100 range queries in a text file whose format is: 
x 1 x’ 1 y 1 y’ 1
x 2 x’ 2 y 2 y’ 2
...
x 100 x’ 100 y 100 y’ 100 
That is, each line specifies a query whose rectangle is [x, x′] × [y, y′]. Then, we will measure its query efficiency as follows. 

Directing output to a disk file: 
• Firstly, your program should display the time of answering queries by reading the entire dataset sequentially. This time serves as the sequential-scan benchmark to be compared with the cost of your query algorithms that leverage the R-tree. 
• Secondly, display the number of points returned by each query-note: we need only the number of points retrieved, instead of the details of those points. 
• Thirdly, display the total running time of answering all the 100 queries, and the average time of each query (i.e., divide the total running time by 100). 

[Programming Language]: Python using the existing libraries provided in the programming language of your choice (i.e., some standard libraries or the libraries for R-Tree). 

[Deliverables]: It includes the following components: 
1.	Source Code: The code you have developed yourself. Make sure your code can be run in 
the standard general programming environment. 
2.	Report: Your report should include the following: 
•	A brief description of the main functions in your source code; 
•	A clear specification of the requirements for executing your code such as, OS environ- 
ment, placement of input files, any input parameters, etc. 


Correctness  of this project is based on: 
• [Queries] 
•	–  Correctness: 
o	∗  [Sequential-Scan Based Method]: If it correctly answers m (out of 100) queries by reading the entire dataset sequentially. 
o	∗  [R-Tree Based Method]: If it correctly answers m (out of 100) queries by searching the R-Tree.
•	–  Efficiency: Is the average query time is at least 5 times or 2 times faster than sequential scan. 
• [The Report] 
o	–  Function Description: A clear description of all the functions in my source code. 
o	–  Requirement Description: A clear description of the requirements for executing my code such as, OS environment, placement of input files, any input parameters, etc.
• [Bonus] 
o	–  Implementing the R-Tree by Using Standard Libraries provided by the python rather than using the existing R-Tree libraries. 
o	–  Analysing the Working of R-Tree: In addition to coding, I have provided a high-quality report that contains a detailed analysis of the working of R-Tree. Selecting 10 data points from the given dataset, and one query from the given queries. Then, clearly and correctly analysed the process of the R-Tree construction and the query process (the search should traverse several nodes of the tree, and during the construction of the R-Tree, there should be an overflow and a node splitting).
