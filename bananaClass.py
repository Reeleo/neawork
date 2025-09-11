import pygame

class Banana:
    def __init__(self,x,pos):
        self._sheet = pygame.image.load("image.png")
        self._pos = pos
        self._scale = 0.1
        self._scale = 1
        self._num = x

    def get_pos(self):
        return self._pos 
    
    def get_scale(self):
        return self._scale
    
    def get_num(self):
        return self._num
    
    def get_sheet(self):
        return self._sheet
    
    def set_pos(self,newpos):
        self._pos = newpos

    def grow(self):
        self._pos[0] -= 0.75
        self._pos[1] -= 0.75
        self._scale += 0.01
    
    
        
