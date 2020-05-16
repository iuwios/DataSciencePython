'''
Created on 2019. 4. 9.

@author: DJeon
'''
import sys,re

#initial step
#file is read and the header is split with the other data
def init(textFile):
    
    cnt = 0
    height = list()
    test = list()
    header = list()
     
    #input the texFilfe in list
    for r in textFile:
        height.append(r)
    
    #clean the data by taking unnecessary tokens and separate header from the rest
    for row in height:
        row = row.strip('\n')
        row = row.strip('\r')
        notab = re.split(r'\t+', row)
        #first line is saved as header
        if(cnt == 0):
            header.append(notab)
            cnt = cnt +1
        else:
            test.append(notab)

    #print(header[0])
   
    return test, header



# check if the given is a number
def is_number(given):
    return isinstance(given, int) or isinstance(given, float)
  

# make questions for the given nodes of the tree
# make all possible questions by iterating over all the values and features
# later used to partition data
class Questions:
    
    # question is asked by column number and value
    def __init__(self, column, given):
        self.column = column
        self.value = given

    # compare if the given is a numeric value 
    def compr(self, example):
        val = example[self.column]
        if is_number(val):
            return val >= self.value
        else:
            return val == self.value

   
# partitions the dataset
# create true and false rows to test    
def partition(rows, question):
    
    trueRows, untrueRows = [], []
    
    #check every row if the question is true or false
    for row in rows:
        if question.compr(row):
            trueRows.append(row)
        else:
            untrueRows.append(row)
    return trueRows, untrueRows

# calculate gini impurity
# calculated by summing the probability(pi) of an item with label i being chosen times the probability of a mistake in catagorizing that item.
def gini(rows):
    
    # counts number of the end column which is the result in the given rows
    cnt = {}  
    for row in rows:
        # last column is always the decider
        label = row[-1]
        # print(label)
        if label not in cnt:
            cnt[label] = 0
        cnt[label] += 1
        
    counts = cnt
    # print(counts)
    impurity = 1
    for lbl in counts:
        prob_of_lbl = counts[lbl] / float(len(rows))
        impurity -= prob_of_lbl**2
    return impurity

# impurity of starting node minus the weighted average impurity of the two child node
def igain(left, right, current_uncertainty):
    p = float(len(left)) / (len(left) + len(right))
    return current_uncertainty - p * gini(left) - (1 - p) * gini(right)

# function to split the data all the above functions are used
def split(rows):
    
    bestQuestion = None  
    currentUncertainty = gini(rows)
    nFeatures = len(rows[0]) - 1 
    bestGain = 0  

    # iterate over every value to find the best question
    for col in range(nFeatures):  # for each feature

        values = set([row[col] for row in rows])  # unique values in the column
        # print(values)

        for val in values:  # for each value

            question = Questions(col, val)
            
            # when best question is found the data is partitioned(true,untrue data)
            trueRows, untrueRows = partition(rows, question)
            # print(len(true_rows))
            # print(len(false_rows))

            # if there is no split, then it is skipped
            if len(trueRows) == 0 or len(untrueRows) == 0:
                continue

            # calculate gain
            gain = igain(trueRows, untrueRows, currentUncertainty)

            # find best gain
            # most gain would be the best
            if gain >= bestGain:
                bestGain, bestQuestion = gain, question

    return bestGain, bestQuestion

# leaf node classification data
class Leaf:

    def __init__(self, rows):
        # dictionary to save counted values. For example dict[student] -> number of yes or no
        cnt = {}  
        for row in rows:
        # last column is always the decider
            label = row[-1]
        #print(label)
        if label not in cnt:
            cnt[label] = 0
        cnt[label] += 1
        self.predictions = cnt
        
# node to ask question
# holds reference to the question, and to the two child nodes.
class Node:
    # saves
    def __init__(self, question, true, false):
        self.question = question
        self.trueBranch = true
        self.untrueBranch = false

# building tree 
def buildtree(rows):

# partition the dataset on each of the unique attribute,
# calculate the information gain,
# return the question that produces the highest gain.
    gain, question = split(rows)
    #print(gain)
    #print(question)

#if no more questions, then return leaf
    if gain == 0:
        return Leaf(rows)

# there is useful question with most gain
# data is split based on the most gain question question
    trueRows, untrueRows = partition(rows, question)
# build
    trueBranch = buildtree(trueRows)
# Recursively build the untrue branch.
    untrueBranch = buildtree(untrueRows)

# the current question becomes the deciding node
    return Node(question, trueBranch, untrueBranch)
    
# tracking down a tree
def classify(row, node):
   
    if isinstance(node, Leaf):
        return node.predictions

    # decide to go to true or untrue branch
    if node.question.compr(row):
        return classify(row, node.trueBranch)
    else:
        return classify(row, node.untrueBranch)
    
# print the result    
def leafprint(res):
        
    answer = list()
    for l in res:
        answer.append(l)
        
    #print(answer)
    return answer


if __name__ == "__main__":
    #run python in commandline
    script = sys.argv[0]
    #input file
    f1 = open(sys.argv[1],"r")
    #output file
    f2 = open(sys.argv[2],"r")
    w1 = open(sys.argv[3],"w")
    
    #Train, Test, Output Data
    trainData = f1
    testData = f2
    result = w1 
    
    f1.close
    f2.close
    
    theGroup, theHeader = init(trainData)
    theTree = buildtree(theGroup)
    theTest, theHeaderTr = init(testData)
    
    #delete to match the format for header
    changeHead = []
    changeHead = theHeader[0]
    changeHead = str(changeHead).replace("'", '')
    changeHead = str(changeHead).replace(",", "\t")
    changeHead = str(changeHead).replace("[", '')
    changeHead = str(changeHead).replace("]", '')
    changeHead = str(changeHead).replace(" ", '')
    
    result.write(changeHead + "\n")
    
    #delete to match the format for answer
    for row in theTest:
        together = []
        results = leafprint(classify(row, theTree))
        together = row + results
        together = str(together).replace("'", '')
        together = str(together).replace(",", "\t")
        together = str(together).replace("[", '')
        together = str(together).replace("]", '')
        together = str(together).replace(" ", '')
        #print(together)
        result.write(together + "\n")
        
    w1.close()
        

    