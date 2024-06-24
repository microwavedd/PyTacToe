import sys
import pygame
import numpy as np

#Constants

W,H,R,C = 500,500,3,3
sizeSquare = W // C
backgroundColor = (28,170,156)
lineColor = (23,45,75)
circColor = (239,231,200)
circWidth = 15
radius = sizeSquare // 4
lineWidth = 15
crossColor = (66,66,66)
crossWidth = 20
offset = 50


pygame.init()
screen = pygame.display.set_mode( (W,H) )
pygame.display.set_caption("PyTacToe")
screen.fill(backgroundColor)
class Board:
    def __init__(self):
        self.squares = np.zeros((R,C))
        self.empty_sqrs = self.squares
        self.marked_sqrs = 0
    
    def final(self):
        #vertical
        for col in range(C):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0:
                return self.squares[0][col]
        #horizontal
        for row in range(R):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
                return self.squares[row][0] 
        #diagonal down
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
            return self.squares[0][0]
        #diagonal up
        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] != 0:
            return self.squares[2][0]
        return 0
        
    def mark(self,row,col,player):
        self.squares[row][col] = player
        self.marked_sqrs += 1
        
    def empty(self, row,col):
        return self.squares[row][col] == 0
    
    def isfull(self):
        return self.marked_sqrs == 9
    
    def isempty(self):
        return self.marked_sqrs == 0
    
    def getEmptySquares(self):
        empty_sqrs = []
        for row in range(R):
            for col in range(C):
                if self.empty(row,col):
                    empty_sqrs.append((row,col))
        return empty_sqrs
        
class Back:
    
    def __init__(self) -> None:
        self.board = Board()
        self.player = 1
        self.lines()
    
    def lines(self):
        #vertical
        pygame.draw.line(screen, lineColor, (sizeSquare,0), (sizeSquare, H), lineWidth)
        pygame.draw.line(screen, lineColor, (W*(2/3),0), (W*(2/3), H), lineWidth)
        #horizontal
        pygame.draw.line(screen, lineColor, (0,sizeSquare), (W, sizeSquare), lineWidth)
        pygame.draw.line(screen, lineColor, (0, H*(2/3)), (W, H*(2/3)), lineWidth)
    def changeplayer(self):
        self.player = self.player % 2 + 1
        
    def draw_fig(self,row,col):
        if self.player == 1:
            startDown = (col * sizeSquare + offset, row * sizeSquare + offset)
            endDown = (col * sizeSquare + sizeSquare - offset, row * sizeSquare + sizeSquare - offset)
            pygame.draw.line(screen,crossColor, startDown, endDown, crossWidth)
            startUp = (col * sizeSquare + offset, row * sizeSquare + sizeSquare - offset)
            endUp = (col * sizeSquare + sizeSquare - offset, row * sizeSquare + offset)
            pygame.draw.line(screen,crossColor,startUp,endUp,crossWidth)
        elif self.player == 2:
            center = (col * sizeSquare + sizeSquare // 2, row * sizeSquare + sizeSquare // 2)
            pygame.draw.circle(screen,circColor,center,radius,circWidth)
    

def main():
    
    game = Back()
    gboard = game.board
    
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                row = pos[1] // sizeSquare
                col = pos[0] // sizeSquare
                if gboard.empty(row,col):
                    gboard.mark(row,col, game.player)
                    game.draw_fig(row,col)
                    game.changeplayer()
                print(gboard.squares)
        pygame.display.update()
main()
        
        