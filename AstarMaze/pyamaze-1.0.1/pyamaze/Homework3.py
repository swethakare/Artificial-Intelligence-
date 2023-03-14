import math
from pyamaze import maze,agent,textLabel
from queue import PriorityQueue
#from cmath import sqrt
def h(cell1,cell2):
    x1,y1=cell1 
    x2,y2=cell2
    return abs(x1-x2) + abs(y1-y2)

def g(cell1,cell2):
    x1,y1 = cell1
    x2,y2 = cell2  
    gscore = math.isqrt(pow((x2-x1),2)+pow((y2-y1),2))
    return gscore;
                
def aStar(m):
    start=(m.rows,m.cols)
    g_score={cell:float('inf') for cell in m.grid}
    g_score[start]=0
    f_score={cell:float('inf') for cell in m.grid}
    f_score[start]=h(start,(1,1))

    open=PriorityQueue()
    open.put((h(start,(1,1)),h(start,(1,1)),start))
    
    
    aPath={}
    while not open.empty():
        
        currCell=open.get()[2]
    
        print(currCell)
        if currCell==(1,1):
            break
        for d in 'ESNW':
            print(d)
            print( m.maze_map[currCell][d])
            if m.maze_map[currCell][d]==True:
                if d=='E':
                    childCell=(currCell[0],currCell[1]+1)
                if d=='W':
                    childCell=(currCell[0],currCell[1]-1)
                if d=='N':
                    childCell=(currCell[0]-1,currCell[1])
                if d=='S':
                    childCell=(currCell[0]+1,currCell[1])
                
                print('found open')   
                print(childCell)
                #temp_g_score=g_score[currCell]+1
                temp_g_score=g(start,childCell)
                print(g_score[currCell])
                print(temp_g_score)
                temp_f_score=temp_g_score+h(childCell,(1,1))
                print(temp_f_score)
                if temp_f_score < f_score[childCell]:
                    g_score[childCell]= temp_g_score
                    f_score[childCell]= temp_f_score
                    open.put((temp_f_score,h(childCell,(1,1)),childCell))
                    aPath[childCell]=currCell
                    print(aPath)
    fwdPath={}
    cell=(1,1)
    while cell!=start:
        fwdPath[aPath[cell]]=cell
        cell=aPath[cell]
        print('choosenpath')
        print(fwdPath)
    return fwdPath

if __name__=='__main__':
#rows and cols must are variables, so factual values are needed to avoid errors
      m = maze(3,3) 
      m.CreateMaze() #create a maze with one path
      a = agent(m, footprints = True) 
      m.tracePath({a:m.path})
      l=textLabel(m,'Path Length',len(m.path)+1) #display the cost of the solution
      m.run()