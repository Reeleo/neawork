import pygame
import random
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
BLUE = (0,0,255)


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
    
    def set_posx(self,x):
        self._pos[0] = x
    def set_posy(self,y):
        self._pos[1] = y
    
    def get_image(self,locx,locy,width,height):
        surface = pygame.Surface((width,height))
        surface.blit(self._sheet,(0,0),((locx*width),(locy*height),width,height))
        surface = pygame.transform.scale(surface,(width*self._scale,height*self._scale))
        surface.set_colorkey(self._colour)
        return surface

    def generate(self):
        self.posx = random.randint(1,21) * 64
        self.posy = random.randint(1,13) * 64




class Player(Sprite):
    def __init__(self):
        super().__init__([100,100],[80,80],2.5,WHITE,pygame.image.load("SpriteSheet.bmp"))
        self._drct = "down"
        self._walk = 1
        self.cycle = 0
        self.room = 1
        self._speed = 40
        self.health = 3
        self.collect = {"bct":0,"bug":0,"flw":0,"lef":0,"frt":0,
                        "wpl":0,"srk":0,"brk":0,"vrk":0,"gem":0,
                        "wtr":0,"swt":0}
        self.chemicals = {"C":0,"O2":0,"CO2":0,"H2O":0,"NH3":0,
                      "NaCl":0,"NaBr":0,"CN":0,"Si":0,"S":0,
                      "Mg":0,"Al":0,"Fe":0,"Na":0,"Cl":0,
                      "Br":0,"I":0,"aGlucose":0,"bGlucose":0,"Sucrose":0,
                      "Startch":0,"Cellulose":0,"m":0,"alkane":0,
                      "alkene":0,"alcohol":0,"carAcid":0,
                      "ester":0,"polyester":0,"CloroAlkane":0,
                      "BromoAlkane":0,"amine":0,"amide":0,
                      "AminoAcid":0,"benzene":0,"phenol":0,
                      "acylCloride":0,"acidAnhydride":0,"NaOH":0,"KOH":0,
                      "HCl":0,"HNO3":0,"H2SO4":0,"H3PO4":0}

    def get_speed(self):
        return self._speed
    def set_speed(self,speed,type):
        if type == "inc":
            self._speed += speed
        else:
            self._speed = speed

    def update(self):
        x = 0
        y = 0
        if self._drct == "right":
            y = 1
        elif self._drct == "left":
            y = 2
        elif self._drct == "up":
            y = 3
        elif self._drct == "down":
            y = 0
        x = self._walk // 4
        frame = self.get_image(x,y,self._size[0]/2.5,self._size[1]/2.5)
        return frame


    # def boundaryCheck(self):
    #     gap = 10
    #     x = -1
    #     if self.posx <= gap and areaMap.store[areaMap.pos[0]][areaMap.pos[1]-1] != -1:
    #         if not e1.visible:
    #             self.posx = WIDTH-self.width-gap
    #             x = 3
    #     elif self.posx >= WIDTH-self.width and areaMap.store[areaMap.pos[0]][areaMap.pos[1]+1] != -1:
    #         if not e1.visible:
    #             self.posx = gap
    #             x = 1
    #     elif self.posy <= gap and areaMap.store[areaMap.pos[0]-1][areaMap.pos[1]] != -1:
    #         if not e1.visible:
    #             self.posy = HEIGHT-self.height-gap
    #             x = 0
    #     elif self.posy >= HEIGHT-self.height and areaMap.store[areaMap.pos[0]+1][areaMap.pos[1]] != -1:
    #         if not e1.visible:
    #             self.posy = gap
    #             x = 2
    #     else:
    #         x = -1
    #     self.updateFeet()
    #     return x
    
    

    def move(self,x,y,width,height):
        walking = False
        if x == -self._speed and self._pos[0] > 0:
            self._pos[0] += x
            self._drct = "left"
            walking = True
        if x == self._speed and self._pos[0]+self._size[0] < width:
            self._pos[0] += x
            self._drct = "right"
            walking = True
        if y == -self._speed and self._pos[1] > 0:
            self._pos[1] += y
            self._drct = "up"
            walking = True
        if y == self._speed and self._pos[1]+self._size[1]< height:
            self._pos[1] += y
            self._drct = "down"
            walking = True

        if walking:
            self._walk += 1
            if self._walk == 16:
                self._walk = 0



    def movecheck(self,gameScreen,w,h):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and not keys[pygame.K_w] and not keys[pygame.K_s]:
            self.move(-self._speed,0,w,h)
        if keys[pygame.K_d] and not keys[pygame.K_w] and not keys[pygame.K_s]:
            self.move(self._speed,0,w,h)
        if gameScreen != "home":
            if keys[pygame.K_w]:
                self.move(0,-self._speed,w,h)
            if keys[pygame.K_s]:
                self.move(0,self._speed,w,h)




class Collectable(Sprite):
    def __init__(self,typeNum,pos):
        super().__init__(pos,[50,50],2,BLACK,pygame.image.load("collectablesSprites.bmp"))
        self._frameSize = 50
        self._visible = True
        self.pic = random.randint(0,6)
        self._type = typeNum


    def assign_type(self, gameTypes):
        self._type = gameTypes[self._type]

    def collision(self,playerpos):
        if self._pos[0]-80 < playerpos[0] < self._pos[0]+self._size[0]+40:
            if self._pos[1]-80 < playerpos[1] < self._pos[1]+self._size[1]+40:
                return True
        return False

       
    def update(self,gameScreen,playerpos):
        x = self._type[1]
        y = self._type[2]
        self._scale = 2
        if gameScreen == "home":
            self._scale = 1.5
        image = self.get_image(x,y,50,50)
        collide = self.collision(playerpos)
        return image, collide




# class Character(Sprite):
#     def __init__(self,type):
#         super().__init__(BLUE,0,0,80,80)
#         self.sheet = pygame.image.load("SpriteSheet.bmp")
#         self.visible = False
#         self.cycle = -1
#         self.cont = False
#         self.type = type 
#         if self.type == "Jonah Magnus":
#             self.text = ["Hello"]
   
#         else:
#             self.text = ["Hello",
#                          "Here is a fun fact",
#                          "Aqua Regia is a mixture of highly concentrated acids",
#                          "Specifically HCl and HNO3",
#                          "It is called this due to its ability to dissolve",
#                          "Noble metals such as gold",
#                          "In the second world war it was used for this purpose",
#                          "In order to sustain a nobel prize owned by de Heves",
#                          "And prevent it from being confiscated by Nazis",
#                          "Later the gold was percipitated out and remolded",
#                          "Byebye",
#                          "I have no more facts",
#                          "Byeee",
#                          "Do you want to hear that again?"]

#     def talk(self):
#         gap = 10
#         if self.cont:
#             self.cycle += 1
#             if self.cycle == len(self.text):
#                 self.cycle = 0
#             tb1.text = self.text[self.cycle]
#             tb1.posx = self.posx + self.width/2 - tb1.width/2
#             tb1.posy = self.posy - 40
#             if tb1.posx + tb1.width + gap > WIDTH:
#                 tb1.posx = WIDTH-tb1.width-gap
#             elif tb1.posx - gap < 0:
#                 tb1.posx += gap
#             if tb1.posy + tb1.height + gap > HEIGHT:
#                 tb1.posy = HEIGHT-tb1.height-gap
#             elif tb1.posy - gap < 0:
#                 tb1.posy += gap
#             self.cont = False

#     def collision(self):
#         x = False
#         if self.posx-60 < player.posx < self.posx+self.width:
#             if self.posy-60 < player.posy < self.posy+self.height+20:
#                 displayText("SPACE", font20, WHITE, player.posx+player.width/2, player.posy-20)
#                 keys = pygame.key.get_pressed()
#                 if keys[pygame.K_SPACE]:
#                     self.talk()
#                     x = True
#         if x:
#             tb1.startTime = time.time()-TIME
#             tb1.visible = True        


#     def update(self):
#         x = 0
#         y = 0
#         frame = self.getImage(SCALE,x,y,self.width/SCALE,self.height/SCALE,WHITE)
#         screen.blit(frame,(self.posx,self.posy))
#         self.collision()




# class Enemy(Sprite):
#     def __init__(self):
#         super().__init__(RED,0,0,80,80)
#         self.visible = False
#         self.sheet = pygame.image.load("EnemySpriteSheet.bmp")
#         self.drct = "down"
#         self.walk = 0
#         self.cycle = 0
#         self.count = 0
#         self.speed = 4
#         self.battleTime = False
#         self.valid = False
    
#     def boundaryCheck(self):
#         if self.posx > WIDTH-self.width:
#             self.posx = WIDTH-self.width
#             self.drct = "left"
#             self.count = 0
#             x = True
#         elif self.posx < 0:
#             self.posx = 0
#             self.drct = "right"
#             self.count = 0
#             x = True
#         elif self.posy < 0:
#             self.posy = 0
#             self.drct = "down"
#             self.count = 0
#             x = True
#         elif self.posy > HEIGHT-self.height:
#             self.posy = HEIGHT-self.height
#             self.drct = "up"
#             self.count = 0
#             x = True
#         else:
#             x = False
#         return x


#     def move(self):
#         if self.walk % 2 == 0:
#             if self.drct == "right":
#                 self.posx += self.speed
#             elif self.drct == "left":
#                 self.posx -= self.speed
#             elif self.drct == "up":
#                 self.posy -= self.speed
#             elif self.drct == "down":
#                 self.posy += self.speed
#             self.count += 1
#         hit = self.boundaryCheck()
#         if self.count >= 50 and not hit:
#             self.count = 0
#             x = random.randint(0,3)
#             if x == 0:
#                 self.drct = "right"
#             elif x == 1:
#                 self.drct = "left"
#             elif x == 2:
#                 self.drct = "up"
#             else:
#                 self.drct = "down"
#         self.walk += 1
#         if self.walk == 16:
#             self.walk = 0



#     def battle(self):
#         if self.valid:
#             self.visible = False
#         keys = pygame.key.get_pressed()
#         if keys[pygame.K_e]:
#             self.battleTime = False
#             self.visible = False


#     def collision(self):
#         if self.posx-60 < player.posx < self.posx+self.width:
#             if self.posy-60 < player.posy < self.posy+self.height+20:
#                 displayText("SPACE", font20, WHITE, player.posx+player.width/2, player.posy-20)
#                 keys = pygame.key.get_pressed()
#                 if keys[pygame.K_SPACE]:
#                     self.battleTime = True
#                     self.battle()
                
        
#     def update(self):
#         if self.drct == "right":
#             y = 1
#         elif self.drct == "left":
#             y = 2
#         elif self.drct == "up":
#             y = 3
#         elif self.drct == "down":
#             y = 0
#         else:
#             y = 0

#         x = self.walk // 4
#         frame = self.getImage(2.5,x,y,self.width/2.5,self.height/2.5,WHITE)
#         screen.blit(frame,(self.posx,self.posy))
#         self.cycle = x
#         if not self.battleTime:
#             self.move()
#             self.collision()
        
