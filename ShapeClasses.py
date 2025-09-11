import pygame
import time
WIDTH, HEIGHT = 1472, 960
BLACK, WHITE = (0,0,0), (255,255,255)
GREY = (100,100,100)
RED = (255,0,0)
BURG = (100,0,0)
GREEN = (0,255,0)
GRASS = (0,50,0)
BLUE = (0,0,255)


class ScreenShape():
    def __init__(self,pos,size):
        self._pos = pos
        self._size = size
        self._text = ""
        self._colours = [BLUE,WHITE]
        
    def get_pos(self):
        return self._pos   
    def get_size(self):
        return self._size
    def get_text(self):
        return self._text
    def get_colours(self):
        return self._colours
    
    def set_pos(self,pos):
        self._pos = pos
    def set_size(self,size):
        self._size = size


class Button(ScreenShape):
    def __init__(self,pos,size,text):
        super().__init__(pos,size)
        self._colours = [RED,WHITE]
        self._text = text
        self._touch = False

    def collision(self):
        mouse = pygame.mouse.get_pos()
        if self._pos[0] <= mouse[0] <= self._pos[0] + self._size[0] and self._pos[1] <= mouse[1] <= self._pos[1] + self._size[1]:
            self._touch = True
            return self._touch
        self._touch = False
        return self._touch

    def get_touch(self):
        return self._touch
    

    

class InputBox(ScreenShape):
    def __init__(self,posx,posy,height,width):
        super().__init__([posx,posy],[width,height])

    def display(self):
        pygame.draw.rect(screen,self.colour2,[self.posx-5,self.posy-5,self.width+10,self.height+10])
        pygame.draw.rect(screen,self.colour1,[self.posx,self.posy,self.width,self.height])
        displayText(self.text, font20, BLACK, self.posx+self.width/2, self.posy+self.height/2)
        x = False
        mouse = pygame.mouse.get_pos()
        if self.posx <= mouse[0] <= self.posx + self.width and self.posy <= mouse[1] <= self.posy + self.height:
            x = True
        return x

class TextBox(ScreenShape):
    def __init__(self,posx,posy,height,width):
        super().__init__([posx,posy],[width,height])
        self.visible = False
        self.text = "Hello Jon"
        self.startTime = 0


    def display(self):
        pygame.draw.rect(screen,self.colour2,[self.posx-5,self.posy-5,self.width+10,self.height+10])
        pygame.draw.rect(screen,self.colour1,[self.posx,self.posy,self.width,self.height])
        displayText(self.text, font20, BLACK, self.posx+self.width/2, self.posy+self.height/2)


class MiniWindow(ScreenShape):
    def __init__(self):
        super().__init__([100,100],[WIDTH-200, HEIGHT-200])
        self._colours = [WHITE, GRASS]


class QuickText(ScreenShape):
    def __init__(self):
        super().__init__([0,0],[0,0])
        self._visible = True
        self._colours = WHITE
        self._startTime = 0.0
        self._duration = 2
    
    def get_visible(self):
        return self._visible 
    def set_up(self,text,time):
        self._text = text
        self._startTime = time
        self._visible = True
    
    def update(self):
        if time.time() - self._startTime > self._duration:
            self._visible = False
