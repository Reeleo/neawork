import pygame
import time
WHITE = (255,255,255)
RED = (255,0,0)
GRASS = (0,50,0)


class ScreenShape():
    def __init__(self,pos,size):
        self._pos = pos
        self._size = size
        self._text = ""
        self._colours = [RED,WHITE]
        
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
    def set_text(self,text):
        self._text = text


class TextBox(ScreenShape):
    def __init__(self,pos,size,text,type):
        super().__init__(pos,size)
        self._colours = [RED,WHITE]
        self._text = text
        self._type = type


class Button(ScreenShape):
    def __init__(self,pos,size,text):
        super().__init__(pos,size)
        self._colours = [RED,WHITE]
        self._text = text
        self._touch = False
        self._isInput = False
    
    def get_isInput(self):
        return self._isInput
    def set_isInput(self):
        self._isInput = True
    
    def increase_text(self,txt):
        self._text += txt
    def decrease_text(self):
        self._text = self._text[:-1]

    def collision(self):
        mouse = pygame.mouse.get_pos()
        if self._pos[0] <= mouse[0] <= self._pos[0] + self._size[0] and self._pos[1] <= mouse[1] <= self._pos[1] + self._size[1]:
            self._touch = True
            return self._touch
        self._touch = False
        return self._touch

    def get_touch(self):
        return self._touch
    
    
class MiniWindow(ScreenShape):
    def __init__(self,pos,size):
        super().__init__(pos,size)
        self._colours = [WHITE, GRASS]


class QuickText(ScreenShape):
    def __init__(self,pos,text,startTime):
        super().__init__(pos,[0,0])
        self._visible = True
        self._colours = WHITE
        self._text = text
        self._startTime = startTime
        self._duration = 2
    
    def get_visible(self):
        return self._visible 
    def update(self):
        if time.time() - self._startTime > self._duration:
            self._visible = False
            return True
        return False
