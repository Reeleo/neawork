
import pygame
import random
import time
pygame.init()


W =360
H = 480


font20 = pygame.font.Font('freesansbold.ttf', 20)
font100 = pygame.font.Font('freesansbold.ttf',100)
WIDTH, HEIGHT = 1472, 960
SPEED = 10
FPS = 40
BLACK = (0,0,0)
WHITE = (255,255,255)
GREY = (100,100,100)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chemistry Game")
clock = pygame.time.Clock()
TIME = time.time()

file = open("saveData1.txt", "r")
line = file.readline()
saveData1 = line.split("/")
file.close



class AreaMap():
    def __init__(self):
        self.posx = 2
        self.posy = 4
        self.store = [[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
            [-1,0,0,0,0,0,0,0,0,0,0,-1],
            [-1,0,0,0,0,0,0,0,0,0,0,-1],
            [-1,0,0,0,0,0,0,0,0,0,0,-1],
            [-1,0,0,0,0,0,0,0,0,0,0,-1],
            [-1,0,0,0,0,0,0,0,0,0,0,-1],
            [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]]
        self.collectStore = [[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
            [-1,0,0,0,0,0,0,0,0,0,0,-1],
            [-1,0,0,0,0,0,0,0,0,0,0,-1],
            [-1,0,0,0,0,0,0,0,0,0,0,-1],
            [-1,0,0,0,0,0,0,0,0,0,0,-1],
            [-1,0,0,0,0,0,0,0,0,0,0,-1],
            [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]]
        self.npcStore = [[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
            [-1,0,0,0,0,0,0,0,0,0,0,-1],
            [-1,0,0,0,0,0,0,0,0,0,0,-1],
            [-1,0,0,0,0,0,0,0,0,0,0,-1],
            [-1,0,0,0,0,0,0,0,0,0,0,-1],
            [-1,0,0,0,0,0,0,0,0,0,0,-1],
            [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]]
    
    def storing(self):
            collectList = []
            if self.collectStore[self.posx][self.posy] == 0:
                for i in range (len(cSprites)):
                    location = [cSprites[i].posx, cSprites[i].posy, 0]
                    if cSprites[i].visible == True:
                        location[2] = 1
                    collectList.append(location)
                self.collectStore[self.posx][self.posy] = collectList
            for j in range(len(cSprites)):
                if cSprites[j].visible == True:
                    self.collectStore[self.posx][self.posy][j][2] = 1
                else:
                    self.collectStore[self.posx][self.posy][j][2] = 0

            npcList = []
            if self.npcStore[self.posx][self.posy] == 0:
                for i in range (len(eSprites)):
                    location = [eSprites[i].posx, eSprites[i].posy, 0]
                    if eSprites[i].visible == True:
                        location[2] = 1
                    npcList.append(location)

                for i in range (len(nSprites)):
                    location = [nSprites[i].posx, nSprites[i].posy, 0]
                    if nSprites[i].visible == True:
                        location[2] = 1
                    npcList.append(location)

                self.npcStore[self.posx][self.posy] = npcList
            for j in range(len(eSprites)):
                if eSprites[j].visible == True:
                    self.npcStore[self.posx][self.posy][j][2] = 1
                else:
                    self.npcStore[self.posx][self.posy][j][2] = 0
            for k in range(len(nSprites)):
                if nSprites[k].visible == True:
                    self.npcStore[self.posx][self.posy][j+len(eSprites)-1][2] = 1

                else:
                    self.npcStore[self.posx][self.posy][j+len(eSprites)-1][2] = 0
            self.store[self.posx][self.posy] = currentMap.skeleton
    
    def loadMap(self,x):
        if x != -1 and not e1.visible:
            self.storing()
            if x == 0:
                self.posy -= 1
            elif x == 1:
                self.posx += 1
            elif x == 2:
                self.posy += 1
            elif x == 3:
                self.posx -= 1

            if self.store[self.posx][self.posy] == 0:
                currentMap.skeleton = currentMap.createMap()
            else:
                currentMap.skeleton = self.store[self.posx][self.posy]

            for k in range (len(cSprites)):
                cSprites[k].generate(k)

            y = random.randint(0,4)
            if y == 1:
                e1.generate()
                chr1.visible = False
            elif y == 2:
                chr1.generate()
                e1.visible  = False
            elif y == 3:
                e1.generate()
                e2.generate()
                chr1.visible  = False
            else:
                e1.visible  = False
                chr1.visible = False
        currentMap.drawMap()

class TileMap():
    def __init__(self):
        self.colour = BLACK
        self.rowLimit = 14
        self.colLimit = 22
        self.sheet = pygame.image.load("forestFloor.bmp")
        # loads in the till sheet to use

    def placeWater(self,skeleton):
        waterTiles = random.randint(2,8)
        row = random.randint(1,self.rowLimit)
        col = random.randint(1,self.colLimit)
        skeleton[row][col] = 4
        tilesPlaced = 1
        while tilesPlaced < waterTiles:
            new = False
            direction = random.randint(0,3)
            if direction == 0 and col > 0:
               if skeleton[row][col-1] != 4:
                col -= 1
            elif direction == 1 and row < self.rowLimit:
               if skeleton[row+1][col] != 4:
                row += 1
            elif direction == 2 and col < self.colLimit:
               if skeleton[row][col+1] != 4:
                col += 1
            elif direction == 3 and row > 0:
               if skeleton[row-1][col] != 4:
                row -= 1
            else:
                new = True
            if new == False:
                skeleton[row][col] = 4
                tilesPlaced += 1
        for i in range(self.colLimit+1):
            skeleton[0][i] = 0
            skeleton[self.rowLimit][i] = 0
        for j in range(self.rowLimit+1):
            skeleton[j][0] = 0
            skeleton[j][self.colLimit] = 0
        return skeleton



    def createMap(self):
        tiles = []
        for i in range(self.rowLimit+1):
            row = []
            for j in range(self.colLimit+1):
                row.append(random.randint(0,1))
            tiles.append(row)
        waterAreas = random.randint(0,3)
        for k in range (waterAreas):
            tiles = self.placeWater(tiles)
        return tiles


    def getTile(self,tileNum, scale):
        # the size of each tile and which tile is being used according to the parameters
        size = 32
        if tileNum == 0:
            xStart = 1
            yStart = 5
        elif tileNum == 1:
            xStart = 5
            yStart = 5
        elif tileNum == 2:
            xStart = 0
            yStart = 1
        elif tileNum == 3:
            xStart = 2
            yStart = 1
        elif tileNum == 4:
            xStart = 3
            yStart = 15
        elif tileNum == 5:
            xStart = 1
            yStart = 1
        else:
            xStart = 0
            yStart = 0
        # creats a surface to display the tile image on selects the tile in the tilesheet
        image = pygame.Surface((size,size)).convert_alpha()
        image.blit(self.sheet,(0,0),((xStart*size),(yStart*size),size,size))
        image = pygame.transform.scale(image,(size*scale,size*scale))
        return image


    def drawMap(self):
        scale = 2
        # for loop to select each tile in the map
        for i in range (len(self.skeleton)):
            for j in range (len(self.skeleton[i])):
                tile = self.getTile(self.skeleton[i][j], scale)
                screen.blit(tile,(j*32*scale,i*32*scale))
                # retrieves the tile and displays it using screen.blit



class ScreenItem():
    def __init__(self,posx,posy,width,height):
        self.colour1 = WHITE
        self.colour2 = RED
        self.text = ""
        self.height = height
        self.width = width
        self.posx = posx
        self.posy = posy
    

class Button(ScreenItem):
    # defines the button's colour, size, position and the text displayed
    def __init__(self,text,posx,posy,height,width):
        super().__init__(posx,posy,height,width)
        self.colour1 = WHITE
        self.colour2 = RED
        self.text = text

    def display(self):
        # displays it as a rectangle on the screen
        pygame.draw.rect(screen,self.colour2,[self.posx-5,self.posy-5,self.width+10,self.height+10])
        pygame.draw.rect(screen,self.colour1,[self.posx,self.posy,self.width,self.height])

        # renders and displays the text
        text1 = font20.render(self.text, True, BLACK)
        textRect = text1.get_rect()
        textRect.center = (self.posx+self.width/2, self.posy+self.height/2)
        screen.blit(text1, textRect)

    def hover(self):
        x = False
        mouse = pygame.mouse.get_pos()
        if self.posx <= mouse[0] <= self.posx + self.width and self.posy <= mouse[1] <= self.posy + self.height:
            pygame.draw.rect(screen,self.colour2,[self.posx,self.posy,self.width,self.height])
            text1 = font20.render(self.text, True, BLACK)
            textRect = text1.get_rect()
            textRect.center = (self.posx+self.width/2, self.posy+self.height/2)
            screen.blit(text1, textRect)
            x = True
        return x

class InputBox(ScreenItem):
    def __init__(self,posx,posy,height,width):
        super().__init__(posx,posy,height,width)

    def display(self):
        pygame.draw.rect(screen,self.colour2,[self.posx-5,self.posy-5,self.width+10,self.height+10])
        pygame.draw.rect(screen,self.colour1,[self.posx,self.posy,self.width,self.height])

        self.processed = font20.render(self.text, True, BLACK)
        textRect = self.processed.get_rect()
        textRect.center = (self.posx+self.width/2, self.posy+self.height/2)
        screen.blit(self.processed, textRect)

    def hover(self):
        x = False
        mouse = pygame.mouse.get_pos()
        if self.posx <= mouse[0] <= self.posx + self.width and self.posy <= mouse[1] <= self.posy + self.height:
            x = True
        return x

class TextBox(ScreenItem):
    def __init__(self,posx,posy,height,width):
        super().__init__(posx,posy,height,width)
        self.visible = False
        self.text = "Hello Jon"
        self.startTime = 0


    def display(self):
        pygame.draw.rect(screen,self.colour2,[self.posx-5,self.posy-5,self.width+10,self.height+10])
        pygame.draw.rect(screen,self.colour1,[self.posx,self.posy,self.width,self.height])

        self.processed = font20.render(self.text, True, BLACK)
        textRect = self.processed.get_rect()
        textRect.center = (self.posx+self.width/2, self.posy+self.height/2)
        screen.blit(self.processed, textRect)

class MiniScreen(ScreenItem):
    def __init__(self,posx,posy,height,width):
        super().__init__(posx,posy,height,width)
        self.text = ""
        self.textx = 0
        self.texty = 0

    def drawScreen(self,x):
        border = pygame.draw.rect(screen, RED, [self.posx-10,self.posy-10, self.width+20, self.height+20])
        inside = pygame.draw.rect(screen, GREY, [self.posx, self.posy, self.width, self.height])
        template = font20.render((self.text), True, BLACK)
        textRect = template.get_rect()
        textRect.center = (self.textx,self.texty)
        if x == "craft":
            middle = pygame.draw.rect(screen, RED, [WIDTH/2-10, 100, 20, HEIGHT-200])
        elif x == "boss":
            smallBorder = pygame.draw.rect(screen, BLACK, [640, 110, 720, 270])
            smallInside = pygame.draw.rect(screen, WHITE, [650, 120, 700, 250])
        screen.blit(template, textRect)




class Sprite(pygame.sprite.Sprite):
    def __init__(self,colour,posx,posy,width,height):
        self.colour = colour
        self.height = height
        self.width = width
        self.posx = posx
        self.posy = posy


    # selecting image from sprite sheet
    def getImage(self,scale,framew,frameh,width,height,colour):
        image = pygame.Surface((width,height)).convert_alpha()
        image.blit(self.sheet,(0,0),((framew*width),(frameh*height),width,height))
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
        super().__init__(BLACK,50,50,W*0.25,H*0.25)
        self.drct = "down"
        self.walk = 1
        self.room = 1
        self.collection = 0

        self.sheet = pygame.image.load("playerSpriteSheet.bmp")
        self.rect = self.sheet.get_rect()
        self.cycle = 0


    def displayStats(self):
        text1 = font20.render(str(self.collection), True, WHITE)
        textRect = text1.get_rect()
        textRect.center = (50,50)
        screen.blit(text1, textRect)

    def updateSprite(self):
        x = 0
        y = 0
        if self.drct == "left":
            y = 1
        elif self.drct == "right":
            y = 2
        elif self.drct == "up":
            y = 3
        elif self.drct == "down":
            y = 0

        x = self.walk // 2
        frame = self.getImage(0.25,x,y,self.width/0.25,self.height/0.25,WHITE)
        screen.blit(frame,(self.posx,self.posy))
        self.cycle = x
        self.displayStats()


    def boundaryCheck(self):
        gap = 10
        x = -1
        if self.posx <= gap and areaMap.store[areaMap.posx-1][areaMap.posy] != -1:
            if not e1.visible:
                self.posx = WIDTH-self.width-gap
                x = 3
        elif self.posx >= WIDTH-self.width and areaMap.store[areaMap.posx+1][areaMap.posy] != -1:
            if not e1.visible:
                self.posx = gap
                x = 1
        elif self.posy <= gap and areaMap.store[areaMap.posx][areaMap.posy-1] != -1:
            if not e1.visible:
                self.posy = HEIGHT-self.height-gap
                x = 0
        elif self.posy >= HEIGHT-self.height and areaMap.store[areaMap.posx][areaMap.posy+1] != -1:
            if not e1.visible:
                self.posy = gap
                x = 2
        else:
            x = -1
        return x


    def move(self,x,y):
        if x == -SPEED and self.posx > self.width/64:
            self.posx += x
            self.drct = "left"
        elif x == SPEED and self.posx < WIDTH-self.width:
            self.posx += x
            self.drct = "right"
        elif y == -SPEED and self.posy > self.height/16:
            self.posy += y
            self.drct = "up"
        elif y == SPEED and self.posy < HEIGHT-self.height:
            self.posy += y
            self.drct = "down"
        self.walk += 1
        if self.walk == 8:
            self.walk = 0


    def movecheck(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and not keys[pygame.K_w] and not keys[pygame.K_s]:
            self.move(-SPEED,0)
        if keys[pygame.K_d] and not keys[pygame.K_w] and not keys[pygame.K_s]:
            self.move(SPEED,0)
        if keys[pygame.K_w]:
            self.move(0,-SPEED)
        if keys[pygame.K_s]:
            self.move(0,SPEED)



class Collectable(Sprite):
    def __init__(self,width,height):
        super().__init__(RED,0,0,width,height)
        self.frameW = 65
        self.frameH = 80
        self.visible = True
        self.sheet = pygame.image.load("plants and rocks.bmp")
        self.rect = self.sheet.get_rect()
        self.pic = random.randint(0,6)


    def collision(self):
        if self.posx-60 < player.posx < self.posx+self.width:
            if self.posy-60 < player.posy < self.posy+self.height+20:
                text1 = font20.render("SPACE", True, WHITE)
                text1Rect = text1.get_rect()
                text1Rect.center = (player.posx+player.width/2, player.posy-20)
                screen.blit(text1, text1Rect)

                keys = pygame.key.get_pressed()
                if keys[pygame.K_SPACE]:
                    self.visible = False
                    player.collection += 1 
    

    def generate(self,i):
        if areaMap.collectStore[areaMap.posx][areaMap.posy] == 0:
            self.visible = True
            self.posx = random.randint(1,currentMap.colLimit-2) * 64
            self.posy = random.randint(1,currentMap.rowLimit-2) * 64
        else:
            self.posx = areaMap.collectStore[areaMap.posx][areaMap.posy][i][0]
            self.posy = areaMap.collectStore[areaMap.posx][areaMap.posy][i][1]
            if areaMap.collectStore[areaMap.posx][areaMap.posy][i][2] == 0:
                self.visible = False
            elif areaMap.collectStore[areaMap.posx][areaMap.posy][i][2] == 1:
                self.visible = True

    def update(self):
        x = 0
        y = 0
        frame = self.getImage(1,x,y,self.frameW,self.frameH,BLACK)
        screen.blit(frame,(self.posx,self.posy))
        self.collision()




class Character(Sprite):
    def __init__(self,width,height):
        super().__init__(BLUE,0,0,width,height)
        self.sheet = pygame.image.load("playerSpriteSheet.bmp")
        self.visible = False
        self.cycle = -1
        self.cont = False
        self.type = "Jonah Magnus"
        self.text = ["Hello, Jon",
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

    def talk(self):
        if self.cont:
            self.cycle += 1
            if self.cycle == len(self.text):
                self.cycle = 0
            tb1.text = self.text[self.cycle]
            tb1.posx = self.posx + self.width/2 - tb1.width/2
            tb1.posy = self.posy - 40
            self.cont = False

    def collision(self):
        x = False
        if self.posx-60 < player.posx < self.posx+self.width:
            if self.posy-60 < player.posy < self.posy+self.height+20:
                text1 = font20.render("SPACE", True, WHITE)
                text1Rect = text1.get_rect()
                text1Rect.center = (player.posx+player.width/2+20, player.posy-20)
                screen.blit(text1, text1Rect)

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
        frame = self.getImage(0.25,x,y,self.width/0.25,self.height/0.25,WHITE)
        screen.blit(frame,(self.posx,self.posy))
        self.collision()



class Boss(Sprite):
    def __init__(self,width,height):
        super().__init__(RED,150,150,width,height)

class Enemy(Sprite):
    def __init__(self,width,height):
        super().__init__(RED,0,0,width,height)
        self.visible = False
        self.sheet = pygame.image.load("playerSpriteSheet.bmp")
        self.drct = "down"
        self.walk = 0
        self.cycle = 0
        self.count = 0
        self.speed = 4
        self.quizTime = False
        self.valid = False
    
    def boundaryCheck(self):
        if self.posx > WIDTH-self.width:
            self.posx = WIDTH-self.width
            self.drct = "left"
            self.count = 0
            x = True
            print("l")
        elif self.posx < 0:
            self.posx = 0
            self.drct = "right"
            self.count = 0
            x = True
            print("r")
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
                self.posx -= self.speed
                print("R")
            elif self.drct == "left":
                self.posx += self.speed
                print("L")
            elif self.drct == "up":
                self.posy -= self.speed
                print("U")
            elif self.drct == "down":
                self.posy += self.speed
                print("D")
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
        if self.walk == 5:
            self.walk = 0



    def quiz(self):
        mini.posx = self.posx - self.width*2
        mini.posy = self.posy - self.height/2
        mini.width = self.width * 5
        mini.height = 50
        mini.drawScreen("")
        if self.valid:
            self.visible = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_e]:
            self.quizTime = False
            self.visible = False



    def collision(self):
        if self.posx-60 < player.posx < self.posx+self.width:
            if self.posy-60 < player.posy < self.posy+self.height+20:
                text1 = font20.render("SPACE", True, WHITE)
                text1Rect = text1.get_rect()
                text1Rect.center = (player.posx+player.width/2+20, player.posy-20)
                screen.blit(text1, text1Rect)

                keys = pygame.key.get_pressed()
                if keys[pygame.K_SPACE]:
                    self.quizTime = True
                    self.quiz()
                
        
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

        x = self.walk // 2
        frame = self.getImage(0.25,x,y,self.width/0.25,self.height/0.25,WHITE)
        screen.blit(frame,(self.posx,self.posy))
        self.cycle = x
        if not self.quizTime:
            self.move()
            self.collision()
        



def screenSetUp(x):
    if x == "boss":
        mini.posx = 100
        mini.posy = 100
        mini.width = WIDTH-200
        mini.height = HEIGHT-200
        mini.text = "FORBIDDEN"
        mini.textx = 1075
        mini.texty = 245
    if x == "craft":
        mini.posx = 100
        mini.posy = 100
        mini.width = WIDTH-200
        mini.height = HEIGHT-200
        mini.text ="+"
        mini.textx = 1000
        mini.texty = 245





def menuScreen():
    cont = 0
    screen.fill(BLACK)
    exitButton.display()
    startButton.display()
    optionsButton.display()

    text1 = font100.render("GAME AAAAAAAA", True, WHITE)
    text1Rect = text1.get_rect()
    text1Rect.center = (WIDTH/2, 200)
    screen.blit(text1, text1Rect)

    exitButton.hover()
    startButton.hover()
    optionsButton.hover()

    pygame.display.update()
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            cont = 1
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                cont = 1
            elif event.key == pygame.K_SPACE:
                cont = 2
        if event.type == pygame.MOUSEBUTTONDOWN:
            if exitButton.hover():
                cont = 2
            elif startButton.hover():
                cont = 3
            elif optionsButton.hover():
                cont = 4
    return cont


def optionsScreen():
    cont = 0
    screen.fill(BLACK)
    menuButton.display()
    menuButton.hover()

    pygame.display.update()
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            cont = 1
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                cont = 1
            elif event.key == pygame.K_SPACE:
                cont = 2
        if event.type == pygame.MOUSEBUTTONDOWN:
            if menuButton.hover():
                cont = 2
    return cont

def pauseScreen():
    cont = 0
    screen.fill(BLACK)
    menuButton.display()
    returnButton.display()
    menuButton.hover()
    returnButton.hover()

    pygame.display.update()
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            cont = 1
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                cont = 1
            elif event.key == pygame.K_z:
                cont = 2
        if event.type == pygame.MOUSEBUTTONDOWN:
            if menuButton.hover():
                cont = 3
            elif returnButton.hover():
                cont = 2
    return cont


def homeScreen():
    cont = 0
    screen.fill(BLACK)

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
                cont = 4
    player.movecheck()
    player.updateSprite()
    pygame.display.update()
    clock.tick(FPS)
    return cont

def craftScreen():
    returnButton.posx = 1150
    returnButton.posy = 750

    b1.posx = 120
    b1.posy = 200
    b1.text = "PLANT"

    b2.posx = 320
    b2.posy = 200
    b2.text = "ROCK"

    b3.posx = 520
    b3.posy = 200
    b3.text = "WATER"

    b4.posx = 1150
    b4.posy = 350
    b4.text = "ENTER"

    cont = 0
    screenSetUp("craft")
    mini.drawScreen()

    returnButton.display()
    b1.display()
    b2.display()
    b3.display()
    b4.display()
    ib1.display()
    ib2.display()
    returnButton.hover()
    b1.hover()
    b2.hover()
    b3.hover()
    b4.hover()

    pygame.display.update()
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            cont = 1
        if event.type == pygame.MOUSEBUTTONDOWN:
            if returnButton.hover():
                cont = 2
            elif b1.hover():
                print("plant")
            elif b2.hover():
                print("rock")
            elif b3.hover():
                print("water")
            elif b4.hover():
                print("enter")
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                cont = 1
            elif event.key == pygame.K_BACKSPACE:
                ib1.text = ib1.text[:-1]
            elif event.key == pygame.K_RETURN:
                userText1 = ib1.text
                ib1.text = ""
            else:
                ib1.text += event.unicode
    return cont


def mapScreen():
    cont = 0
    areaMap.loadMap(player.boundaryCheck())
    if tb1.visible:
        screen.fill(BLACK)

    for i in range(len(cSprites)):
        if cSprites[i].visible and not tb1.visible:
            cSprites[i].update()
    for j in range(len(eSprites)):
        if eSprites[j].visible:
            eSprites[j].update()
            if eSprites[j].quizTime:
                eSprites[j].quiz()
    if chr1.visible:
        chr1.update()
    if tb1.visible:
        tb1.display()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            cont = 1
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                cont = 1
            elif event.key == pygame.K_p:
                cont = 2
            elif event.key == pygame.K_b:
                cont = 3

    if time.time()-TIME >= tb1.startTime + 1:
        chr1.cont = True
    if time.time()-TIME >= tb1.startTime + 3:
        tb1.visible = False
    player.movecheck()
    player.updateSprite()
    pygame.display.update()
    clock.tick(FPS)
    return cont


def bossScreen():
    cont = 0
    screenSetUp("boss")
    mini.drawScreen()
    userText = ""
    exitButton.display()
    b1.display()
    b2.display()
    b3.display()
    b4.display()
    exitButton.hover()
    b1.hover()
    b2.hover()
    b3.hover()
    b4.hover()
    boss1.update()

    pygame.display.update()
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            cont = 1
        if event.type == pygame.MOUSEBUTTONDOWN:
            if exitButton.hover():
                cont = 2
            elif b1.hover():
                print("1")
            elif b2.hover():
                print("2")
            elif b3.hover():
                print("3")
            elif b4.hover():
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
exitButton = Button("EXIT",WIDTH/4-90,3*HEIGHT/4,180,80)
startButton = Button("START",3*WIDTH/4-90,3*HEIGHT/4,180,80)
optionsButton = Button("OPTIONS",WIDTH/2-90,HEIGHT/2,180,80)
returnButton = Button("RETURN",WIDTH/2,3*HEIGHT/4,180,80)
menuButton = Button("MENU",WIDTH/4-90,3*HEIGHT/4,180,80)
b1 = Button("",0,0,180,80)
b2 = Button("",0,0,180,80)
b3 = Button("",0,0,180,80)
b4 = Button("",0,0,180,80)
ib1 = InputBox(800,200,250,80)
ib2 = InputBox(1100,200,250,80)
tb1 = TextBox (0,0,720,25)

# for bosses
qb1 = Button("1",280,80,700,400)
qb2 = Button("2",280,80,1000,400)
qb3 = Button("3",250,80,700,500)
qb4 = Button("4",250,80,1000,500)
mini = MiniScreen(0,0,0,0)


areaMap = AreaMap()
currentMap = TileMap()
c1 = Collectable(50,50)
c2 = Collectable(50,50)
c3 = Collectable(50,50)
c4 = Collectable(50,50)
c5 = Collectable(50,50)
c6 = Collectable(50,50)
cSprites = [c1,c2,c3,c4,c5,c6]
boss1 = Boss(350,650)
e1 = Enemy(W*0.25,H*0.25)
e2 = Enemy(W*0.25,H*0.25)
chr1 = Character(W*0.25,H*0.25)
eSprites = [e1,e2]
nSprites = [chr1]
player = Player()

menu = True
maps = False
boss = False
inHome = False
home = False
craft = False
options = False
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
            running = False
            print("exit")
            break
        elif cont == 3:
            menu = False
            currentMap.skeleton = currentMap.createMap()
            home = True
            print("start")
            break
        elif cont == 4:
            menu = False
            options = True
            print("options")
            break


    while home:
        inHome = True
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
            inHome = False
            for j in range (len(cSprites)):
                cSprites[j].generate(j)
        elif cont == 4:
            home = False
            craft = True

    while craft:
        cont = craftScreen()
        if cont == 1:
            craft = False
            running = False
        elif cont == 2:
            craft = False
            home = True


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
            boss = True

    while boss:
        cont = bossScreen()
        if cont == 1:
            boss = False
            running = False
        elif cont == 2:
            boss = False
            maps = True


    while options:
        cont = optionsScreen()
        if cont == 1:
            options = False
            running = False
        elif cont == 2:
            options = False
            menu = True

    while pause:
        cont = pauseScreen()
        if cont == 1:
            pause = False
            running = False
        elif cont == 2:
            pause = False
            if inHome == True:
                home = True
            elif inHome == False:
                maps = True
        elif cont == 3:
            pause = False
            menu = True



    pygame.display.update()
    clock.tick(FPS)
pygame.quit()











