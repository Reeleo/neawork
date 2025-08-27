import pygame
import random
import time
pygame.init()

font20 = pygame.font.Font('freesansbold.ttf', 20)
font100 = pygame.font.Font('freesansbold.ttf',100)
WIDTH, HEIGHT = 1472, 960
SCALE = 2.5
FPS = 40
BLACK = (0,0,0)
WHITE = (255,255,255)
GREY = (100,100,100)
RED = (255,0,0)
BURG = (100,0,0)
GREEN = (0,255,0)
GRASS = (0,50,0)
BLUE = (0,0,255)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chemistry Game")
clock = pygame.time.Clock()
TIME = time.time()


 
def displayText(txt, fnt, colour, posx, posy):
    txt = fnt.render(str(txt), True, colour)
    txtrect = txt.get_rect()
    txtrect.center = (posx, posy)
    screen.blit(txt, txtrect)


class GameSettings():
    def __init__(self):
        self.SaveFile = 0
        self.eSpawnRate = 2
        self.diff = "Easy"
        self.screen = "menu"
        self.displayAll = False
        self.collectTypes = [["bct",0,0],["bug",1,0],["flw",0,1],["lef",1,1],["frt",2,1],["wpl",3,1],["srk",0,2],["brk",1,2],["vrk",2,2],["gem",3,2],["wtr",2,0],["swt",3,0]]
        self.itemChances = {"bct":[["C",3],["CO2",2],["m",1],["AminoAcid",1]],
                        "bug":[["C",3],["CO2",2],["AminoAcid",1],["CN",1]],
                        "flw":[["C",2],["O2",2],["AminoAcid",1]],
                        "lef":[["C",2],["O2",4],["Startch",5],["Cellulose",5],["AminoAcid",1]],
                        "frt":[["C",2],["O2",2],["Startch",2],["Sucrose",5],["AminoAcid",1]],
                        "wpl":[["C",5],["O2",4],["Startch",5],["AminoAcid",1]],
                        "srk":[["Si",5],["Fe",1],["Mg",1],["Al",1]],
                        "brk":[["Si",10],["Fe",3],["Mg",3],["Al",3]],
                        "vrk":[["C",5],["S",2],["NH3",2]],
                        "gem":[["C",10],["Si",10],["Mg",5],["Al",5]],
                        "wtr":[["H2O",5],["CO2",3],["O2",4]],
                        "swt":[["H2O",5],["CO2",3],["O2",4],["NaCl",5],["NaBr",5]]}

    def increaseDiff(self):
        if game.diff == "Easy":
            game.diff = "Medium"
        elif game.diff == "Medium":
            game.diff = "Hard"
        elif game.diff == "Hard":
            game.diff = "Easy"


class AreaMap():
    def __init__(self):
        self.pos = [1,1]
        self.store = []
        self.discovered = []
        self.infoStore = []
        for i in range(10):
            rows = [[],[],[],[]]
            if i == 0 or i == 9:
                for j in range(9):
                    rows[0].append(-1)
                    rows[1].append(-1)
                    rows[2].append(-1)
            else:
                for j in range(9):
                    if j == 0 or j == 8:
                        rows[0].append(-1)
                        rows[1].append(-1)
                        rows[2].append(-1)
                    else:
                        rows[0].append(0)
                        rows[1].append(0)
                        rows[2].append(0)
            self.store.append(rows[0])
            self.discovered.append(rows[1])
            self.infoStore.append(rows[2])
            for k in range(len(self.infoStore)):
                for l in range(len(self.infoStore[k])):
                    self.infoStore[k][l] = []
        self.discovered[self.pos[0]][self.pos[1]] = 1

    def loadMap(self,x):
        scale = 2
        if x != -1:
            if x == 0:
                self.pos[0] -= 1
            elif x == 1:
                self.pos[1] += 1
            elif x == 2:
                self.pos[0] += 1
            elif x == 3:
                self.pos[1] -= 1
            currentMap.skeleton = self.store[self.pos[0]][self.pos[1]]
            for i in range (len(cSprites)):
                cSprites[i].posx = self.infoStore[self.pos[0]][self.pos[1]][i][0]
                cSprites[i].posy = self.infoStore[self.pos[0]][self.pos[1]][i][1]
                cSprites[i].visible = self.infoStore[self.pos[0]][self.pos[1]][i][2]
            self.discovered[self.pos[0]][self.pos[1]] = 1
            print("load")
        currentMap.drawMap(scale)


    def checkWater(self,coord):
        valid = True
        if coord[0] == -1:
            valid = False
        elif self.store[coord[0]][coord[1]][coord[2]][coord[3]] == 3:
            valid = False
        return valid 


    def setWater(self):
        for i in range(random.randint(9,10)):
            waterCount = 0
            start = [-1,-1,-1,-1]
            while not self.checkWater(start):
                start = [random.randint(1,8), random.randint(1,7), 
                        random.randint(0,13), random.randint(0,21)]
            print(start)
            self.store[start[0]][start[1]][start[2]][start[3]] = 3
            try:
                self.store[start[0]][start[1]][start[2]+1][start[3]] = 3
            except:
                pass
            try:
                self.store[start[0]][start[1]][start[2]-1][start[3]] = 3
            except:
                pass
            try:
                self.store[start[0]][start[1]][start[2]][start[3]+1] = 3
            except:
                pass
            try:
                self.store[start[0]][start[1]][start[2]+1][start[3]-1] = 3
            except:
                pass
            # coord = start
            # size = random.randint(5,20)
            # tileCount = 0
            # while tileCount < size:
            #     drct = random.ranint(0,3)
            #     if drct == 0:
            #         try:
            #             coord[2] -= 1
            #         except:
            #             coord[2]

    
    def placeItems(self,row,col):
        for i in range (len(cSprites)):
            self.infoStore[row][col].append([random.randint(1,currentMap.colLimit-2) * 64,random.randint(1,currentMap.rowLimit-2) * 64,True])
    
    def createMap(self):
        for row in range(len(self.store)):
            for col in range(len(self.store[row])):
                if self.store[row][col] != -1:
                    self.store[row][col] = currentMap.generateMap()
                self.placeItems(row,col)
        self.setWater()
        self.loadMap(4)
        print("MAP MADE")


    def drawMiniMap(self, currentMap):
        currentRow, currentCol = self.pos[0], self.pos[1] 
        for row in range(len(self.store)):
            for col in range(len(self.store[row])):
                if self.store[row][col] != -1:
                    if self.discovered[row][col] == 1 or game.displayAll:
                        self.pos[0], self.pos[1] = row, col
                        currentMap.skeleton = self.store[row][col]
                        currentMap.drawMap(0.2)  
        self.pos[0], self.pos[1] = currentRow, currentCol
        currentMap.skeleton = self.store[self.pos[0]][self.pos[1]]
        pass

    


                


class TileMap():
    def __init__(self):
        self.colour = BLACK
        self.rowLimit = 15
        self.colLimit = 23
        self.skeleton = []
        self.sheet = pygame.image.load("grasslandsTiles.bmp")
        # loads in the till sheet to use

    
    def generateMap(self):
        count = 0
        self.skeleton = []
        for i in range(self.rowLimit):
            row = []
            for j in range(self.colLimit):
                row.append(random.randint(0,2))
            self.skeleton.append(row)
            count += 1
        return self.skeleton
            

    def getTile(self,tileNum, scale):
        # the size of each tile and which tile is being used according to the parameters
        size = 32
        if tileNum == 0:
            # grass 1
            xStart = 0
            yStart = 0
        elif tileNum == 1:
            # grass 2 
            xStart = 0
            yStart = 1
        elif tileNum == 2:
            # grass 3
            xStart = 1
            yStart = 1
        elif tileNum == 3:
            # water 1
            xStart = 1 
            yStart = 0
        elif tileNum == 4:
            # water 2
            xStart = 2
            yStart = 0
        elif tileNum == 5:
            # path 1
            xStart = 0
            yStart = 2
        else:
            xStart = 0
            yStart = 0
        # creats a surface to display the tile image on selects the tile in the tilesheet
        image = pygame.Surface((size,size)).convert_alpha()
        image.blit(self.sheet,(0,0),((xStart*size),(yStart*size),size,size))
        image = pygame.transform.scale(image,(size*scale,size*scale))
        return image


    def drawMap(self,scale):
        # for loop to select each tile in the map
        for i in range (len(self.skeleton)):
            for j in range (len(self.skeleton[i])):
                tile = self.getTile(self.skeleton[i][j], scale)
                if scale == 2:
                    screen.blit(tile,(j*32*scale,i*32*scale))
                else:
                    screen.blit(tile,(100+WIDTH*scale*0.5*(areaMap.pos[1]-1)+j*32*scale,100+HEIGHT*scale*0.5*(areaMap.pos[0]-1)+i*32*scale))
                # retrieves the tile and displays it using screen.blit

class WaterRecord():
    def __init__(self):
        tilenum = 0


class ScreenShape():
    def __init__(self,posx,posy,width,height):
        self.colour1 = BLUE
        self.colour2 = WHITE
        self.text = ""
        self.height = height
        self.width = width
        self.posx = posx
        self.posy = posy
    
    def test(self):
        pygame.draw.rect(screen,self.colour1,[self.posx,self.posy,self.width,self.height])

class Button(ScreenShape):
    # defines the button's colour, size, position and the text displayed
    def __init__(self):
        super().__init__(0,0,80,180)
        self.colour1 = WHITE
        self.colour2 = RED
        self.text = "text"

    def update(self):
        # displays it as a rectangle on the screen
        pygame.draw.rect(screen,self.colour2,[self.posx-5,self.posy-5,self.width+10,self.height+10])
        pygame.draw.rect(screen,self.colour1,[self.posx,self.posy,self.width,self.height])

        # renders and displays the text
        displayText(self.text, font20, BLACK, self.posx+self.width/2, self.posy+self.height/2)
        hover = False
        mouse = pygame.mouse.get_pos()
        if self.posx <= mouse[0] <= self.posx + self.width and self.posy <= mouse[1] <= self.posy + self.height:
            pygame.draw.rect(screen,self.colour2,[self.posx,self.posy,self.width,self.height])
            displayText(self.text, font20, BLACK, self.posx+self.width/2, self.posy+self.height/2)
            hover = True
        return hover

    def setSize(self):
        self.width = 180
        self.height = 80
    

class InputBox(ScreenShape):
    def __init__(self,posx,posy,height,width):
        super().__init__(posx,posy,height,width)

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
        super().__init__(posx,posy,height,width)
        self.visible = False
        self.text = "Hello Jon"
        self.startTime = 0


    def display(self):
        pygame.draw.rect(screen,self.colour2,[self.posx-5,self.posy-5,self.width+10,self.height+10])
        pygame.draw.rect(screen,self.colour1,[self.posx,self.posy,self.width,self.height])
        displayText(self.text, font20, BLACK, self.posx+self.width/2, self.posy+self.height/2)


class MiniWindow(ScreenShape):
    def __init__(self):
        super().__init__(0,0,0,0)
        self.colour1 = WHITE
        self.colour2 = GRASS

    def drawScreen(self):
        pygame.draw.rect(screen, self.colour1, [self.posx-10, self.posy-10, self.width+20, self.height+20])
        pygame.draw.rect(screen, self.colour2, [self.posx, self.posy, self.width, self.height])


class QuickText():
    def __init__(self):
        self.posx = 0
        self.posy = 0
        self.startTime = 0.0
        self.duration = 2
        self.text = ""
        self.visible = False
        self.colour = WHITE
    
    def update(self):
        if self.visible:
            displayText(self.text,font20,self.colour,self.posx,self.posy)
            if time.time() - self.startTime > self.duration:
                self.visible = False





class Sprite(pygame.sprite.Sprite):
    def __init__(self,colour,posx,posy,width,height):
        self.colour = colour
        self.height = height
        self.width = width
        self.posx = posx
        self.posy = posy


    # selecting image from sprite sheet
    def getImage(self,scale,xloc,yloc,width,height,colour):
        image = pygame.Surface((width,height)).convert_alpha()
        image.blit(self.sheet,(0,0),((xloc*width),(yloc*height),width,height))
        image = pygame.transform.scale(image,(width*scale,height*scale))
        image.set_colorkey(colour)
        return image

    # basic update
    def update(self):
        self.spriteRect = pygame.Rect(self.posx, self.posy, self.width, self.height)
        self.sprite = pygame.draw.rect(screen, self.colour, self.spriteRect)

    def generate(self):
        self.visible = True
        self.posx = random.randint(1,currentMap.colLimit-2) * 64
        self.posy = random.randint(1,currentMap.rowLimit-2) * 64




class Player(Sprite):
    def __init__(self):
        super().__init__(BLACK,100,100,80,80)
        self.drct = "down"
        self.walk = 1
        self.room = 1
        self.speed = 40
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
        
        self.sheet = pygame.image.load("SpriteSheet.bmp")
        self.rect = self.sheet.get_rect()
        self.cycle = 0

    def updateSprite(self):
        x = 0
        y = 0
        if self.drct == "right":
            y = 1
        elif self.drct == "left":
            y = 2
        elif self.drct == "up":
            y = 3
        elif self.drct == "down":
            y = 0
        x = self.walk // 4
        frame = self.getImage(SCALE,x,y,self.width/SCALE,self.height/SCALE,WHITE)
        screen.blit(frame,(self.posx,self.posy))
        self.cycle = x
        displayText("", font20, WHITE, 60,60)
        displayText("", font20, RED, 160,60)

    def updateFeet(self):
        leftFoot.posx, leftFoot.posy = player.posx+8*2.5, player.posy+player.height-10
        rightFoot.posx, rightFoot.posy = player.posx+20*2.5, player.posy+player.height-10


    def boundaryCheck(self):
        gap = 10
        x = -1
        if self.posx <= gap and areaMap.store[areaMap.pos[0]][areaMap.pos[1]-1] != -1:
            if not e1.visible:
                self.posx = WIDTH-self.width-gap
                x = 3
        elif self.posx >= WIDTH-self.width and areaMap.store[areaMap.pos[0]][areaMap.pos[1]+1] != -1:
            if not e1.visible:
                self.posx = gap
                x = 1
        elif self.posy <= gap and areaMap.store[areaMap.pos[0]-1][areaMap.pos[1]] != -1:
            if not e1.visible:
                self.posy = HEIGHT-self.height-gap
                x = 0
        elif self.posy >= HEIGHT-self.height and areaMap.store[areaMap.pos[0]+1][areaMap.pos[1]] != -1:
            if not e1.visible:
                self.posy = gap
                x = 2
        else:
            x = -1
        self.updateFeet()
        return x
    
    
    def obstacleCheck(self,xmove,ymove):
        valid = [True,True,True,True]
        return valid


    def move(self,x,y):
        walking = False
        validMove = self.obstacleCheck(x,y)
        if validMove[3]:
            if x == -self.speed and self.posx > 0:
                self.posx += x
                self.drct = "left"
                walking = True
        if validMove[1]:
            if x == self.speed and self.posx+self.width < WIDTH:
                self.posx += x
                self.drct = "right"
                walking = True
        if validMove[0]:
            if y == -self.speed and self.posy > 0:
                self.posy += y
                self.drct = "up"
                walking = True
        if validMove[2]:
            if y == self.speed and leftFoot.posy+leftFoot.height < HEIGHT:
                self.posy += y
                self.drct = "down"
                walking = True
        if walking:
            self.walk += 1
            if self.walk == 16:
                self.walk = 0
        self.updateFeet()



    def movecheck(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and not keys[pygame.K_w] and not keys[pygame.K_s]:
            self.move(-self.speed,0)
        if keys[pygame.K_d] and not keys[pygame.K_w] and not keys[pygame.K_s]:
            self.move(self.speed,0)
        if game.screen != "home":
            if keys[pygame.K_w]:
                self.move(0,-self.speed)
            if keys[pygame.K_s]:
                self.move(0,self.speed)

    
    # def testUpdate(self):
    #     self.spriteRect = pygame.Rect(self.posx, self.posy, self.width, self.height)
    #     self.sprite = pygame.draw.rect(screen, self.colour, self.spriteRect)



class Collectable(Sprite):
    def __init__(self,typeNum):
        super().__init__(RED,0,0,50,50)
        self.frameW = 50
        self.frameH = 50
        self.visible = True
        self.sheet = pygame.image.load("collectablesSprites.bmp")
        self.rect = self.sheet.get_rect()
        self.pic = random.randint(0,6)
        self.type = game.collectTypes[typeNum]
  


    def collision(self):
        if self.posx-80 < player.posx < self.posx+self.width+40:
            if self.posy-80 < player.posy < self.posy+self.height+40:
                displayText("SPACE", font20, WHITE, player.posx+player.width/2, player.posy-20)
                keys = pygame.key.get_pressed()
                if keys[pygame.K_SPACE]:
                    self.visible = False
                    player.collect[self.type[0]] += 1 

    def update(self):
        x = self.type[1]
        y = self.type[2]
        scale = 2
        if game.screen == "home":
            scale = 1.5
        frame = self.getImage(scale,x,y,self.frameW,self.frameH,BLACK)
        screen.blit(frame,(self.posx,self.posy))
        self.collision()






class Character(Sprite):
    def __init__(self,type):
        super().__init__(BLUE,0,0,80,80)
        self.sheet = pygame.image.load("SpriteSheet.bmp")
        self.visible = False
        self.cycle = -1
        self.cont = False
        self.type = type 
        if self.type == "Jonah Magnus":
            self.text = ["Hello, ",
            "Apologies for the deception",
            "But I wanted to make sure you started reading",
            "So I thought it best not to announce myself",
            "Im assuming youre alone", 
            "You always did prefer to read your statements in private", 
            "I wouldnt try too hard to stop reading",
            "Theres every likelihood youll just hurt yourself",
            "So just listen",
            "Statement of Jonah Magnus regarding Jonathan Sims",
            "The Archivist",
            "Statement begins",
            "I hope youll forgive me the self-indulgence",
            "But I have worked so very hard for this moment",
            "A culmination of two centuries of work", 
            "Its rare that you get the chance to monologue through another",
            "And you cant tell me youre not curious",
            "Why does a man seek to destroy the world?",
            "Its a simple enough answer: for immortality and power.",
            "Uninspired, perhaps, but, my god. The discovery", 
            "Not simply of the dark and horrible reality of the world in which you live",
            "But that you would quite willingly doom that world",
            "And confine the billions in it to an eternity of terror and suffering",
            "All to ensure your own happiness",
            "To place yourself beyond pain and death and fear",
            "It is an awful thing to know about yourself", 
            "But the freedom, John, the freedom of it all", 
            "I have dedicated my life to handing the world to these Dread Powers",
            "all for my own gain", 
            "and I feel… nothing but satisfaction in that choice.",
            "I am to be a king of a ruined world, and I shall never die."]
        else:
            self.text = ["Hello",
                         "Here is a fun fact",
                         "Aqua Regia is a mixture of highly concentrated acids",
                         "Specifically HCl and HNO3",
                         "It is called this due to its ability to dissolve",
                         "Noble metals such as gold",
                         "In the second world war it was used for this purpose",
                         "In order to sustain a nobel prize owned by de Heves",
                         "And prevent it from being confiscated by Nazis",
                         "Later the gold was percipitated out and remolded",
                         "Byebye",
                         "I have no more facts",
                         "Byeee",
                         "Do you want to hear that again?"]

    def talk(self):
        gap = 10
        if self.cont:
            self.cycle += 1
            if self.cycle == len(self.text):
                self.cycle = 0
            tb1.text = self.text[self.cycle]
            tb1.posx = self.posx + self.width/2 - tb1.width/2
            tb1.posy = self.posy - 40
            if tb1.posx + tb1.width + gap > WIDTH:
                tb1.posx = WIDTH-tb1.width-gap
            elif tb1.posx - gap < 0:
                tb1.posx += gap
            if tb1.posy + tb1.height + gap > HEIGHT:
                tb1.posy = HEIGHT-tb1.height-gap
            elif tb1.posy - gap < 0:
                tb1.posy += gap
            self.cont = False

    def collision(self):
        x = False
        if self.posx-60 < player.posx < self.posx+self.width:
            if self.posy-60 < player.posy < self.posy+self.height+20:
                displayText("SPACE", font20, WHITE, player.posx+player.width/2, player.posy-20)
                keys = pygame.key.get_pressed()
                if keys[pygame.K_SPACE]:
                    self.talk()
                    x = True
        if x:
            tb1.startTime = time.time()-TIME
            tb1.visible = True        


    def update(self):
        x = 0
        y = 0
        frame = self.getImage(SCALE,x,y,self.width/SCALE,self.height/SCALE,WHITE)
        screen.blit(frame,(self.posx,self.posy))
        self.collision()



class Boss(Sprite):
    def __init__(self,width,height):
        super().__init__(RED,150,150,width,height)

class Enemy(Sprite):
    def __init__(self):
        super().__init__(RED,0,0,80,80)
        self.visible = False
        self.sheet = pygame.image.load("EnemySpriteSheet.bmp")
        self.drct = "down"
        self.walk = 0
        self.cycle = 0
        self.count = 0
        self.speed = 4
        self.battleTime = False
        self.valid = False
    
    def boundaryCheck(self):
        if self.posx > WIDTH-self.width:
            self.posx = WIDTH-self.width
            self.drct = "left"
            self.count = 0
            x = True
        elif self.posx < 0:
            self.posx = 0
            self.drct = "right"
            self.count = 0
            x = True
        elif self.posy < 0:
            self.posy = 0
            self.drct = "down"
            self.count = 0
            x = True
        elif self.posy > HEIGHT-self.height:
            self.posy = HEIGHT-self.height
            self.drct = "up"
            self.count = 0
            x = True
        else:
            x = False
        return x


    def move(self):
        if self.walk % 2 == 0:
            if self.drct == "right":
                self.posx += self.speed
            elif self.drct == "left":
                self.posx -= self.speed
            elif self.drct == "up":
                self.posy -= self.speed
            elif self.drct == "down":
                self.posy += self.speed
            self.count += 1
        hit = self.boundaryCheck()
        if self.count >= 50 and not hit:
            self.count = 0
            x = random.randint(0,3)
            if x == 0:
                self.drct = "right"
            elif x == 1:
                self.drct = "left"
            elif x == 2:
                self.drct = "up"
            else:
                self.drct = "down"
        self.walk += 1
        if self.walk == 16:
            self.walk = 0



    def battle(self):
        if self.valid:
            self.visible = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_e]:
            self.battleTime = False
            self.visible = False


    def collision(self):
        if self.posx-60 < player.posx < self.posx+self.width:
            if self.posy-60 < player.posy < self.posy+self.height+20:
                displayText("SPACE", font20, WHITE, player.posx+player.width/2, player.posy-20)
                keys = pygame.key.get_pressed()
                if keys[pygame.K_SPACE]:
                    self.battleTime = True
                    self.battle()
                
        
    def update(self):
        if self.drct == "right":
            y = 1
        elif self.drct == "left":
            y = 2
        elif self.drct == "up":
            y = 3
        elif self.drct == "down":
            y = 0
        else:
            y = 0

        x = self.walk // 4
        frame = self.getImage(SCALE,x,y,self.width/SCALE,self.height/SCALE,WHITE)
        screen.blit(frame,(self.posx,self.posy))
        self.cycle = x
        if not self.battleTime:
            self.move()
            self.collision()
        




def screenSetUp(x):
    #1
    if x == "menu":
        b1.posx, b1.posy, b1.text = WIDTH/4-90, 3*HEIGHT/4, "EXIT"
        b2.posx, b2.posy, b2.text = 3*WIDTH/4-90, 3*HEIGHT/4, "START"
        b3.posx, b3.posy, b3.text = WIDTH/2-90, HEIGHT/2, "HOW TO PLAY"
        b1.setSize()
        b2.setSize()
        b3.setSize()
        screen.fill(BURG)
        pygame.draw.rect(screen,RED,[20,20,WIDTH-40, HEIGHT-40])
        pygame.draw.rect(screen,BLACK,[40,40,WIDTH-80, HEIGHT-80])
        for i in range(3):
            buttonTemps[i].update()
        displayText("game", font100, WHITE, WIDTH/2, 200)

    #2
    if x == "htp":
        screen.fill(BURG)
        pygame.draw.rect(screen,RED,[20,20,WIDTH-40, HEIGHT-40])
        pygame.draw.rect(screen,BLACK,[40,40,WIDTH-80, HEIGHT-80])
        b1.posx, b1.posy, b1.text = WIDTH-300, 200, "MENU"
        b1.setSize()

        surface = pygame.Surface((213,146)).convert_alpha()
        surface.blit(pygame.image.load("htpImage.bmp"),(0,0),((0),(0),213,146))
        surface = pygame.transform.scale(surface,(213*6,146*5))
        screen.blit(surface,(100,100))
        for i in range(1):
            buttonTemps[i].update()


    
    #3
    if x == "savefiles":
        screen.fill(BURG)
        pygame.draw.rect(screen,RED,[20,20,WIDTH-40, HEIGHT-40])
        pygame.draw.rect(screen,BLACK,[40,40,WIDTH-80, HEIGHT-80])
        b1.posx, b1.posy, b1.width, b1.height, b1.text = 400, 100, 1000, 150, "Save1"
        b2.posx, b2.posy, b2.width, b2.height, b2.text = 400, 300, 1000, 150, "Save2"
        b3.posx, b3.posy, b3.width, b3.height, b3.text = 400, 500, 1000, 150, "Save3"
        b4.posx, b4.posy, b4.text = WIDTH/4-200, 3*HEIGHT/4, "MENU"
        b4.setSize()
        for i in range(4):
            buttonTemps[i].update()

    #4
    if x == "home":
        screen.fill(BURG)
        player.posy = HEIGHT-200-player.height
        pygame.draw.rect(screen,BLACK,[40, 40, WIDTH-80, HEIGHT-80])
        pygame.draw.rect(screen,BURG,[0, HEIGHT-200, WIDTH, 200])

    #5
    if x == "pause":
        screen.fill(BURG)
        pygame.draw.rect(screen,RED,[20,20,WIDTH-40, HEIGHT-40])
        pygame.draw.rect(screen,BLACK,[40,40,WIDTH-80, HEIGHT-80])
        b1.posx, b1.posy, b1.height, b1.width, b1.text = 900, 250, 80, 80, "+"
        b2.posx, b2.posy, b2.height, b2.width, b2.text = 600, 250, 80, 80, "+"
        b3.posx, b3.posy, b3.height, b3.width, b3.text = 350, 250, 80, 80, str(game.displayAll)
        b4.posx, b4.posy, b4.text = WIDTH/2, 3*HEIGHT/4, "RETURN"
        b5.posx, b5.posy, b5.text = WIDTH/4-90, 3*HEIGHT/4, "MENU"
        b6.posx, b6.posy, b6.text = WIDTH/3+20, 3*HEIGHT/4, "SAVE"
        b4.setSize()
        b5.setSize()
        b6.setSize()
        for i in range(6):
            buttonTemps[i].update()
        displayText(f"Difficulty: {game.diff}", font20, WHITE, 800, 300)
        displayText(f"Speed: {player.speed}", font20, WHITE, 530, 300)
        displayText(f"AllMiniMap: ", font20, WHITE, 280, 300)
    
    #6
    if x == "extract":
        b1.posx, b1.posy, b1.text = 1150, 750, "RETURN"
        b1.posx, b1.posy = 1150, 750
        mini.posx, mini.posy = 100, 100
        mini.width, mini.height = WIDTH-200, HEIGHT-200
        pygame.draw.rect(screen,WHITE,(100,HEIGHT/2-75,WIDTH-200,10))
        mini.drawScreen()
        b1.setSize()
        b1.update()

        displayText("Your Collection:", font20, WHITE, 212, 150)
        for i in range (1,len(buttonTemps)):
            buttonTemps[i].posx, buttonTemps[i].posy = 140+(i-1)*100, 200
            buttonTemps[i].width, buttonTemps[i].height = 80, 80
            buttonTemps[i].text = ""
            buttonTemps[i].update()
        for j in range (len(cSprites)):
            #cSprites[j].type = game.collectTypes[j]
            cSprites[j].visible = True
            cSprites[j].posx, cSprites[j].posy = 140+j*100, 200
            cSprites[j].update()
        x = 210
        y = 310
        displayText(f"BACTERIA: {player.collect["bct"]}", font20, WHITE, x, y)
        displayText(f"BUG: {player.collect["bug"]}", font20, WHITE, x+200, y)
        displayText(f"FLOWER: {player.collect["flw"]}", font20, WHITE, x+400, y)
        displayText(f"LEAF: {player.collect["lef"]}", font20, WHITE, x+600, y)
        displayText(f"FRUIT: {player.collect["frt"]}", font20, WHITE, x+800, y)
        displayText(f"OCEAN PLANT: {player.collect["wpl"]}", font20, WHITE, x+1000, y)
        displayText(f"SMALL ROCK: {player.collect["srk"]}", font20, WHITE, x, y+30)
        displayText(f"BIG ROCK: {player.collect["brk"]}", font20, WHITE, x+200, y+30)
        displayText(f"VOLCANIC ROCK: {player.collect["vrk"]}", font20, WHITE, x+400, y+30)
        displayText(f"GEMSTONE: {player.collect["gem"]}", font20, WHITE, x+600, y+30)

        displayText(f"WATER: {player.collect["wtr"]}", font20, WHITE, x, y+60)
        displayText(f"SEAWATER: {player.collect["swt"]}", font20, WHITE, x+200, y+60)


    
    #7
    if x == "craft":
        b1.posx, b1.posy, b1.text = 1150, 750, "RETURN"
        b1.posx, b1.posy = 1150, 750
        mini.posx, mini.posy = 100, 100
        mini.width, mini.height = WIDTH-200, HEIGHT-200
        pygame.draw.rect(screen,WHITE,(100,HEIGHT/2-75,WIDTH-200,10))
        mini.drawScreen()
        b1.setSize()
        b1.update()

        displayText("Your Chemicals:", font20, WHITE, 212, 150)
        for i in range (1,len(buttonTemps)):
            buttonTemps[i].posx, buttonTemps[i].posy = 140+(i-1)*100, 200
            buttonTemps[i].width, buttonTemps[i].height = 80, 80
            buttonTemps[i].text = ""
            buttonTemps[i].update()

    
    #8
    if x == "map":
        pass
    
    #9
    if x == "minimap":
        mini.posx, mini.posy, mini.width, mini.height = 100, 100, WIDTH-200, HEIGHT-192
        mini.colour1, mini.colour2 = WHITE, GRASS
        b1.posx, b1.posy, b1.text = 1187, 783, "RETURN"
        mini.drawScreen()
        b1.setSize()
        b1.update()
        areaMap.drawMiniMap(currentMap)
        displayText(f"PlayerPosx = {areaMap.pos[1]}",font20,WHITE,1270,130)
        displayText(f"PlayerPosy = {areaMap.pos[0]}",font20,WHITE,1270,160)
        pass

    #12
    if x == "gate":
        pass
    


def eventSetUp(x, spr):
    #10
    if x == "boss":
        mini.posx, mini.posy = 100, 100
        mini.width, mini.height = WIDTH-200, HEIGHT-200
        mini.text = "FORBIDDEN"
        mini.textx, mini.texty = 1075, 245

        # for bosses
        # qb1 = Button("1",280,80,700,400,WHITE,RED)
        # qb2 = Button("2",280,80,1000,400,WHITE,RED)
        # qb3 = Button("3",250,80,700,500,WHITE,RED)
        # qb4 = Button("4",250,80,1000,500,WHITE,RED)

    #11
    if x == "battle":
        screen.fill(BLACK)
        displayText("battle", font100, WHITE, WIDTH/2, 200)
        spr.posx, spr.posy = 100, 200
        player.posx, player.posy = 500, 200


def extraction(item):
    chances = game.itemChances[item]
    chem = chances[random.randint(0,len(chances)-1)][0]
    player.chemicals[chem] += 1
    player.collect[item] -= 1
    print(item, chem, player.chemicals[chem])

    qt.posx, qt.posy, qt.visible = WIDTH/2, 700, True
    qt.text,qt.startTime = f"{item}, {chem}, {player.chemicals[chem]}", time.time()
    return chem
    

def loadGame():
    if game.SaveFile == 1:
        file = open("saveData1.txt","r")
    elif game.SaveFile == 2:
        file = open("saveData2.txt","r")
    elif game.SaveFile == 3:
        file = open("saveData3.txt","r")
    for i in range(4):
        line = file.readline()
        saveData = line.split(",")
        count = 0
        if i == 0:
            for item in player.collect:
                player.collect[item] = int(saveData[count])
                count += 1
        elif i == 1:
            for item in player.chemicals:
                player.chemicals[item] = int(saveData[count])
                count += 1
        elif i == 2:
            game.diff = saveData[0]
        elif i == 3:
            
            player.speed = int(saveData[0])
    



def saveGame():
    if game.SaveFile == 1:
        file = open("saveData1.txt","w")
    elif game.SaveFile == 2:
        file = open("saveData2.txt","w")
    elif game.SaveFile == 3:
        file = open("saveData3.txt","w")
    collectLine = ""
    chemicalLine = ""
    gameLine1 = ""
    gameLine2 = ""
    for item in player.collect:
        collectLine += str(player.collect[item])+","
    for chem in player.chemicals:
        chemicalLine += str(player.chemicals[chem])+","
    gameLine1 += game.diff
    gameLine2 += str(player.speed)
    file.writelines(collectLine)
    file.writelines("\n") 
    file.writelines(chemicalLine)
    file.writelines("\n") 
    file.writelines(gameLine1)
    file.writelines(gameLine2)
    file.close
    print("SAVED")




def menuScreen():
    cont = 0
    # sets up and displays the size and placement of the buttons and text 
    screenSetUp("menu")
    for event in pygame.event.get():
        # cont 1 causes the game to terminate 
        if event.type == pygame.QUIT:
            cont = 1
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                cont = 1
        if event.type == pygame.MOUSEBUTTONDOWN:
            # button.update displays the button 
            # and also returns a value of True if the mouse button is hovering over it  
            if b1.update():
                cont = 1
            elif b2.update():
                cont = 2
                # transfers to the saveFile screen 
            elif b3.update():
                cont = 3
                # transfers to the options screen
    pygame.display.update()
    clock.tick(FPS)
    return cont

def saveFileScreen():
    cont = 0
    screenSetUp("savefiles")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            cont = 1
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                cont = 1
        if event.type == pygame.MOUSEBUTTONDOWN:
            if b1.update():
                game.SaveFile = 1
                loadGame()
                cont = 3
            elif b2.update():
                game.SaveFile = 2
                loadGame()
                cont = 3
            elif b3.update():
                game.SaveFile = 3
                loadGame()
                cont = 3
            elif b4.update():
                cont = 2
    pygame.display.update()
    clock.tick(FPS)
    return cont


def htpScreen():
    cont = 0
    screenSetUp("htp")
    pygame.display.update()
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            cont = 1
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                cont = 1
        if event.type == pygame.MOUSEBUTTONDOWN:
            if b1.update():
                cont = 2
    return cont

def pauseScreen():
    cont = 0
    screenSetUp("pause")
    pygame.display.update()
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            cont = 1
        if event.type == pygame.MOUSEBUTTONDOWN:
            if b1.update():
                game.increaseDiff()
            elif b2.update():
                if player.speed <= 50:
                    player.speed += 5
                else:
                    player.speed = 10
            elif b3.update():
                if game.displayAll:
                    game.displayAll = False
                else:
                    game.displayAll = True
            elif b4.update():
                cont = 2
            elif b5.update():
                cont = 3
            elif b6.update():
                saveGame()
    return cont


def homeScreen():
    cont = 0
    craftTime, extractTime = False, False
    screenSetUp("home")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            cont = 1
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                cont = 1
            elif event.key == pygame.K_p:
                cont = 2
            elif event.key == pygame.K_SPACE:
                cont = 3
            elif event.key == pygame.K_c:
                craftTime = True
            elif event.key == pygame.K_e:
                extractTime  = True

    while craftTime:
        screenSetUp("craft")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                craftTime = False
                cont = 1
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    craftTime = False
                    cont = 1
                elif event.key == pygame.K_SPACE:
                    craftTime = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if b1.update():
                    craftTime = False
        pygame.display.update()
        clock.tick(FPS)

    while extractTime:
        screenSetUp("extract")
        extractItem = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                extractTime = False
                cont = 1
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    extractTime = False
                    cont = 1
                elif event.key == pygame.K_SPACE:
                    extractTime = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if b1.update():
                    extractTime = False
                if b2.update():
                    extractItem = "bct"
                elif b3.update():
                    extractItem = "bug"
                elif b4.update():
                    extractItem = "flw"
                elif b5.update():
                    extractItem = "lef"
                elif b6.update():
                    extractItem = "frt"
                elif b7.update():
                    extractItem = "wpl"
                elif b8.update():
                    extractItem = "srk"
                elif b9.update():
                    extractItem = "brk"
                elif b10.update():
                    extractItem = "vrk"
                elif b11.update():
                    extractItem = "gem"
                elif b12.update():
                    extractItem = "wtr"
                elif b13.update():
                    extractItem = "swt"
        if extractItem != 0:
            extraction(extractItem)
            if player.collect[extractItem] > 0:
                extraction(extractItem)
        qt.update()
        pygame.display.update()
        clock.tick(FPS)

    player.movecheck()
    player.updateSprite()
    pygame.display.update()
    clock.tick(FPS)
    return cont


def battleMode(opponant):
    while opponant.battleTime:
        cont = 0
        eventSetUp("battle",opponant)

        opponant.update()
        opponant.battle()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                cont = 1
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    cont = 1
                elif event.key == pygame.K_p:
                    cont = 4

        player.updateSprite()
        pygame.display.update()
        clock.tick(FPS)
        if cont == 4:
            break
        elif cont != 0:
            opponant.battleTime = False
    return cont

def mapScreen():
    cont = 0
    miniMap = False
    areaMap.loadMap(player.boundaryCheck())
    for i in range(len(cSprites)):
        if cSprites[i].visible and not tb1.visible:
            cSprites[i].update()
    for j in range(len(eSprites)):
        if eSprites[j].visible:
            eSprites[j].update()
            if eSprites[j].battleTime:
                cont = battleMode(eSprites[j])
    if chr1.visible:
        chr1.update()
    if tb1.visible:
        tb1.display()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            cont = 1
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                cont = 3
            elif event.key == pygame.K_p:
                cont = 2
            elif event.key == pygame.K_m:
                miniMap = True
                screen.fill(BLACK)
                screenSetUp("minimap")

    if time.time()-TIME >= tb1.startTime + 0.5:
        chr1.cont = True
    if time.time()-TIME >= tb1.startTime + 2:
        tb1.visible = False

    while miniMap:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                miniMap = False
                cont = 1
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    miniMap = False
                    cont = 1
                elif event.key == pygame.K_m:
                    miniMap = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if b1.update():
                    miniMap = False
        pygame.display.update()
        clock.tick(FPS)
    player.movecheck()
    player.updateSprite()
    # player.testUpdate()
    # leftFoot.test()
    # rightFoot.test()
    pygame.display.update()
    clock.tick(FPS)
    return cont


def bossScreen():
    cont = 0
    eventSetUp("boss","")
    mini.drawScreen()
    userText = ""
    for i in range(4):
        buttonTemps[i].update()
    exitButton.update()
    boss1.update()

    pygame.display.update()
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            cont = 1
        if event.type == pygame.MOUSEBUTTONDOWN:
            if exitButton.update():
                cont = 2
            elif b1.update():
                print("1")
            elif b2.update():
                print("2")
            elif b3.update():
                print("3")
            elif b4.update():
                print("4")
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                cont = 1
            elif event.key == pygame.K_BACKSPACE:
                ib1.text = ib1.text[:-1]
            elif event.key == pygame.K_RETURN:
                userText = ib1.text
                ib1.text = ""
            else:
                ib1.text += event.unicode
    return cont





# button presets
b1 = Button()
b2 = Button()
b3 = Button()
b4 = Button()
b5 = Button()
b6 = Button()
b7 = Button()
b8 = Button()
b9 = Button()
b10 = Button()
b11 = Button()
b12 = Button()
b13 = Button()
buttonTemps = [b1,b2,b3,b4,b5,b6,b7,b8,b9,b10,b11,b12,b13]
tb1 = TextBox (0,0,720,25)
mini = MiniWindow()
qt = QuickText()


player = Player()
game = GameSettings()

areaMap = AreaMap()
currentMap = TileMap()
c1 = Collectable(0)
c2 = Collectable(1)
c3 = Collectable(2)
c4 = Collectable(3)
c5 = Collectable(4)
c6 = Collectable(5)
c7 = Collectable(6)
c8 = Collectable(7)
c9 = Collectable(8)
c10 = Collectable(9)
c11 = Collectable(10)
c12 = Collectable(11)
cSprites = [c1,c2,c3,c4,c5,c6,c7,c8,c9,c10,c11,c12]
for i in range(len(cSprites)):
    print(cSprites[i].type)

e1 = Enemy()
e2 = Enemy()
eSprites = [e1,e2]

chr1 = Character("Normal")
chr2 = Character("Jonah Magnus")
nSprites = [chr1]



leftFoot = ScreenShape(player.posx,player.posx,10,10)
rightFoot = ScreenShape(player.posy,player.posy,10,10)


menu = True
htp = False
loadfile = False
home = False
maps = False
pause = False
running = True
while running:
    while menu:
        cont = menuScreen()
        if cont == 1:
            menu = False
            running = False
            print("END")
            break
        elif cont == 2:
            menu = False
            loadfile = True
            print("saves")
            break
        elif cont == 3:
            menu = False
            htp = True
            print("options")
            break

    while htp:
        cont = htpScreen()
        if cont == 1:
            htp = False
            running = False
        elif cont == 2:
            htp = False
            menu = True

    while loadfile:
        cont = saveFileScreen()
        if cont == 1:
            loadfile = False
            running = False
        elif cont == 2:
            loadfile = False
            menu = True
        elif cont == 3:
            loadfile = False
            home = True
            game.screen = "home"
            player.posx = 100

    while home:
        cont = homeScreen()
        if cont == 1:
            home = False
            running = False
        elif cont == 2:
            home = False
            pause = True
        elif cont == 3:
            home = False
            maps = True
            game.screen = "grassland"
            areaMap.createMap()

    while maps:
        cont = mapScreen()
        if cont == 1:
            maps = False
            running = False
        elif cont == 2:
            maps = False
            pause = True
        elif cont == 3:
            maps = False
            home = True
            game.screen = "home"

    while pause:
        cont = pauseScreen()
        if cont == 1:
            pause = False
            running = False
        elif cont == 2:
            pause = False
            if game.screen == "home":
                home = True
            elif game.screen == "grassland":
                maps = True
        elif cont == 3:
            pause = False
            menu = True


    pygame.display.update()
    clock.tick(FPS)
pygame.quit()