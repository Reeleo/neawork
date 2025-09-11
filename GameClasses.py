import pygame
import random
WIDTH, HEIGHT = 1472, 960
BLACK, WHITE = (0,0,0), (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

class GameSettings():
    def __init__(self):
        self.SaveFile = 0
        self.eSpawnRate = 2
        self.diff = "Easy"
        self._screen = "menu"
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
    
    def get_screen(self):
        return self.screen
    
    def increaseDiff(self):
        if self.diff == "Easy":
            self.diff = "Medium"
        elif self.diff == "Medium":
            self.diff = "Hard"
        elif self.diff == "Hard":
            self.diff = "Easy"
    


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

