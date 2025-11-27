import pygame
import random
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
BLUE = (0,0,255)


#---------------PARENT(SPRITE)---------------#
class Sprite(pygame.sprite.Sprite):
    def __init__(self,pos,size,scale,colour,sheet):
        self._pos = pos
        self._size = size
        self._visible = True
        self._sheet = sheet
        self._scale = scale
        self._colour = colour

    def get_pos(self):
        return self._pos   
    def get_size(self):
        return self._size
    def get_scale(self):
        return self._scale
    def get_sheet(self):
        return self._sheet
    def get_visible(self):
        return self._visible
    
    def set_pos(self,pos):
        self._pos = pos
    def set_posx(self,x):
        self._pos[0] = x
    def set_posy(self,y):
        self._pos[1] = y
    def set_visible(self,vis):
        self._visible = vis
    
    def generateImage(self,locx,locy,width,height):
        surface = pygame.Surface((width,height))
        surface.blit(self._sheet,(0,0),((locx*width),(locy*height),width,height))
        surface = pygame.transform.scale(surface,(width*self._scale,height*self._scale))
        surface.set_colorkey(self._colour)
        return surface

    def generate(self):
        self.posx = random.randint(1,21) * 64
        self.posy = random.randint(1,13) * 64



#---------------PLAYER---------------#
class Player(Sprite):
    def __init__(self):
        super().__init__([100,100],[80,80],3.5,BLACK,pygame.image.load("SpriteSheet.png"))
        self._drct = "down"
        self._cycle = 1
        self._speed = 20
        self._idle = True
        self._health = 3
        self._hasKey = False
        self._validDrct = [True,True,True,True]
        self._achievements = [False,False]
        self._collect = {"pebble":0,"bug":0,"flower":0,"leaf":0,"fruit":0,
                        "wplant":0,"bush":0,"rock":0,"gem":0,"volrock":0,
                        "freshwater":0,"saltwater":0}
        self._chemicals = {"acylchloride":0,"alcohol":0,"aldehyde":0,"alkane":0,"alkene":0,"aluminium":0,  
                            "amide":0,"amine":0,"aminoacid":0,"ammonia":0,"ammoniumsalt":0,"carbon":0, 
                            "carbondioxide":0,"carboxylicacid":0,"cyanidesalt":0,"ester":0,"glucose":0, 
                            "haloalkane":0,"halogensalt":0,"hydrogen":0,"hydrogenhalide":0,"hydroxynitrile":0, 
                            "hydroxidesalt":0,"iron":0,"ketone":0,"magnesium":0,"nickle":0,"nitrile":0,"oxygen":0, 
                            "potassiumdichromate":0,"silicon":0,"startch":0,"sulfur":0,"sulfurdioxide":0,
                            "sulfuricacid":0,"thionylchloride":0,"water":0}

    def get_speed(self):
        return self._speed
    def get_health(self):
        return self._health
    def get_collect(self):
        return self._collect
    def get_chemicals(self):
        return self._chemicals
    def get_hasKey(self):
        return self._hasKey
    def get_carbonCount(self):
        return self._chemicals["carbon"]
    def get_achievements(self):
        return self._achievements
    
    def set_pos(self,drct,w,h):
        if drct == 0:
            self._pos[1] = h-self._size[1]-20
        elif drct == 1:
            self._pos[0] = 20
        elif drct == 2:
            self._pos[1] = 20
        elif drct == 3:
            self._pos[0] = w-self._size[0]-20
    def set_speed(self,speed,type):
        if type == "inc":
            self._speed += speed
        else:
            self._speed = speed
    def set_collect(self,item,num):
        self._collect[item] = num
    def set_chemicals(self,item,num):
        self._chemicals[item] = num
    def set_validWalk(self,drct,valid):
        if drct == "all":
            self._validDrct = valid
        else:
            self._validDrct[drct] = valid
    def set_hasKey(self):
        self._hasKey = True
        self._achievements[0] = True
    def inc_collect(self,item):
        self._collect[item] += 1
    def dec_chemicals(self,chem):
        self._chemicals[chem] -= 1
    def inc_chemicals(self,chem):
        self._chemicals[chem] += 1
    def set_achievements(self,achieve,i):
        self._achievements[i] = achieve




    def set_extracted(self,item,chem,amount):
        self._collect[item] -= 1
        self._chemicals[chem] += amount
    
    def decrease_health(self):
        self._health -= 1
    def heal_self(self):
        self._health += 1
    def revive_self(self):
        self._health = 3

    def set_int(self):
        self._pos[0] = int(self._pos[0])
        self._pos[1] = int(self._pos[1])
        self._speed = int(self._speed)
    

    
    def updateSprite(self):
        x = 0
        y = 0
        if self._idle:
            x = self._cycle // 8
            frame = self.generateImage(x,0,self._size[0]/2.5,self._size[1]/2.5)
            return frame

        if self._drct == "right":
            y = 3
        elif self._drct == "left":
            y = 4
        elif self._drct == "up":
            y = 2
        elif self._drct == "down":
            y = 1
        x = self._cycle // 8
        frame = self.generateImage(x,y,self._size[0]/2.5,self._size[1]/2.5)
        return frame

    def update(self,gameScreen,w,h):
        self._idle = True
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and not keys[pygame.K_w] and not keys[pygame.K_s]:
            if self._pos[0] > 0 and self._validDrct[3]:
                self._pos[0] -= self._speed
                self._drct = "left"
                self._idle = False
        if keys[pygame.K_d] and not keys[pygame.K_w] and not keys[pygame.K_s]:
            if self._pos[0]+self._size[0] < w and self._validDrct[1]:
                self._pos[0] += self._speed
                self._drct = "right"
                self._idle = False
        if gameScreen != "home":
            if keys[pygame.K_w]:
                if self._pos[1] > 0 and self._validDrct[0]:
                    self._pos[1] -= self._speed
                    self._drct = "up"
                    self._idle = False
            if keys[pygame.K_s]:
                if self._pos[1]+self._size[1]< h and self._validDrct[2]:
                    self._pos[1] += self._speed
                    self._drct = "down"
                    self._idle = False
        self._cycle += 1
        if self._cycle == 32:
            self._cycle = 0
        return self.updateSprite()


        
#---------------COLLECTABLES---------------#
class Collectable(Sprite):
    def __init__(self,pos,typeNum):
        super().__init__(pos,[32,32],2,BLACK,pygame.image.load("collectablesSprites.bmp"))
        self._frameSize = 32
        self._num = typeNum
        self._type = ""


    def get_num(self):
        return self._num
    def assign_type(self, gameTypes):
        self._type = gameTypes[self._num]

    def collision(self,playerpos):
        if self._num == 12:
            if self._pos[0]-100 < playerpos[0] < self._pos[0]+self._size[0]+100:
                return True
        else:
            if self._pos[0]-80 < playerpos[0] < self._pos[0]+self._size[0]+40:
                if self._pos[1]-80 < playerpos[1] < self._pos[1]+self._size[1]+40:
                    return True
        return False
       
    def update(self,gameScreen):
        x = self._type[1]
        y = self._type[2]
        self._scale = 2.5
        if gameScreen == "home":
            self._scale = 2.5
            if self._num == 12:
                self._scale = 5.5
        else:
            if self._num == 0 or self._num == 1 or self._num == 3 or self._num == 4:
                self._scale = 1.5
            elif 5 < self._num < 9:
                self._scale = 3.2
        image = self.generateImage(x,y,32,32)
        return image



#---------------ENEMYS---------------#
class Enemy(Sprite):
    def __init__(self,pos,typeNum,diff):
        super().__init__(pos,[80,80],3.5,BLACK,pygame.image.load("EnemySpriteSheet.png"))
        self._drct = "down"
        self._cycle = 1
        self._battleTime = False
        self._qSet = []
        self._qNum = 0
        self._num = typeNum
        self._validDrct = [True,True,True,True]
        if diff == "Easy":
            self._speed = 3
        elif diff == "Hard":
            self._speed = 5
        else:
            self._speed = 4

    def get_battle(self):
        return self._battleTime
    def get_qSet(self):
        return self._qSet
    def get_qNum(self):
        return self._qNum
    def get_speed(self):
        return self._speed
    def get_num(self):
        return self._num
    
    def set_battle(self,battle):
        self._battleTime = battle
    def set_qSet(self,questions):
        self._qSet = questions
    def set_qNum(self,num):
        if num == "inc":
            self._qNum += 1
        else:
            self._qNum = num
    def set_validWalk(self,drct,valid):
        if drct == "all":
            self._validDrct = valid
        else:
            self._validDrct[drct] = valid
    
    
    
    def updateSprite(self,check):
        x = 0
        y = 0
        if self._drct == "right":
            if not check:
                self._pos[0] += self._speed
            y = 3
        elif self._drct == "left":
            if not check:
                self._pos[0] -= self._speed
            y = 4
        elif self._drct == "up":
            if not check:
                self._pos[1] -= self._speed
            y = 2
        elif self._drct == "down":
            if not check:
                self._pos[1] += self._speed
            y = 1
        x = self._cycle // 8
        frame = self.generateImage(x,y,self._size[0]/2.5,self._size[1]/2.5)
        return frame

    def update(self,playerpos):
        favouredDrct = []
        for i in range(4):
            if i == 0:
                newpos = [self._pos[0],self._pos[1]-self._speed]
                new = [abs(newpos[0]-playerpos[0])+abs(newpos[1]-playerpos[1]),"up"]
            elif i == 1:
                newpos = [self._pos[0]+self._speed,self._pos[1]]
                new = [abs(newpos[0]-playerpos[0])+abs(newpos[1]-playerpos[1]),"right"]
            elif i == 2:
                newpos = [self._pos[0],self._pos[1]+self._speed]
                new = [abs(newpos[0]-playerpos[0])+abs(newpos[1]-playerpos[1]),"down"]
            elif i == 3:
                newpos = [self._pos[0]-self._speed,self._pos[1]]
                new = [abs(newpos[0]-playerpos[0])+abs(newpos[1]-playerpos[1]),"left"]
            favouredDrct.append(new)
            favouredDrct.sort()
        for j in range(len(self._validDrct)):
            if not self._validDrct[j]:
                if j == 0:
                    drct = "up"
                elif j == 1:
                    drct = "right"
                elif j == 2:
                    drct = "down" 
                else:
                    drct = "left"
                for k in range(len(favouredDrct)):
                    if favouredDrct[k][1] == drct:
                        favouredDrct.pop(k)
                        break
        #print(favouredDrct)
        #print(self._validDrct)
        if len(favouredDrct) > 0 :
            change = random.randint(0,10)
            if 0 < change < 5:
                self._drct = favouredDrct[0][1]


        self._cycle += 1
        if self._cycle == 32:
            self._cycle = 0
        return self.updateSprite(False)



#---------------NON PLAYER CHARACTERS---------------#
class Character(Sprite):
    def __init__(self,pos,type):
        if type == "enemyImage" or type == "boss":
            sheet = pygame.image.load("EnemySpriteSheet.png")
            scale = 20
        elif type == "gate":
            sheet = pygame.image.load("collectablesSprites.bmp")
            scale = 5
        else:
            sheet = pygame.image.load("SpriteSheet.png")
            scale = 3.5
        super().__init__(pos,[80,80],scale,BLACK,sheet)
        self._cycle = 0 
        self._type = type
        self._startTime = 0
        self._pointer = 0
        self._dialogue = ["error","error","error","error"]
        file = open("characterDialogue.txt","r")
        if self._type != "enemyImage" and self._type != "boss" and self._type != "gate":
            for i in range(1,10):
                line = file.readline()
                if i == self._type:
                    self._dialogue = line.split(",")
                    break
            self._dialogue.pop(-1)   
        file.close()


    def get_type(self):
        return self._type
    def get_dialogue(self):
        return self._dialogue[self._pointer]
    def get_timer(self,currentTime):
        return currentTime - self._startTime
    
    def set_timer(self,time):
        self._startTime = time
        self._pointer += 1
        if self._pointer == 3:
            self._pointer = 0
    
    def collision(self,playerpos):
        if self._type == "boss":
            if self._pos[0]-40 < playerpos[0] < self._pos[0]+self._size[0]+400:
                if self._pos[1]-40 < playerpos[1] < self._pos[1]+self._size[1]+500:
                    return True
        else:
            if self._pos[0]-80 < playerpos[0] < self._pos[0]+self._size[0]+40:
                if self._pos[1]-80 < playerpos[1] < self._pos[1]+self._size[1]+40:
                    return True
        return False

    def updateSprite(self):
        x = self._cycle // 8
        if self._type == "enemyImage" or self._type == "boss":
            frame = self.generateImage(x,0,self._size[0]/2.5,self._size[1]/2.5)
        elif self._type == "gate":
            frame = self.generateImage(1,3,32,32)
        else:
            frame = self.generateImage(x,0,self._size[0]/2.5,self._size[1]/2.5)
        return frame

    def update(self):
        if self._type != "gate" or self._type == "gate":
            self._cycle += 1
            if self._cycle == 32:
                self._cycle = 0
        return self.updateSprite()

