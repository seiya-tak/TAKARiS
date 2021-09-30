import sys
from random import randint
import pygame
from pygame.locals import *
import copy

pygame.init()

BLACK, WHITE, GRAY = (0,0,0), (255,255,255),(204,204,204)

SURW,SURH = 720,770
FIEW,FIEH = [120,390],[150,720]
CELL = 30
Txt_x = 99+13*CELL
Hld_y,score_y,Lv_y,Lin_y = 150,350,450,550

crtAxis = [270,120]
nxtAxis = [420,60]
nxt2Axis = [570,60]
hldAxis = [540,250]

FONTSIZE = 36
BLOCKTYPE = [None,'O','I','Z','S','L','J','T']
COLORS = [None,
    [255,255,  0],  #O
    [157,204,224],  #I
    [255,  0,  0],  #Z
    [0  ,255,  0],  #S
    [255,165,  0],  #L
    [0  ,  0,255],  #J
    [204, 51,204]   #T
    ]

SHAPES = [None,
    [[-1,0],[0,0],[-1,-1],[0,-1]],    #O
    [[-1,0],[0,0],[1,0] ,[-2,0]],    #I
    [[-1,-1],[0,0],[1,0] ,[0,-1]],     #Z
    [[-1,0],[0,0],[1,-1] ,[0,-1]],     #S
    [[-1,0],[0,0],[1,0] ,[-1,-1]],    #L
    [[-1,0],[0,0],[1,0] ,[1,-1]],     #J
    [[-1,0],[0,0],[1,0] ,[0,-1]]      #T
    ]

SURFACE = pygame.display.set_mode((SURW, SURH))
pygame.display.set_caption("TAKARiS") 
img1 = pygame.image.load("img1.png")
FPSCLOCK = pygame.time.Clock()

def SURFACE_init():
    HldObj = pygame.font.Font(None, FONTSIZE)
    dispHld = HldObj.render("HOLD", True, WHITE)
    SURFACE.blit(dispHld, (Txt_x,Hld_y))

    scoreObj = pygame.font.Font(None, FONTSIZE)
    dispScore = scoreObj.render("SCORE", True, WHITE)
    SURFACE.blit(dispScore, (Txt_x,score_y))

    lvObj = pygame.font.Font(None, FONTSIZE)
    dispLv = lvObj.render("LEVEL", True, WHITE)
    SURFACE.blit(dispLv, (Txt_x,Lv_y))

    LinObj = pygame.font.Font(None, FONTSIZE)
    dispLin = LinObj.render("LINE", True, WHITE)
    SURFACE.blit(dispLin, (Txt_x,Lin_y))

    pygame.draw.rect(SURFACE, GRAY, (120,SURH-20,CELL*10,CELL))
    pygame.draw.rect(SURFACE, GRAY, (90,120,CELL,SURH))
    pygame.draw.rect(SURFACE, GRAY, (90+CELL*9,120,CELL*2,CELL))
    pygame.draw.rect(SURFACE, GRAY, (120,120,CELL*2,CELL))
    pygame.draw.rect(SURFACE, GRAY, (90+CELL*11,120,CELL,SURH))


class scoreC():
    def __init__(self):
        self.point = 0
        self.font = pygame.font.Font(None, FONTSIZE)
    
    def disp(self, x, y):
        disp_score = self.font.render("{}".format(self.point), True, WHITE)
        SURFACE.blit(disp_score, (x, y))

class BlockC():
    def __init__(self,flag,Axis):
        if flag == True:
            self.typeIdx = randint(1, 7)
        else:
            self.typeIdx = 0
        self.type = copy.deepcopy(BLOCKTYPE[self.typeIdx])
        self.color = copy.deepcopy(COLORS[self.typeIdx])
        self.shape = copy.deepcopy(SHAPES[self.typeIdx])
        self.x ,self.y = Axis
        self.rotate_flag = True
    
    
    def disp(self):
        bound = 2
        if self.type != None:
            for i,j in self.shape:
                blockAxis = [self.x+i*CELL,self.y+j*CELL]
                block1 = pygame.Rect(blockAxis[0], blockAxis[1], CELL, CELL)
                block2 = pygame.Rect(blockAxis[0]+bound, blockAxis[1]+bound, CELL-bound*2, CELL-bound*2)
                pygame.draw.rect(SURFACE,WHITE,block1)
                pygame.draw.rect(SURFACE,self.color,block2)
     

    def rotate(self): 
        flag = self.moveable(3)       
        if self.type == 'O' or self.type == None:
            pass
        else:
            if flag:
                if self.rotate_flag == True:
                    for cells in self.shape:
                        cells[0],cells[1] = cells[1],-1*cells[0]
                    if self.type == 'I' or self.type == 'Z' or self.type == 'S':
                        self.rotate_flag = not self.rotate_flag
                else:
                    for cells in self.shape:
                        cells[0],cells[1] = -1*cells[1],cells[0]
                    self.rotate_flag = not self.rotate_flag
   
    def moveable(self,direction):
        flag = True
        blocks = []
        refShape = copy.deepcopy(self.shape)

        if direction == 3:
            if self.rotate_flag == True:
                for cells in refShape:
                    cells[0],cells[1] = cells[1],-1*cells[0]
            else:
                for cells in refShape:
                    cells[0],cells[1] = -1*cells[1],cells[0]
            
        for i,j in refShape:
            blockAxis = [self.x+i*CELL,self.y+j*CELL]
            blocks.append(blockAxis)
        
        if direction == 0 and max(blocks)[0]+30 > FIEW[1]:
            return False
        elif direction == 1 and min(blocks)[0]-30 < FIEW[0]:
            return False
        elif direction == 2 and max(blocks)[1]+30 > FIEH[1]:
            return False
        elif direction == 3:
            if min(blocks)[0] < FIEW[0] or max(blocks)[0] > FIEW[1]:
                return False

        return flag
    
    def move(self,direction):
        flag = self.moveable(direction)
        if flag:
            if direction == 0:
                self.x += 30
            elif direction == 1:
                self.x -= 30
            elif direction == 2:
                self.y += 30

def hardDrop(self):
    self.y = 720

def main():
    START = True
    running_2 = False
    
    while START:
        pygame.display.update() 
        SURFACE.blit(img1, (0, 0))
        for event in pygame.event.get(): 
            if event.type == KEYDOWN: 
                START = False
                running_2 = True
    
    score,levels,line = scoreC(),scoreC(),scoreC() #scoreの初期化  
    crtBlock ,nxtBlock,nxtBlock2,hldBlock = BlockC(True,crtAxis),BlockC(True,nxtAxis),BlockC(True,nxt2Axis),BlockC(False,hldAxis)
    
    while running_2:
        pygame.display.update() 
        SURFACE.fill(BLACK)
        
        SURFACE_init()
        
        crtBlock.disp()
        nxtBlock.disp()
        nxtBlock2.disp()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                K_prsd= event.key
                if K_prsd == K_DOWN:
                    crtBlock.move(2)
                if K_prsd == K_LEFT:
                    crtBlock.move(1)
                if K_prsd == K_RIGHT:
                    crtBlock.move(0)
                if K_prsd == K_UP:
                    hardDrop(crtBlock)
                if K_prsd == K_SPACE:
                    crtBlock.rotate()
                if K_prsd == K_p:
                    print('pressed P')
        
        score.disp(Txt_x,score_y+55)
        levels.disp(Txt_x,Lv_y+55)
        line.disp(Txt_x,Lin_y+55)



if __name__ == '__main__':
    main()
