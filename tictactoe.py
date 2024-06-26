import sys
import random
import copy
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
class Board:
    def __init__(self):
        self.squares = np.zeros((R,C))
        self.empty_sqrs = self.squares
        self.marked_sqrs = 0
    
    def final(self, show=False):
        #vertical
        for col in range(C):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0:
                if show:
                    color = circColor if self.squares[0][col] == 2 else crossColor
                    iPos = (col * sizeSquare + sizeSquare // 2, 20)
                    fPos = (col * sizeSquare + sizeSquare // 2, H - 20)
                    pygame.draw.line(screen, color, iPos, fPos, lineWidth)
                return self.squares[0][col]
        #horizontal
        for row in range(R):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
                if show:
                    color = circColor if self.squares[row][0] == 2 else crossColor
                    iPos = (20, row * sizeSquare + sizeSquare // 2)
                    fPos = (W - 20, row * sizeSquare + sizeSquare // 2)
                    pygame.draw.line(screen, color, iPos, fPos, lineWidth)
                return self.squares[row][0] 
        #diagonal down
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
            if show:
                color = circColor if self.squares[0][0] == 2 else crossColor
                iPos = (20, 20)
                fPos = (W -20, H - 20)
                pygame.draw.line(screen, color, iPos, fPos, lineWidth)
            return self.squares[0][0]
        #diagonal up
        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] != 0:
            if show:
                color = circColor if self.squares[0][0] == 2 else crossColor
                iPos = (20, H - 20)
                fPos = (W - 20, 20)
                pygame.draw.line(screen, color, iPos, fPos, lineWidth)
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
 
#Level 0 = random ai, level 1 = minmax ai
class AI:
    def __init__(self, level=1, player=2) -> None:
        self.level = level
        self.player = player 
        
    def rnd(self, board):
        empty_sqr = board.getEmptySquares()
        idx = random.randrange(0, len(empty_sqr))
        return empty_sqr[idx]
    
    def minimax(self, board, maximizing:bool):
        case = board.final()
        
        #player 1 wins
        if case == 1:
            return case, None
        #player 2 wins
        if case == 2:
            return -1, None
        #draw
        elif board.isfull():
            return 0, None
        
        if maximizing:
            max_eval = -2
            best_move = None
            empty_sqrs = board.getEmptySquares()
            
            for (row, col) in empty_sqrs:
                temp = copy.deepcopy(board)
                temp.mark(row,col, 1)
                eval = self.minimax(temp, False)[0]
                if eval > max_eval:
                    max_eval = eval
                    best_move = (row, col)
            return max_eval, best_move
                    
        
        elif not maximizing:
            min_eval = 2
            best_move = None
            empty_sqrs = board.getEmptySquares()
            
            for (row, col) in empty_sqrs:
                temp = copy.deepcopy(board)
                temp.mark(row,col, self.player)
                eval = self.minimax(temp, True)[0]
                if eval < min_eval:
                    min_eval = eval
                    best_move = (row, col)
            return min_eval, best_move
                    
        
    def eval(self, mainboard):
        if self.level == 0:
            eval = 'random'
            move = self.rnd(mainboard)
        else:
            eval, move = self.minimax(mainboard, False)
            
        print(f"La IA ha elegido marcar la casilla {move}, con una evaluación de {eval}", sep="")
        return move
class Back:
    
    def __init__(self) -> None:
        self.board = Board()
        self.ai = AI()
        self.player = 1
        self.gamemode = 'ai'
        self.running = True
        self.lines()
    
    def lines(self):
        screen.fill(backgroundColor)
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
    def changeGamemode(self):
        self.gamemode = 'ai' if self.gamemode == 'pvp' else 'pvp'
    
    def reset(self):
        self.__init__()
        
    def isover(self):
        return self.board.final(show=True) != 0 or self.board.isfull()
    
    
    

def main():
    
    game = Back()
    gboard = game.board
    gai = game.ai
    
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                row = pos[1] // sizeSquare
                col = pos[0] // sizeSquare
                if gboard.empty(row,col) and game.running:
                    gboard.mark(row,col, game.player)
                    game.draw_fig(row,col)
                    game.changeplayer()
                    
                    if game.isover():
                        game.running = False
                print(gboard.squares)
                
            if event.type == pygame.KEYDOWN:
                
                if event.key == pygame.K_g:
                    game.changeGamemode()
                    
                if event.key == pygame.K_0:
                    gai.level = 0
                    
                if event.key == pygame.K_1:
                    gai.level = 1
                    
                if event.key == pygame.K_r:
                    game.reset()
                    gboard = game.board
                    gai = game.ai
                
                
        if game.gamemode == 'ai' and game.player == gai.player and game.running:
            pygame.display.update()
            
            row, col = gai.eval(gboard)
            if gboard.empty(row,col):
                gboard.mark(row,col, gai.player)
                game.draw_fig(row,col)
                game.changeplayer()
                if game.isover():
                        game.running = False
            
            
        pygame.display.update()
main()
        
        