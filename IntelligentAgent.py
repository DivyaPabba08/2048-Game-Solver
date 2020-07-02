#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 00:39:05 2020

@author: divya
"""
from BaseAI import BaseAI
import time
vecIndex = [UP, DOWN, LEFT, RIGHT] = range(4)


timeLimit = 0.2

class IntelligentAgent(BaseAI):
    
     def getAvailableCells(self) -> list:
        """ Returns a list of empty cells """
        return [(x,y)
                for x in range(self.size)
                for y in range(self.size)
                if self.map[x][y] == 0]
        
     def updateAlarm(self,currentTime) -> None:
        """ Checks if move exceeded the time limit and updates the alarm """
        if currentTime - self.prevTime > timeLimit:
            self.timeLimitReached = True
 
     def setCellValue(self,grid, pos: tuple, value: int):
        """ Set the value of cell at position pos to value """
        grid.map[pos[0]][pos[1]] = value   
        return grid       
    
     def move(self, direction: int):
        """ Moves the grid in a specified direction """
        if direction == UP:
            return self.moveUD(False)
        if direction == DOWN:
            return self.moveUD(True)
        if direction == LEFT:
            return self.moveLR(False)
        if direction == RIGHT:
            return self.moveLR(True)

     def moveUD(self, down:bool=False)->bool:
        """ Move up or down """
        r = range(self.size -1, -1, -1) if down else range(self.size)

        moved = False

        for j in range(self.size):
            cells = []

            for i in r:
                cell = self.map[i][j]

                if cell != 0:
                    cells.append(cell)

            self.merge(cells)

            for i in r:
                value = cells.pop(0) if cells else 0

                if self.map[i][j] != value:
                    moved = True

                self.map[i][j] = value

        return moved

     def moveLR(self, right:bool=False)->bool:
        """ Move left or right """
        r = range(self.size - 1, -1, -1) if right else range(self.size)

        moved = False

        for i in range(self.size):
            cells = []

            for j in r:
                cell = self.map[i][j]

                if cell != 0:
                    cells.append(cell)

            self.merge(cells)

            for j in r:
                value = cells.pop(0) if cells else 0

                if self.map[i][j] != value:
                    moved = True

                self.map[i][j] = value

        return moved    
     
     def getAvailableMoves(self,grid,dirs = vecIndex):
        availableMoves = []        
        gridCopyUp = grid.clone()
        gridCopyDown=grid.clone()
        gridCopyLeft=grid.clone()
        gridCopyRight=grid.clone()
            
        if gridCopyUp.move(UP):
                availableMoves.append(UP)
        if gridCopyDown.move(DOWN):
                availableMoves.append(DOWN)
        if gridCopyLeft.move(LEFT):
                availableMoves.append(LEFT)
        if gridCopyRight.move(RIGHT):
                availableMoves.append(RIGHT)        

        return availableMoves

     def getMove(self, grid):
        #Function to obtain Intelligent Agent Move through performing Iterative Deepening search Technique
        self.prevTime=time.process_time()
        self.timeLimitReached=False
        alpha= float('-inf')
        beta=float('inf')
        self.max_depth=0
        while self.timeLimitReached==False:
            self.updateAlarm(time.process_time())
            self.max_depth=self.max_depth+1
            intelligentAgentMove = self.maximize(grid,alpha,beta,1)[0]
            if intelligentAgentMove != None:		        
                final_move = intelligentAgentMove		
        return final_move if self.getAvailableMoves(grid) else None		
     
     def minimize(self, grid, alpha, beta,depth):
        #Function to perform minimize
       if grid.getAvailableCells()==[]:
            return (None,self.evaluate(grid))
        
       if depth==self.max_depth:
            return (None,self.evaluate(grid))
        
       (minCell,minUtility) = (None, float('inf'))	
       
        
       availableCells=grid.getAvailableCells()
       for  availableCell in availableCells:
            grid_clone=grid.clone()
            grid_clone = self.setCellValue(grid_clone,availableCell,2)
            utility= self.maximize(grid_clone,alpha,beta,depth+1)[1]
            if utility==None:
                return (None,None) 
            if utility<minUtility:
                (minCell, minUtility) = (availableCell, utility)
            if minUtility <= alpha:
                break
            if minUtility < beta:
                beta = minUtility         
                

       return (minCell, minUtility)
  

     def maximize(self, grid, alpha, beta,depth):
       
        if self.getAvailableMoves(grid)==[] :        #Function to check if its a terminal state
            return (None,self.evaluate(grid))
          
        
        (maxChild,maxUtility) = (None, float('-inf'))			

        for  child in self.getAvailableMoves(grid):
            grid_clone=grid.clone()
            grid_clone.move(child)
            utility= self.minimize(grid_clone,alpha,beta,depth)[1]
            self.updateAlarm(time.process_time())
            if self.timeLimitReached or utility==None:
                return (None, None)
            if utility>maxUtility:
                (maxChild,maxUtility) = (child, utility)			
            if maxUtility >= beta:
                break
            if maxUtility > alpha:
                alpha = maxUtility
    
                
        return  (maxChild,maxUtility)       
        
        

     def evaluate(self, grid):
        w1=1
        available = grid.getAvailableCells()
        return w1*len(available)*grid.getMaxTile()

    