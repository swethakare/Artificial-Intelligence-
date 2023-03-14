'''
Created on Mar 1, 2023

@author: swetha Kare
GID: G01378458
'''
import random
import math
import copy
from queue import PriorityQueue
from cmath import pi

def randomMatrix_func(N,K):
# randomly creates a matrix that can be given as input to the simulated annealing algorithm
    rows, cols = (N, K)
    Matrix = [[random.randint(0, 1) for j in range(cols)] for i in range(rows)]
    return Matrix

def objective_func(Matrix,K,N):
# considering N X T matrix and obtaining total cost.
    i = 0
    cost=0
    while i < K:
        j = i+1
        while j < K:
            startcol=(int(str(i)))
            endcol=(int(str(j)))
            cost += estimatecost(startcol,endcol,Matrix,N)
            j += 1
        i += 1
    return cost

def estimatecost(startcol,endcol,Matrix,N):
# based on the combinations between the columns(01,02,03...34) for K=5 the estimated missing combinations count is found
    check = ['00','01','10','11']
    valcheck = []
    i=0
    while i<N:
        val1 = Matrix[i][startcol]
        val2 = Matrix[i][endcol]
        valcheck.append(str(val1)+str(val2))
        i +=1
    MissingCombi = compareCombinations(valcheck,check)  
    return MissingCombi

def compareCombinations(array2,array1):
# compares combinations with the allowed combinations and returns the missing combinations
    missing_count = 0
    for i in range(len(array1)):
        found = False
        for j in range(len(array2)):
            if array1[i] == array2[j]:
                found = True
                break
        if not found:
            missing_count += 1    
    return missing_count

def neighbourMatrix_func(tempMat,K,N,row_index,rand_col_index,PrioQ):
# adds all possible neighbors, and their objective functions into a queue and returns it
    if (tempMat[row_index][rand_col_index]==1):
        tempMat[row_index][rand_col_index]= 0
    else:
        tempMat[row_index][rand_col_index]= 1

    NextCost = objective_func(tempMat,K,N) 
    PrioQ.put((NextCost,tempMat))
    return PrioQ
       
def Simulate_Annealing(N,K,v,t,Matrix,CurrentCost):
# returns the CA with 0 cost
    Best = copy.deepcopy(Matrix)
    BestCost = CurrentCost
    PrioQ=PriorityQueue()
    CurrentMatrix = copy.deepcopy(Matrix)
    Temperature = K;
# pi is the frozen factor.
    pi = pow(v, t) * math.comb(K, t)
    times = 0
    frozenCnt = 0
    while(Temperature):
        if Temperature==0:
# if temperature is 0 then just return that no solution can be achieved. 
            print("Minimum Temperature is arrived")
            print("No Solution Found")
            break 

        if CurrentCost == 0:
# if the current cost is 0 then the covering array is returned.
            print("Covering Array")
            print("Execution Times:",times)
            for row in Best:
                print(row)
            break
        
        if frozenCnt == pi:
# if the frozen count is equal to the frozen factor then we can presume that there exist no best solution and return
            print("Frozen State")
            print("No Solution Found")
            break
        
        num_cols = len(Matrix[0])
        rand_col_index = random.randint(0, num_cols - 1)
        i=0
# determines the number of neighbors based on the value of N
        while(i<N):
            tempMat = copy.deepcopy(Matrix)
            PrioQ = neighbourMatrix_func(tempMat,K,N,i,rand_col_index,PrioQ)
            i +=1
        
        NextCost = PrioQ.get()[0]
        NextMatrix = PrioQ.get()[1]
        
# if delta_E is negative then the neighbor state is selected as the current state.
# is delta_E is positive we make a bad move based on the acceptance probability.
        Delta_E = NextCost - CurrentCost
        acceptance_prob = math.exp(-Delta_E/Temperature)
        randomdigit = random.random()
        if(NextCost<CurrentCost):
            CurrentMatrix = NextMatrix
            CurrentCost = NextCost
        elif(acceptance_prob>randomdigit):
            CurrentMatrix = NextMatrix
            CurrentCost = NextCost
            
# if current cost is better then best cost and best matrix are the current ones.
        if(CurrentCost<BestCost):
            Best = CurrentMatrix
            BestCost = CurrentCost
            frozenCnt = 0
            
        frozenCnt += 1       
        Matrix = CurrentMatrix  
# times determines the number of iterations to arrive at the solution 
        times +=1
        Temperature = Temperature*0.99
            

if __name__=='__main__':
    
    v = 2
    t = 2
    print("Please enter a value for K, from 5 to 7:")
    user_inp = input()
    i=0
    while(i<30):
        K = int(user_inp)
        N = 6
# random matrix is generated a new during each iteration of the loop for 30 executions.        
        Matrix = randomMatrix_func(N,K)
        CurrentCost = objective_func(Matrix,K,N)
        Simulate_Annealing(N,K,v,t,Matrix,CurrentCost)
        i += 1
        print("***************************************")
    
    
   
    
    
    