from queue import PriorityQueue
import numpy as np
import random


def makeSpecificGrid():
    grid = np.zeros((10,10),dtype=np.int16)
    for xx in range(10):
        for yy in range(10):
                grid[xx][yy] = random.randrange(1,3)
    return grid

def a_star_search(map,start,goal):
    # store evey node that has been explored
    frontier = PriorityQueue()
    # where we start
    frontier.put(start,0)
    came_from = {}
    came_from[start] = None

    cost_so_far = {}
    cost_so_far[start] = 0

    explored = [start]

    while not frontier.empty():
        #
        current = frontier.get();
        if current == goal:
            break

        neighbors = []
        (x1,y1) = current;
        if(x1>0):
            neighbors.append((x1-1 , y1))
        if(y1>0):
            neighbors.append((x1 , y1-1))
        if(x1< len(map[0])-1):
            neighbors.append((x1+1 , y1))
        if(y1 < len(map[0])-1):
            neighbors.append((x1 , y1+1))

        #计算周边代价 选最小的那个
        for next in neighbors:

            explored.append(next)
            # 之前的代价 + 新代价
            new_cost = cost_so_far[current] + 1
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(goal,next);
                frontier.put(next,priority)
                came_from[next] = current

    cur = goal
    path = [goal]
    while(came_from.get(cur) != start):
        cur = came_from.get(cur)
        path.append(cur)
    path.append(start)
    return path[::-1], cost_so_far.get(goal)

def heuristic(a,b):
    (x1,y1) = a
    (x2,y2) = b
    return abs( x1 - x2 ) + abs( y1 - y2 )

path, camefrom=a_star_search(makeSpecificGrid(),(2,3),(8,7))
print(path)
print(camefrom)
