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

file = open("saveData1.txt", "r")
line = file.readline()
saveData1 = line.split("/")
file.close
 
def displayText(txt, fnt, colour, posx, posy):
    txt = fnt.render(str(txt), True, colour)
    txtrect = txt.get_rect()
    txtrect.center = (posx, posy)
    screen.blit(txt, txtrect)


class GameSettings():
    def __init__(self):
        self.eSpawnRate = 0
        self.diff = "Easy"
        self.screen = "menu"
        self.displayAll = False
    
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
        self.sheet = pygame.image.load("forestFloor.bmp")
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


class ScreenItem():
    def __init__(self,posx,posy,width,height):
        self.colour1 = RED
        self.colour2 = WHITE
        self.text = ""
        self.height = height
        self.width = width
        self.posx = posx
        self.posy = posy
    
    def test(self):
        pygame.draw.rect(screen,self.colour1,[self.posx,self.posy,self.width,self.height])

class Button(ScreenItem):
    # defines the button's colour, size, position and the text displayed
    def __init__(self,text,posx,posy,height,width,c1,c2):
        super().__init__(posx,posy,height,width)
        self.colour1 = c1
        self.colour2 = c2
        self.text = text

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



class InputBox(ScreenItem):
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

class TextBox(ScreenItem):
    def __init__(self,posx,posy,height,width):
        super().__init__(posx,posy,height,width)
        self.visible = False
        self.text = "Hello Jon"
        self.startTime = 0


    def display(self):
        pygame.draw.rect(screen,self.colour2,[self.posx-5,self.posy-5,self.width+10,self.height+10])
        pygame.draw.rect(screen,self.colour1,[self.posx,self.posy,self.width,self.height])
        displayText(self.text, font20, BLACK, self.posx+self.width/2, self.posy+self.height/2)


class MiniScreen(ScreenItem):
    def __init__(self):
        super().__init__(0,0,0,0)
        self.text = ""
        self.textx = 0
        self.texty = 0
        self.colour1 = RED
        self.colour2 = GREY

    def drawScreen(self):
        x = 1
        border = pygame.draw.rect(screen, self.colour1, [self.posx-10,self.posy-10, self.width+20, self.height+20])
        inside = pygame.draw.rect(screen, self.colour2, [self.posx, self.posy, self.width, self.height])
        template = font20.render((self.text), True, BLACK)
        textRect = template.get_rect()
        textRect.center = (self.textx,self.texty)
        screen.blit(template, textRect)




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
        self.collection = 0

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
        displayText(self.collection, font20, WHITE, 60,60)
        displayText(self.room, font20, RED, 160,60)

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
    def __init__(self,width,height):
        super().__init__(RED,0,0,width,height)
        self.frameW = 50
        self.frameH = 50
        self.visible = True
        self.sheet = pygame.image.load("plants and rocks copy.bmp")
        self.rect = self.sheet.get_rect()
        self.pic = random.randint(0,6)


    def collision(self):
        if self.posx-60 < player.posx < self.posx+self.width:
            if self.posy-60 < player.posy < self.posy+self.height+20:
                displayText("SPACE", font20, WHITE, player.posx+player.width/2, player.posy-20)
                keys = pygame.key.get_pressed()
                if keys[pygame.K_SPACE]:
                    self.visible = False
                    player.collection += 1 

    def update(self):
        x = 0
        y = 0
        frame = self.getImage(1,x,y,self.frameW,self.frameH,BLACK)
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
        screen.fill(BURG)
        pygame.draw.rect(screen,RED,[20,20,WIDTH-40, HEIGHT-40])
        pygame.draw.rect(screen,BLACK,[40,40,WIDTH-80, HEIGHT-80])
        exitButton.update()
        startButton.update()
        optionsButton.update()
        displayText("game", font100, WHITE, WIDTH/2, 200)

    #2
    if x == "options":
        screen.fill(BURG)
        pygame.draw.rect(screen,RED,[20,20,WIDTH-40, HEIGHT-40])
        pygame.draw.rect(screen,BLACK,[40,40,WIDTH-80, HEIGHT-80])
        menuButton.update()
        b1.posx, b1.posy = 420, 300
        b2.posx, b2.posy = 420, 200
        b3.posx, b3.posy = 900, 250
        b1.width, b2.width, b3.width = 80, 80, 80
        b1.height, b2.height, b3.height = 80, 80, 80
        b1.text, b2.text, b3.text = "-", "+", "+"
        b1.update()
        b2.update()
        b3.update()
        displayText(f"Enemy spwan rate: {game.eSpawnRate}", font20, WHITE, 300, 300)
        displayText(f"Difficulty: {game.diff}", font20, WHITE, 800, 300)
    
    #3
    if x == "savefiles":
        screen.fill(BURG)
        pygame.draw.rect(screen,RED,[20,20,WIDTH-40, HEIGHT-40])
        pygame.draw.rect(screen,BLACK,[40,40,WIDTH-80, HEIGHT-80])
        menuButton.update()
        b1.posx, b1.posy = 400, 100
        b2.posx, b2.posy = 400, 300
        b3.posx, b3.posy = 400, 500
        b1.width, b2.width, b3.width = 1000, 1000, 1000
        b1.height, b2.height, b3.height = 150, 150, 150
        b1.text, b2.text, b3.text = "Save1", "Save2", "Save3"
        b1.update()
        b2.update()
        b3.update()

    #4
    if x == "home":
        screen.fill(BURG)
        pygame.draw.rect(screen,BLACK,[40, 40, WIDTH-80, HEIGHT-80])
        pygame.draw.rect(screen,BURG,[0, HEIGHT-200, WIDTH, 200])

    #5
    if x == "pause":
        screen.fill(BURG)
        pygame.draw.rect(screen,RED,[20,20,WIDTH-40, HEIGHT-40])
        pygame.draw.rect(screen,BLACK,[40,40,WIDTH-80, HEIGHT-80])
        menuButton.update()
        returnButton.update()
        b3.posx, b3.posy, b3.height, b3.width = 900, 250, 80, 80
        b4.posx, b4.posy, b4.height, b4.width = 600, 250, 80, 80
        b2.posx, b2.posy, b2.height, b2.width = 350, 250, 80, 80
        b3.text = "+"
        b4.text = "+"
        b2.text = str(game.displayAll)
        b3.update()
        b4.update()
        b2.update()
        displayText(f"Difficulty: {game.diff}", font20, WHITE, 800, 300)
        displayText(f"Speed: {player.speed}", font20, WHITE, 530, 300)
        displayText(f"AllMiniMap: ", font20, WHITE, 280, 300)
    
    #6
    if x == "extract":
        pass
        # returnButton.posx, returnButton.posy = 1150, 750
        # b1.posx, b1.posy = 120, 200
        # b1.text = "PLANT"
        # b2.posx, b2.posy = 320, 200
        # b2.text = "ROCK"
        # b3.posx, b3.posy = 520, 200
        # b3.text = "WATER"
        # b4.posx, b4.posy = 1150, 350
        # b4.text = "ENTER"
        # mini.posx, mini.posy = 100, 100
        # mini.width = WIDTH-200
        # mini.height = HEIGHT-200
        # mini.text ="+"
        # mini.textx = 1000
        # mini.texty = 245
        # for i in range(4):
        #     buttonTemps[i].update()
        # ib1.display()
        # ib2.display()
        # returnButton.update()
        # mini.drawScreen()
    
    #7
    if x == "craft":
        pass
        # returnButton.posx, returnButton.posy = 1150, 750
        # b1.posx, b1.posy = 120, 200
        # b1.text = "PLANT"
        # b2.posx, b2.posy = 320, 200
        # b2.text = "ROCK"
        # b3.posx, b3.posy = 520, 200
        # b3.text = "WATER"
        # b4.posx, b4.posy = 1150, 350
        # b4.text = "ENTER"
        # mini.posx, mini.posy = 100, 100
        # mini.width = WIDTH-200
        # mini.height = HEIGHT-200
        # mini.text ="+"
        # mini.textx = 1000
        # mini.texty = 245
        # for i in range(4):
        #     buttonTemps[i].update()
        # ib1.display()
        # ib2.display()
        # returnButton.update()
        # mini.drawScreen()
    
    #8
    if x == "map":
        pass
    
    #9
    if x == "minimap":
        mini.posx, mini.posy = 100, 100
        mini.width = WIDTH-200
        mini.height = HEIGHT-192
        mini.colour1, mini.colour2 = WHITE, GRASS
        mini.text = ""
        returnButton.posx, returnButton.posy = 1187,783
        mini.drawScreen()
        returnButton.update()
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

    #11
    if x == "battle":
        screen.fill(BLACK)
        displayText("battle", font100, WHITE, WIDTH/2, 200)
        spr.posx, spr.posy = 100, 200
        player.posx, player.posy = 500, 200






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
            if exitButton.update():
                cont = 1
            elif startButton.update():
                cont = 2
                # transfers to the saveFile screen 
            elif optionsButton.update():
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
            if menuButton.update():
                cont = 2
            elif b1.update() or b2.update() or b3.update():
                cont = 3
    pygame.display.update()
    clock.tick(FPS)
    return cont


def optionsScreen():
    cont = 0
    screenSetUp("options")
    pygame.display.update()
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            cont = 1
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                cont = 1
        if event.type == pygame.MOUSEBUTTONDOWN:
            if menuButton.update():
                cont = 2
            if b1.update():
                if game.eSpawnRate > 0:
                    game.eSpawnRate -= 1                
            if b2.update():
                if game.eSpawnRate < 2:
                    game.eSpawnRate += 1
            if b3.update():
                game.increaseDiff()
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
            if menuButton.update():
                cont = 3
            elif returnButton.update():
                cont = 2
            elif b3.update():
                game.increaseDiff()
            elif b4.update():
                if player.speed <= 50:
                    player.speed += 5
                else:
                    player.speed = 10
            elif b2.update():
                if game.displayAll:
                    game.displayAll = False
                else:
                    game.displayAll = True
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
                cont = 1
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    cont = 1
                elif event.key == pygame.K_SPACE:
                    craftTime = False
        pygame.display.update()
        clock.tick(FPS)

    while extractTime:
        screenSetUp("extract")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                cont = 1
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    cont = 1
                elif event.key == pygame.K_SPACE:
                    extractTime = False
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
                if returnButton.update():
                    miniMap = False
        pygame.display.update()
        clock.tick(FPS)
    player.movecheck()
    player.updateSprite()
    # player.testUpdate()
    leftFoot.test()
    rightFoot.test()
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
exitButton = Button("EXIT",WIDTH/4-90,3*HEIGHT/4,180,80,WHITE,RED)
startButton = Button("START",3*WIDTH/4-90,3*HEIGHT/4,180,80,WHITE,RED)
optionsButton = Button("OPTIONS",WIDTH/2-90,HEIGHT/2,180,80,WHITE,RED)
returnButton = Button("RETURN",WIDTH/2,3*HEIGHT/4,180,80,WHITE,BURG)
menuButton = Button("MENU",WIDTH/4-90,3*HEIGHT/4,180,80,WHITE,BURG)
b1 = Button("",0,0,180,80,WHITE,RED)
b2 = Button("",0,0,180,80,WHITE,RED)
b3 = Button("",0,0,180,80,WHITE,RED)
b4 = Button("",0,0,180,80,WHITE,RED)
buttonTemps = [b1,b2,b3,b4]
ib1 = InputBox(800,200,250,80)
ib2 = InputBox(1100,200,250,80)
tb1 = TextBox (0,0,720,25)

# for bosses
qb1 = Button("1",280,80,700,400,WHITE,RED)
qb2 = Button("2",280,80,1000,400,WHITE,RED)
qb3 = Button("3",250,80,700,500,WHITE,RED)
qb4 = Button("4",250,80,1000,500,WHITE,RED)
mini = MiniScreen()


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
e1 = Enemy()
e2 = Enemy()
chr1 = Character("Normal")
chr2 = Character("Jonah Magnus")
eSprites = [e1,e2]
nSprites = [chr1]
player = Player()
game = GameSettings()


leftFoot = ScreenItem(player.posx,player.posx,10,10)
rightFoot = ScreenItem(player.posy,player.posy,10,10)


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
        cont = optionsScreen()
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
            player.posx, player.posy = 100, HEIGHT-200-player.height

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