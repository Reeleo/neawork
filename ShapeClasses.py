import pygame
WHITE = (255,255,255)
RED = (255,0,0)
MINI = (10,50,40)



#---------------PARENT(SHAPE)---------------#
class ScreenConstruct():
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


#---------------INTERACTABLE BOXES---------------#
class Button(ScreenConstruct):
    def __init__(self,pos,size,text,colour):
        super().__init__(pos,size)
        self._colours = [colour,WHITE]
        self._text = text
    
    def get_touch(self):
        return self._touch
    
    def collision(self):
        mouse  = pygame.mouse.get_pos()
        if self._pos[0] <= mouse[0] <= self._pos[0] + self._size[0] and self._pos[1] <= mouse[1] <= self._pos[1] + self._size[1]:
            self._touch = True
            return self._touch
        self._touch = False
        return self._touch



class InputBox(Button):
    def __init__(self,pos,size,text,colour):
        super().__init__(pos,size,text,colour)
        self._takesInput = False
    
    def get_takesInput(self):
        return self._takesInput
    def set_takesInput(self, change):
        self._takesInput = change

    def increase_text(self,txt):
        self._text += txt
    def decrease_text(self):
        self._text = self._text[:-1]



#---------------MINI WINDOW---------------#  
class MiniWindow(ScreenConstruct):
    def __init__(self):
        super().__init__([100,100],[1272,760])
        self._colours = [WHITE, MINI]



#---------------QUICK SCREEN TEXT---------------#
class QuickText(ScreenConstruct):
    def __init__(self,pos,text,startTime):
        super().__init__(pos,[0,0])
        self._visible = True
        self._colours = WHITE
        self._text = text
        self._startTime = startTime
        self._duration = 2
    
    def get_visible(self):
        return self._visible 
    def update(self,time):
        if time - self._startTime > self._duration:
            self._visible = False
            return True
        return False
