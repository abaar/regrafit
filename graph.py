# Python Program to detect cycle in an undirected graph
 
from collections import defaultdict
  
#This class represents a undirected graph using adjacency list representation
class Graph:
  
    def __init__(self,vertices):
        self.V= vertices #No. of vertices
        self.graph = defaultdict(list) # default dictionary to store graph
        self.Time = 0
        self.eupath=list()
    # function to add an edge to graph
    def addEdge(self,v,w):
        self.graph[v].append(w) #Add w to v_s list
        self.graph[w].append(v) #Add v to w_s list
  
    # A recursive function that uses visited[] and parent to detect
    # cycle in subgraph reachable from vertex v.
    def isCyclicUtil(self,v,visited,parent):
 
        #Mark the current node as visited 
        visited[v]= True
 
        #Recur for all the vertices adjacent to this vertex
        for i in self.graph[v]:
            # If the node is not visited then recurse on it
            if  visited[i]==False : 
                if(self.isCyclicUtil(i,visited,v)):
                    return True
            # If an adjacent vertex is visited and not parent of current vertex,
            # then there is a cycle
            elif  parent!=i:
                return True
         
        return False

    def deleteEdge(self,v,w):
        del self.graph[v]
        del self.graph[w]
  
    #Returns true if the graph contains a cycle, else false.
    def isCyclic(self):
        # Mark all the vertices as not visited
        visited =[False]*(self.V)
        # Call the recursive helper function to detect cycle in different
        #DFS trees
        for i in range(self.V):
            if visited[i] ==False: #Don't recur for u if it is already visited
                if(self.isCyclicUtil(i,visited,-1))== True:
                    return True
         
        return False
    # This function removes edge u-v from graph    
    def rmvEdge(self, u, v):
        for index, key in enumerate(self.graph[u]):
            if key == v:
                self.graph[u].pop(index)
        for index, key in enumerate(self.graph[v]):
            if key == u:
                self.graph[v].pop(index)

 #A function used by isConnected
    def DFSUtil(self,v,visited):
        # Mark the current node as visited 
        visited[v]= True
 
        #Recur for all the vertices adjacent to this vertex
        for i in self.graph[v]:
            if visited[i]==False:
                self.DFSUtil(i,visited)

 
    # A DFS based function to count reachable vertices from v
    def DFSCount(self, v, visited):
        count = 1
        visited[v] = True
        for i in self.graph[v]:
            if visited[i] == False:
                count = count + self.DFSCount(i, visited)         
        return count
 
    # The function to check if edge u-v can be considered as next edge in
    # Euler Tour
    def isValidNextEdge(self, u, v):
        # The edge u-v is valid in one of the following two cases:
  
          #  1) If v is the only adjacent vertex of u
        if len(self.graph[u]) == 1:
            return True
        else:
            '''
             2) If there are multiple adjacents, then u-v is not a bridge
                 Do following steps to check if u-v is a bridge
  
            2.a) count of vertices reachable from u'''   
            visited =[False]*(self.V)
            count1 = self.DFSCount(u, visited)
 
            '''2.b) Remove edge (u, v) and after removing the edge, count
                vertices reachable from u'''
            self.rmvEdge(u, v)
            visited =[False]*(self.V)
            count2 = self.DFSCount(u, visited)
 
            #2.c) Add the edge back to the graph
            self.addEdge(u,v)
 
            # 2.d) If count1 is greater, then edge (u, v) is a bridge
            return False if count1 > count2 else True
 
 
    # Print Euler tour starting from vertex u
    def printEulerUtil(self, u):
        #Recur for all the vertices adjacent to this vertex
        for v in self.graph[u]:
            #If edge u-v is not removed and it's a a valid next edge
            if self.isValidNextEdge(u, v):
                self.eupath.append((u,v))
                self.rmvEdge(u, v)
                self.printEulerUtil(v)
 
 
     
    '''The main function that print Eulerian Trail. It first finds an odd
   degree vertex (if there is any) and then calls printEulerUtil()
   to print the path '''
    def StartComputeFeury(self):
        #Find a vertex with odd degree
        u = 0
        for i in range(self.V):
            if len(self.graph[i]) %2 != 0 :
                u = i
                break
        # Print tour starting from odd vertex
        #print ("\n")
        self.printEulerUtil(u)
        return self.eupath

    def isConnected(self):
  
        # Mark all the vertices as not visited
        visited =[False]*(self.V)
 
        #  Find a vertex with non-zero degree
        for i in range(self.V):
            if len(self.graph[i]) > 1:
                break
 
        # If there are no edges in the graph, return true
        if i == self.V-1:
            return True
 
        # Start DFS traversal from a vertex with non-zero degree
        self.DFSUtil(i,visited)
 
        # Check if all non-zero degree vertices are visited
        for i in range(self.V):
            if visited[i]==False and len(self.graph[i]) > 0:
                return False
         
        return True

    def isEulerian(self):
        # Check if all non-zero degree vertices are connected
        if self.isConnected() == False:
            return 0
        else:
            #Count vertices with odd degree
            odd = 0
            for i in range(self.V):
                if len(self.graph[i]) % 2 !=0:
                    odd +=1
 
            '''If odd count is 2, then semi-eulerian.
            If odd count is 0, then eulerian
            If count is more than 2, then graph is not Eulerian
            Note that odd count can never be 1 for undirected graph'''
            if odd == 0:
                return 2
            elif odd == 2:
                return 1
            elif odd > 2:
                return 0 
#This code is contributed by Neelam Yadav