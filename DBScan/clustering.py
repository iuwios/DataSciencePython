
import sys,re
import numpy
from array import array

UNCLASSIFIED = False
NOISE = None

def init(textFile):
    
    cnt = 0
    height = list()
    test = list()
    first = list()
    second = list()
    n=0
    
     
    #input the texFilfe in list
    for r in textFile:
        height.append(r)
    
    #print(len(height)%2)
    #clean the data by taking unnecessary tokens and separate header from the rest
    for row in height:
        #delete unnecessary parts
        row = row.strip('\n')
        row = row.strip('\r')
        row = row.strip(' ')
        notab = re.split(r'\t+', row)
        
        #save the x and y coordinates
        if( len(height)%2 == 0):
            if(n < (len(height)/2)):
                first.append(float(notab[1]))
                first.append(float(notab[2]))
                n = n+1
       
            else:    
                second.append(float(notab[1]))
                second.append(float(notab[2]))
                n = n+1
    
    
        
    test.append(first)
    test.append(second)
        
    
        
    #save the overall list in numpy array
    m = numpy.array(test)
    m = numpy.reshape(m, (m.shape[1], m.shape[0]))
    #print(m)
        
    return m

#DBScan Algorithm with inputs data, epsilon and minimum point
def MyDBSCAN(D, eps, MinPts):
 
    # This list will hold the final cluster assignment for each point in D.
    # There are two reserved values:
    #    -1 - Indicates a noise point
    #     0 - Means the point hasn't been considered yet.
    # Initially all labels are 0.    
    labels = [0]*len(D)
    #print(labels)
    #print(len(D))

    # C is the ID of the current cluster.    
    C = 0
    
    # This outer loop is just responsible for picking new seed points--a point
    # from which to grow a new cluster.
    # Once a valid seed point is found, a new cluster is created, and the 
    # cluster growth is all handled by the 'expandCluster' routine.
    
    # For each point P in the Dataset D...
    # ('P' is the index of the datapoint, rather than the datapoint itself.)
    for P in range(0, len(D)):
    
        # Only points that have not already been claimed can be picked as new 
        # seed points.    
        # If the point's label is not 0, continue to the next point.
        if not (labels[P] == 0):
           #print(labels[P])
           continue
        
        # Find all of P's neighboring points.
        NeighborPts = findNeighbor(D, P, eps)
        #print(NeighborPts)
        
        # If the number is below MinPts, this point is noise. 
        # This is the only condition under which a point is labeled 
        # NOISE--when it's not a valid seed point. A NOISE point may later 
        # be picked up by another cluster as a boundary point (this is the only
        # condition under which a cluster label can change--from NOISE to 
        # something else).
        #print(NeighborPts)
        if len(NeighborPts) < MinPts:
            labels[P] = -1
            #print(labels[P])
        # Otherwise, if there are at least MinPts nearby, use this point as the 
        # seed for a new cluster.    
        else: 
           # Get the next cluster label.
           C += 1
           
           # Assing the label to our seed point.
           labels[P] = C
           
           # Grow the cluster from the seed point.
           addCluster(D, labels, P, C, eps, MinPts)
           
    
    # All data has been clustered!
    #print(labels)
    #print(labels)
    return labels

# D is the dataset
# labels stores the cluster labels
#P is the index
# C is the label for the new cluster
#eps is the epsilon
#MinPTS is the minimum point
def addCluster(D, labels, P, C, eps, MinPts):

    # SearchQueue is a FIFO queue of points to evaluate. It will only ever 
    # contain points which belong to cluster C (and have already been labeled
    # as such).
    #
    # The points are represented by their index values (not the actual vector).
    #
    # The FIFO queue behavior is accomplished by appending new points to the
    # end of the list, and using a while-loop rather than a for-loop.
    SearchQueue = [P]

    # For each point in the queue:
    #   1. Determine whether it is a branch or a leaf
    #   2. For branch points, add their unclaimed neighbors to the search queue
    i = 0
    while i < len(SearchQueue):    
        
        # Get the next point from the queue.        
        P = SearchQueue[i]

        # Find all the neighbors of P
        NeighborPts = findNeighbor(D, P, eps)
        
        # If the number of neighbors is below the minimum, then this is a leaf
        # point and we move to the next point in the queue.
        if len(NeighborPts) < MinPts:
            i += 1
            continue
        
        # Otherwise, we have the minimum number of neighbors, and this is a 
        # branch point.
            
        # For each of the neighbors...
        for Pn in NeighborPts:
           
            # If Pn was labelled NOISE during the seed search, then we
            # know it's not a branch point (it doesn't have enough 
            # neighbors), so make it a leaf point of cluster C and move on.
            if labels[Pn] == -1:
               labels[Pn] = C
            # Otherwise, if Pn isn't already claimed, claim it as part of
            # C and add it to the search queue.   
            elif labels[Pn] == 0:
                # Add Pn to cluster C.
                labels[Pn] = C
                
                # Add Pn to the SearchQueue.
                SearchQueue.append(Pn)
            
        # Advance to the next point in the FIFO queue.
        i += 1        
    
    # We've finished growing cluster C!

#finds all neighboring point by comparing distance to epsilon
def findNeighbor(D, P, eps):
    neighbors = []
    
    # For each point in the dataset...
    for Pn in range(0, len(D)):
        
        # If the distance is below the threshold, add it to the neighbors list.
        if numpy.linalg.norm(D[P] - D[Pn]) < eps:
           #print(numpy.linalg.norm(D[P] - D[Pn]))   
           neighbors.append(Pn)
    #print(neighbors) 
    return neighbors
    
if __name__ == "__main__":
    
    cnt=1;
    
     #run python in commandline
    script = sys.argv[0]
    #input file
    f1 = open(sys.argv[1],"r")
    #number of cluster
    n = sys.argv[2]
    #Epsilon
    EPS = sys.argv[3]
    #Minimum number of points
    MinPts = sys.argv[4]
    
    #initializing data before clustering
    m = init(f1)
    
    
    DB = MyDBSCAN(m, float(EPS), float(MinPts))
    
    #dividing cluster
    clust_1 = list()
    clust_2 = list()
    clust_3 = list()
    clust_4 = list()
    clust_5 = list()
    clust_6 = list()
    clust_7 = list()
    clust_8 = list()
    for element in range(0, len(DB)):
        if(DB[element] == 1):
            clust_1.append(element)
        elif(DB[element] == 2):
            clust_2.append(element)
        elif(DB[element] == 3):
            clust_3.append(element)
        elif(DB[element] == 4):
            clust_4.append(element)
        elif(DB[element] == 5):
            clust_5.append(element)
        elif(DB[element] == 6):
            clust_6.append(element)
        elif(DB[element] == 7):
            clust_7.append(element)
        elif(DB[element] == 8):
            clust_8.append(element)
            
    
   
    #saving cluster
    while(cnt<=n):
        if(cnt==1):
            file = open("input2_cluster_1_ideal", "w")
            for elem in clust_1:
                file.write( str(elem) +"\n")
            file.close()
        elif(cnt ==2):
            file = open("input2_cluster_2_ideal", "w")
            for elem in clust_1:
                file.write( str(elem) +"\n")
            file.close
        elif(cnt ==3):
            file = open("input2_cluster_3_ideal", "w")
            for elem in clust_1:
                file.write( str(elem) +"\n")
            file.close
        elif(cnt ==4):
            file = open("input2_cluster_4_ideal", "w")
            for elem in clust_1:
                file.write( str(elem) +"\n")
            file.close
        elif(cnt ==5):
            file = open("input2_cluster_5_ideal", "w")
            for elem in clust_1:
                file.write( str(elem) +"\n")
            file.close
        elif(cnt ==6):
            file = open("input2_cluster_6_ideal", "w")
            for elem in clust_1:
                file.write( str(elem) +"\n")
            file.close
        elif(cnt ==7):
            file = open("input2_cluster_7_ideal", "w")
            for elem in clust_1:
                file.write( str(elem) +"\n")
            file.close
        elif(cnt ==8):
            file = open("input2_cluster_8_ideal", "w")
            for elem in clust_1:
                file.write( str(elem) +"\n")
            file.close
        