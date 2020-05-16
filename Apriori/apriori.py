'''
Created on 2019. 3. 6.

@author: DJeon
'''
import sys,re

from collections import defaultdict
from itertools import chain, combinations

#Union to join sets
def joinSet(setItem, length):
    return set([i.union(j) for i in setItem for j in setItem if len(i.union(j)) == length])

#Read input file and separate itemsets and transactions
def getItemSetTransactionList(textFile):
    transactionList = list()
    setItem = set()
    for record in textFile:
            record = record.strip('\n')
            no_tab = re.split(r'\t+', record)
            transactionList.append(no_tab)
    for j in transactionList:
        for item in j:
            if item not in setItem:
                setItem.add(frozenset([item]))
   
    return setItem, transactionList

#return all possible subsets of given array
def subsets(arr):
    return chain(*[combinations(arr,i+1) for i,a in enumerate(arr)])

#find minimum support of each item
def countSuppandComp(setItem, listTransaction, minimumSupport, frequentSet):
    frequentsetDictionary = defaultdict(int)
    _setItem = set()

    #check each transaction for matching setItem and increment frequentSet
    for item in setItem:
        for transaction in listTransaction:
            if item.issubset(transaction):
                frequentSet[item] += 1
                frequentsetDictionary[item] += 1
    
    #get the support and compare it to the minimum support        
    for item, count in frequentsetDictionary.items():
        support = float(count)/len(listTransaction)
        if support >= minimumSupport:
            _setItem.add(item)
            
    return _setItem

#Apriori main algorithm        
def runApriori(data_iter, minSupport):
    itemSet, transactionList = getItemSetTransactionList(data_iter)
    freqsetDictionary = defaultdict(int)
    largeSet = dict()
    
    oneCSet = countSuppandComp(itemSet, transactionList, minSupport, freqsetDictionary)
    
    #Lset and Cset
    currentLSet = oneCSet
    k=2
    while(currentLSet != set(([]))):
        largeSet[k-1] = currentLSet
        currentLSet = joinSet(currentLSet, k)
        currentCSet = countSuppandComp(currentLSet, transactionList, minSupport, freqsetDictionary)
        currentLSet = currentCSet
        k = k + 1
    
    #support = (frequency of an item) / (length of transactionList)
    def getSupport(item):
        return float(freqsetDictionary[item])/len(transactionList)

    #save the support and confidence of the selected items
    supportConfindenceRule = []
    for key, value in largeSet.items():
        for item in value:
            sub = map(frozenset, [x for x in subsets(item)])
            for element in sub:
                remain = item.difference(element)
                if len(remain) > 0:
                    #confidence
                    confidence = getSupport(item)/getSupport(element)
                    supportConfindenceRule.append(((tuple(element), tuple(remain)), (confidence, getSupport(item))))
    return supportConfindenceRule

#print items in format style and save it in output file
def toFile(rules, outFile):
    for rule, supcon in sorted(rules, key = lambda supcon: supcon):
        left, right = rule
        conf, sup = supcon
        pleft = str(left).replace('(', '')
        pleft = pleft.replace(')', '')
        pleft = pleft.replace("'", '')
        if len(pleft) < 4:
            pleft = pleft.replace(',', '')
        
        pright = str(right).replace('(', '')
        pright = pright.replace(')', '')
        pright = pright.replace("'", '')
        if len(pright) < 4:
            pright = pright.replace(',', '')
        outFile.write("{" + pleft + "}"+"\t" + "{" + pright + "}" + "\t"  + str(format(sup*100,'.2f')) + "\t" + str(format(conf*100,'.2f')) + "\n")
             

if __name__ == "__main__":
   
    transactionList = list()
    b = list()
    
    #run python in commandline
    script = sys.argv[0]
    #minimum support
    minimum = sys.argv[1]
    #input file
    f = open(sys.argv[2],"r")
    #output file
    w = open(sys.argv[3],"w")
    f.close
    outFile = w
    inFile = f
    minimumsupport = float(minimum) * 0.01
    rules = runApriori(inFile, minimumsupport)
    toFile(rules, outFile)
    w.close
    

