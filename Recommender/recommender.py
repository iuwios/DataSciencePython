'''
Created on 2019. 5. 29.

@author: DJeon
'''
import sys, re
from math import sqrt
from copy import deepcopy

#process base and test data
def s1(textFile1,textFile2):
    #['userId', 'movieId', 'rating', 'timestamp']
    input_data = textFile1
    test_data = textFile2
    
    
    filterdata = []
    filterdata2 = []
#base data
    d = 1
    for ln in input_data:
        ln = ln.strip('\n')
        ln = ln.strip('\r')
        notab = re.split(r'\t+', ln)
        filterdata.append([notab[0],notab[1],notab[2]])
        b = notab[0] 
        if(d < int((notab[1]))):
            d = int((notab[1]))
        
#test data   
    for i in test_data:
        i = i.strip('\n')
        i = i.strip('\r')
        notabi = re.split(r'\t+', i)
        #print(notabi[1])
        filterdata2.append([notabi[0],notabi[1]])
        

    return mtrix(filterdata,d,b ), d,b, filterdata2
    
#save base data into matrix table for processing   
def mtrix(file, d, b):
    
    cnt = 1
    #size of matrix, initialize all spaces to 0
    input_movie_and_ratings = [[0]*(d) for n in range(int(b))]
    
    #add the base file information into input_movie_and_ratings
    for ln1 in file:
        input_movie_and_ratings[int(ln1[0])-1][int(ln1[1])-1] = int(ln1[2])
        
            
    return input_movie_and_ratings

#pearson correlation(mean value)
def mean_cos(small_mtrix, mtrx, num_len, n):
    
    sum = 0
    count = 0
    #count all the number of non-zeros for given row
    for num in small_mtrix:
        sum = sum + int(num)
        if(int(num) !=0):
            count = count + 1
            
    #Find Pearson Correlation      
    for cnt in range(num_len):
        if(small_mtrix[cnt] != 0 ):
            #Pearson Correlation equation and add to matrix
            mtrx[n][cnt] = (float(mtrx[n][cnt]) - (float(sum)/float(count)))
      
    return mtrx

#execution
def all(mtrx,num_len,lens):
    
    similarity = [[0]*int(lens) for n in range(int(lens))]
    n = 1
    clean_matrix = deepcopy(mtrx)
    
  
    for line in range(len(mtrx)):
        b = mean_cos(mtrx[line],mtrx, num_len, line) 
    
    input_movie_and_rating2 = [[0]*int(num_len) for n in range(int(lens))]
    input_movie_and_rating3 = [[0]*int(num_len) for n in range(int(lens))]
    
    
    #cosine similarity
    for nm in range(len(mtrx)):
        for m in range(len(mtrx)):
            #cosine similarity
            similarity[nm][m] = cossim(mtrx[nm], mtrx[m])
            #if compared cosine similarity is greater than 0
            if(similarity[nm][m]> 0.01 and similarity[nm][m]<0.99):
                #find the elements for weighted average
                for element in range(int(num_len)):
                    if(int(clean_matrix[nm][element])==0 and int(clean_matrix[m][element])!=0):
                        input_movie_and_rating2[nm][element] = float(input_movie_and_rating2[nm][element]) + (float(similarity[nm][m]) * float(clean_matrix[m][element]))
                        input_movie_and_rating3[nm][element] = float(input_movie_and_rating3[nm][element]) + float(similarity[nm][m]) 
                     
   
    for nm in range(int(lens)):
        for m in range(int(num_len)):
            if(int(clean_matrix[nm][m])==0 and input_movie_and_rating3[nm][m]!=0.0):
                  clean_matrix[nm][m] = float(clean_matrix[nm][m]) + float(input_movie_and_rating2[nm][m])/float(input_movie_and_rating3[nm][m])
                  #print(clean_matrix[nm][m])
         
      
    return clean_matrix

#cosine similarity
def cossim(mtrx1, mtrx2):
    dot1 = 0.0
    ddot1 = 0.0
    ddot2 = 0.0
    #(dot1*dot2)/(||dot1||)(||dot2||)
    for p in range(len(mtrx1)):
        dot1 = dot1 + (float(mtrx1[p])*float(mtrx2[p]))
        ddot1 = ddot1 + float(mtrx1[p])*float(mtrx1[p])
        ddot2 = ddot2 + float(mtrx2[p])*float(mtrx2[p])
    
    ddot2 = sqrt(ddot2)
    ddot1 = sqrt(ddot1)
    

    result = float(dot1)/(float(ddot2)*float(ddot1))
    return result
    
    
if __name__ == '__main__':
    #python script
     script = sys.argv[0]
      #input file
     f1 = open(sys.argv[1],"r")
     f2 = open(sys.argv[2],"r")
    
    #processing input file
     a,num_len,lens,test = s1(f1,f2)
     # find result matrix
     result = all(a,num_len,lens)
     
     #Save result into prediction file
     file = open("u5.base_prediction.txt", "w")
     for i in range(len(test)):
        for j in range(1):
            file.write(str((test[i][0])))
            file.write("\t")
            file.write(str((test[i][1])))
            file.write("\t")
            
            if(float(result[int(test[i][0])-1][int(test[i][1])-1] != 0.0)):
                file.write(str(result[int(test[i][0])-1][int(test[i][1])-1]))
            else:
                file.write(str("1.0"))
            file.write("\n")
     
    
 
     f1.close()
     f2.close()
     file.close()
  

