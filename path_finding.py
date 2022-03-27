#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 26 16:09:57 2022

@author: heritiana
"""
#%%
import numpy as np



#%%
class Node:
    def __init__(self, coordinate, parent = None, brk = 0):
        self.coordinate = coordinate
        self.parent = parent
        self.n_break = (0 if type(parent) != Node else parent.n_break) + brk
    
    def __str__(self):
        return f"{self.parent} ---> " + f"{str(self.coordinate)}\n"
    
    def __repr__(self):
        return str(self)
    
    def move_up(self, brk = 0):
        x, y = self.coordinate
        return Node([x -1 , y], self, brk)
    
    def move_down(self, brk = 0):
        x, y = self.coordinate
        return Node([x + 1, y], self, brk)
    
    def move_left(self, brk = 0):
        x, y = self.coordinate
        return Node([x, y - 1], self, brk)
    
    def move_right(self, brk = 0):
        x, y = self.coordinate
        return Node([x, y + 1], self, brk)



#%%
def find_path(maze, max_to_break = 0, start = None, goal = None):
    maze = np.array(maze)
    
    row, col = maze.shape 
    _maze = -np.ones((row + 2, col + 2))
    goal = ([row, col] if goal == None else goal)[:]

    current_positions = [ Node([1,1], "Start", 0) if start == None else Node(start, "Start", 0) ]
    _maze[1:-1, 1:-1] = maze
    
    steps_number = 1
    
    while True:
        steps_number += 1
        new_positions = []
        for curr_pos in current_positions:
            x, y = curr_pos.coordinate
            up = _maze[x - 1, y]
            down = _maze[x + 1, y]
            left = _maze[x, y - 1]
            right = _maze[x, y + 1]
            if up in [0,1]:
                new_pos = curr_pos.move_up(up)
                _maze[x - 1, y] = 2 # 2 for visited places
                if new_pos.n_break <= max_to_break:
                    if new_pos.coordinate == goal:
                        return Node(f"Done in {steps_number - 1} moves by breaking {int(new_pos.n_break)} wall(s).", new_pos)
                    new_positions.append(new_pos)
            if down in [0,1]:
                new_pos = curr_pos.move_down(down)
                _maze[x + 1, y] = 2
                if new_pos.n_break <= max_to_break:
                    if new_pos.coordinate == goal:
                        return Node(f"Done in {steps_number - 1} moves by breaking {int(new_pos.n_break)} wall(s).", new_pos)
                    new_positions.append(new_pos)
            if right in [0,1]:
                new_pos = curr_pos.move_right(right)
                _maze[x, y + 1] = 2
                if new_pos.n_break <= max_to_break:
                    if new_pos.coordinate == goal:
                        return Node(f"Done in {steps_number - 1} moves by breaking {int(new_pos.n_break)} wall(s).", new_pos)
                    new_positions.append(new_pos)
            if left in [0,1]:
                new_pos = curr_pos.move_left(left)
                _maze[x, y - 1] = 2
                if new_pos.n_break <= max_to_break:
                    if new_pos.coordinate == goal:
                        return Node(f"Done in {steps_number - 1} moves by breaking {int(new_pos.n_break)} wall(s).", new_pos)
                    new_positions.append(new_pos)
        
        if new_positions == []:
            return "No solutions"
        current_positions = new_positions[:]



#%%
if __name__ == "__main__":
    maze = eval(input("""Enter the maze.                  
                       0 : open
                       1 : wall
                   \n> """))
    start = [int(val) for val in input("Enter the coordinate of the starting point separated by a space : ").split()]
    goal = [int(val) for val in input("Enter the coordinate of the goal point separated by a space : ").split()]
    max_to_break = int(input("Enter the maximum number of walls allowed to break : "))
    print("\n\n")
    print(find_path(maze, max_to_break, start, goal))
    print("\n\nThe maze is : ")
    print(np.array(maze))
