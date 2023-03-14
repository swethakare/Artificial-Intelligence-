'''
Created on Feb 8, 2023

@author: Swetha Kare
GID: G01378458
'''
import math
from pyamaze import maze,agent,textLabel
from queue import PriorityQueue

def hfunc(current,goal):
#hfunction is the manhattan distance and can be calculated using the formula abs(x1-x2) + abs(y1-y2)
    x1,y1=current 
    x2,y2=goal
    return abs(x1-x2) + abs(y1-y2)

def gfunc(start,current):
#gfunction is the euclidian distance and can be calculated using the formula math.isqrt(pow((x2-x1),2)+pow((y2-y1),2))
    x1,y1 = start
    x2,y2 = current  
    Gfunction = math.isqrt(pow((x2-x1),2)+pow((y2-y1),2))
    return Gfunction;
                      
def aStar(m):
    start=(m.rows,m.cols)
# Assign fFunction with infinity, this function keeps changing whenever we encounter a new child of the current node  
    Ffunc={cell:float('inf') for cell in m.grid}
    Ffunc[start]=gfunc(start,start)+hfunc(start,(1,1))
    
# PriorityQ is initially added with the start cell's Ffunction 
    PrioQ=PriorityQueue()
    PrioQ.put((Ffunc[start],start))
    aPath={}
    while not PrioQ.empty():
        currCell=PrioQ.get()[1]
# if we have reached (1,1) then we have arrived at the goal node so break to return the answer
        if currCell==(1,1):
            break
# Check if there is neighbor(that is stored inside the map), if neighbour is found then add the neighbor along with its cost to the qeue.
        for d in 'NSEW':
            if m.maze_map[currCell][d]==True:
                if d=='E':
                    NeighbourCell=(currCell[0],currCell[1]+1)
                if d=='W':
                    NeighbourCell=(currCell[0],currCell[1]-1)
                if d=='N':
                    NeighbourCell=(currCell[0]-1,currCell[1])
                if d=='S':
                    NeighbourCell=(currCell[0]+1,currCell[1])                    
# computing ffunction for each neighbor node that is adjacent to the current cell  
                  
                temp_Ffunc=gfunc(start,NeighbourCell)+hfunc(NeighbourCell,(1,1))
                if temp_Ffunc < Ffunc[NeighbourCell]:
# assigning cost of the function to the neighbor cells                    
                    Ffunc[NeighbourCell]= temp_Ffunc
                    PrioQ.put((temp_Ffunc,NeighbourCell))
# storing the parent in apath dictionary to finally arrive at the path from start to goal node                   
                    aPath[NeighbourCell]=currCell
                    
    forwardPath={}
    cell= (1,1)
# returns the cell path from start to the goal node ( maze path is returned)    
    while cell!=start:
        forwardPath[aPath[cell]]=cell
        cell=aPath[cell]
    
    return forwardPath

if __name__=='__main__':
    
    m=maze(80,80)
    m.CreateMaze()
    Astarpath=aStar(m)
    a=agent(m,footprints=True)
    m.tracePath({a:Astarpath})
    l=textLabel(m,'A Star Path Length',len(Astarpath)+1)
    m.run()
