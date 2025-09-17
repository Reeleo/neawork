import pygame
import random


class GameSettings():
    def __init__(self):
        self._saveFile = 0
        self.eSpawnRate = 2
        self._diff = "Easy"
        self._screen = "menu"
        self._showAll = True
        self._music = -1
        self._playMusic = False
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
        return self._screen
    def get_saveFile(self):
        return self._saveFile
    def get_showAll(self):
        return self._showAll
    def get_music(self):
        return self._music
    def get_playMusic(self):
        return self._playMusic


    def set_screen(self,screen):
        self._screen = screen
    def set_saveFile(self,file):
        self._saveFile = file
    def set_showAll(self):
        if self._showAll:
            self._showAll = False
        else:
            self._showAll = True
    def set_music(self,track):
        self._music = track
    def set_playMusic(self):
        if self._playMusic:
            self._playMusic = False
        else:
            self._playMusic = True
    
    def increaseDiff(self):
        if self.diff == "Easy":
            self.diff = "Medium"
        elif self.diff == "Medium":
            self.diff = "Hard"
        elif self.diff == "Hard":
            self.diff = "Easy"
    


class AreaMap():
    def __init__(self):
        self._pos = [1,1]
        self._currentMap = []
        self._rowLim = 15
        self._colLim = 23
        self._store = []
        self._discovered = []
        self._infoStore = []
        self._sheet = pygame.image.load("grasslandsTiles.bmp")
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
            self._store.append(rows[0])
            self._discovered.append(rows[1])
            self._infoStore.append(rows[2])
            for k in range(len(self._infoStore)):
                for l in range(len(self._infoStore[k])):
                    self._infoStore[k][l] = []
        self._discovered[self._pos[0]][self._pos[1]] = 1


    def get_pos(self):
        return self._pos
    def get_store(self):
        return self._store
    
    def set_collected(self,itemNum):
        info = self._infoStore[self._pos[0]][self._pos[1]]
        for i in range(len(info)):
            try:
                if info[i][4] == itemNum:
                    print("byebye")
                    self._infoStore[self._pos[0]][self._pos[1]][i][2] = False
            except:
                pass
    

    def get_tile(self,tileNum, scale):
        start = [0,0]
        size = 32
        if tileNum == 0:
            # grass 1
            start = [0,0]
        elif tileNum == 1:
            # grass 2 
            start = [0,1]
        elif tileNum == 2:
            # grass 3
            start = [1,1]
        elif tileNum == 3:
            # water 1
            start = [1,0]
        elif tileNum == 5:
            # path 1
            start = [0,2]
        image = pygame.Surface((size,size))
        image.blit(self._sheet,(0,0),((start[0]*size),(start[1]*size),size,size))
        image = pygame.transform.scale(image,(size*scale,size*scale))
        return image


    def drawMap(self,scale,width,height):
        tiles = []
        for i in range (len(self._currentMap)):
            for j in range (len(self._currentMap[i])):
                tile = self.get_tile(self._currentMap[i][j], scale)
                if scale == 2:
                    tiles.append([tile,[j*32*scale,i*32*scale]])
                else:
                    tiles.append([tile,[100+width*scale*0.5*(self._pos[1]-1)+j*32*scale,100+height*scale*0.5*(self._pos[0]-1)+i*32*scale]])
        return tiles


    def loadMap(self,playerpos,playersize,w,h):
        resetPlayer = -1
        if playerpos[0] <= 10 and self._store[self._pos[0]][self._pos[1]-1] != -1:
                resetPlayer = 3
                self._pos[1] -= 1
        elif playerpos[0] >= w-playersize[0] and self._store[self._pos[0]][self._pos[1]+1] != -1:
                resetPlayer = 1
                self._pos[1] += 1
        elif playerpos[1] <= 10 and self._store[self._pos[0]-1][self._pos[1]] != -1:
                resetPlayer = 0
                self._pos[0] -= 1
        elif playerpos[1] >= h-playersize[1] and self._store[self._pos[0]+1][self._pos[1]] != -1:
                resetPlayer = 2
                self._pos[0] += 1
        self._currentMap = self._store[self._pos[0]][self._pos[1]]
        self._discovered[self._pos[0]][self._pos[1]] = 1
        if self._pos[0] == 1 and self._pos[1] == 7:
            info = "GATE"
        elif self._pos[0] == 8 and self._pos[1] == 7:
            info = "BOSS"
        else:
            info = self._infoStore[self._pos[0]][self._pos[1]]
        return self.drawMap(2,w,h), info, resetPlayer




    def generateMap(self):
        count = 0
        skeleton = []
        for _ in range(self._rowLim):
            row = []
            for _ in range(self._colLim):
                row.append(random.randint(0,2))
            skeleton.append(row)
            count += 1
        return skeleton
    

    def placeItems(self,row,col):
        self._infoStore[row][col].clear()
        collectNum = random.randint(1,5)
        for _ in range(collectNum):
            type = random.randint(0,6)
            self._infoStore[row][col].append([random.randint(1,self._colLim-2)*64, random.randint(1,self._rowLim-2)*64, True, "collect",type])
        enemyNum = random.randint(1,2)
        for _ in range(enemyNum):
            self._infoStore[row][col].append([random.randint(1,self._colLim-2)*64, random.randint(1,self._rowLim-2)*64, True, "enemy"]) 
        charNum = random.randint(0,1)
        for _ in range(charNum):
            self._infoStore[row][col].append([random.randint(1,self._colLim-2)*64, random.randint(1,self._rowLim-2)*64, True, "char"])

    def placePath(self):
        currentTmPos = [1,1]
        pathDrct = random.randint(0,1)
        acrossMap, downMap = False, False
        if pathDrct == 0:
            acrossMap = True
            currentTilePos = [random.randint(0,self._rowLim-1),0]
        else:
            downMap = True
            currentTilePos = [0,random.randint(0,self._rowLim-1)]

        valid = False
        while not valid:
            pathSet  = False
            while not pathSet:
                if currentTilePos[0] >= self._rowLim-1 or currentTilePos[1] >= self._colLim-1:
                    pathSet = True
                self._store[currentTmPos[0]][currentTmPos[1]][currentTilePos[0]][currentTilePos[1]] = 5
                if acrossMap:
                    currentTilePos[1] += 1
                elif downMap:
                    currentTilePos[0] += 1

            if acrossMap:
                currentTmPos[1] += 1
                currentTilePos[1] = 0
            elif downMap:
                currentTmPos[0] += 1
                currentTilePos[0] = 0

            acrossMap, downMap = False, False
            if currentTmPos[0] == 8 and currentTmPos[1] == 7:
                valid = True
            elif currentTmPos[0] == 8:
                acrossMap = True
            elif currentTmPos[1] == 7:
                downMap = True
            else:
                pathDrct = random.randint(0,1)
                if pathDrct == 0:
                    acrossMap = True
                else:
                    downMap = True
            


        

    def placeWater(self):
        waterAreas = random.randint(50,80)
        for _ in range(waterAreas):
            startRow, startCol, starty, startx = random.randint(1,8), random.randint(1,7), random.randint(1,self._rowLim-1), random.randint(1,self._colLim-1)
            while self._store[startRow][startCol][starty][startx] == 3:
                startRow, startCol = random.randint(1,8), random.randint(1,7)
                starty, startx = random.randint(1,self._rowLim-1), random.randint(1,self._colLim-1)
            self._store[startRow][startCol][starty][startx] = 3
            print("START",startRow,startCol,starty,startx)

            size = random.randint(15,25)
            for _ in range(size):
                new = False
                row, col = startRow, startCol 
                y, x = starty, startx
                while self._store[row][col][y][x] == 3 and not new:
                    drct = random.randint(0,3)
                    new = False
                    if drct == 0:
                        if y-1 >= 1:
                            y, x = starty-1, startx
                            new = True
                    elif drct == 1:
                        if x+1 <= self._colLim-1:
                            y, x = starty, startx+1
                            new = True
                    elif drct == 2:
                        if y+1 <= self._rowLim-1:
                            y, x = starty+1, startx
                            new = True
                    elif drct == 3:
                        if x-1 >= 1:
                            y, x = starty, startx-1
                            new = True
                self._store[row][col][y][x] = 3
                starty, startx = y, x
                print("set",y,x)



    def createAreaMap(self):
        for row in range(len(self._store)):
            for col in range(len(self._store[row])):
                if self._store[row][col] != -1:
                    self._store[row][col] = self.generateMap()
                if row == 8 and col == 7:
                    self._infoStore[row][col] = "BOSS"
                elif row == 0 and col == 7:
                    self._infoStore[row][col] = "GATE"
                else:
                    self.placeItems(row,col)
        self.placeWater()
        self.placePath()
        print("MAP MADE")


    def drawMiniMap(self,width,height,showAll):
        tiles = []
        currentCol, currentRow = self._pos[0], self._pos[1] 
        for row in range(len(self._store)):
            for col in range(len(self._store[row])):
                if self._store[row][col] != -1:
                    if self._discovered[row][col] == 1 or showAll:
                        self._pos[0], self._pos[1] = row, col
                        self._currentMap = self._store[row][col]
                        tiles.append(self.drawMap(0.2,width,height))
        self._pos[0], self._pos[1] = currentCol, currentRow
        self._currentMap = self._store[self._pos[0]][self._pos[1]]
        return tiles

    

    
