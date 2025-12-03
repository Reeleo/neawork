import pygame
import random


#---------------GAME SETTINGS---------------#
class GameSettings():
    def __init__(self):
        self._saveFile = 0
        self._diff = "Easy"
        self._screen = "menu"
        self._showAll = False
        self._music = -1
        self._playMusic = False
        self._showTutorial = True
        self._collectTypes = [["pebble",0,0],["bug",1,0],["flower",0,1],["leaf",1,1],["fruit",2,1],["wplant",3,1],["bush",0,2],["rock",1,2],["gem",2,2],["volrock",3,2],["freshwater",2,0],["saltwater",3,0],["door",1,3]]
        self._itemChances = {"pebble":[["carbon",1]],
                        "bug":[["carbon",1],["cyanidesalt",1],["carboxylicacid",1]], 
                        "flower":[["carbon",1],["amine",1],["alkane",1]], 
                        "leaf":[["carbon",1],["oxygen",1],["ester",1],["aminoacid",1]],
                        "fruit":[["carbon",1],["water",1],["glucose",1],["aminoacid",1]],
                        "wplant":[["carbon",1],["oxygen",1],["ester",1],["water",1],["silicon",1]],
                        "bush":[["carbon",3],["oxygen",1],["ester",1],["aminoacid",1]],
                        "rock":[["carbon",3],["silicon",1],["magnesium",1]],
                        "gem":[["carbon",3],["magnesium",1],["nickel",1]],
                        "volrock":[["carbon",3],["sulfur",1],["ammonia",1]],
                        "freshwater":[["water",3],["carbondioxide",1],["oxygen",1]],
                        "saltwater":[["water",3],["CO2",1],["oxygen",1],["halogensalt",1]]}
        self._battleRewards = ["ammonia","thionylchloride","potassiumdichromate","NaBH4","nickel","hydrogen","alcohol","alkane","alkene","ester",
                               "carbon","oxygen","water","magnesium","halogensalt","carboxylicacid"]

    
    def get_screen(self):
        return self._screen
    def get_saveFile(self):
        return self._saveFile
    def get_showAll(self):
        return self._showAll
    def get_diff(self):
        return self._diff
    def get_music(self):
        return self._music
    def get_playMusic(self):
        return self._playMusic
    def get_tutorial(self):
        return self._showTutorial
    def get_collectTypes(self):
        return self._collectTypes
    def get_itemChances(self):
        return self._itemChances
    def get_rewards(self):
        return self._battleRewards


    def set_screen(self,screen):
        self._screen = screen
    def set_saveFile(self,file):
        self._saveFile = file
    def set_tutorial(self,on):
        self._showTutorial = on
    def set_showAll(self):
        if self._showAll:
            self._showAll = False
        else:
            self._showAll = True
    def set_diff(self,new):
        self._diff = new
    def set_music(self,track):
        self._music = track
    def set_playMusic(self):
        if self._playMusic:
            self._playMusic = False
        else:
            self._playMusic = True
    
    def inc_diff(self):
        if self._diff == "Easy":
            self._diff = "Medium"
        elif self._diff == "Medium":
            self._diff = "Hard"
        elif self._diff == "Hard":
            self._diff = "Easy"
    


#---------------MAPS---------------#
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
    
    def reset(self):
        self._pos = [1,1]
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
    def get_waterPos(self):
        positions = []
        for i in range(len(self._store[self._pos[0]][self._pos[1]])):
            for j in range(len(self._store[self._pos[0]][self._pos[1]][i])):
                if self._store[self._pos[0]][self._pos[1]][i][j] == 5 or self._store[self._pos[0]][self._pos[1]][i][j] == 6:
                    positions.append([i,j])
        return positions

    
    def set_collected(self,itemNum):
        info = self._infoStore[self._pos[0]][self._pos[1]]
        for i in range(len(info)):
            try:
                if info[i][4] == itemNum:
                    self._infoStore[self._pos[0]][self._pos[1]][i][2] = False
            except:
                pass

    

    def generateTile(self,tileNum, scale):
        size = 32
        tile = "empty"
        tileTypes = {"grass1":[0,0],"grass2":[1,1],"grass3":[0,1],"grass4":[2,1],
                    "water1":[1,0],"water2":[2,0],
                    "path1":[0,2],"empty":[1,2]}
        if tileNum == 0:
            tile = "grass1"
        elif tileNum == 1:
            tile = "grass2"
        elif tileNum == 2:
            tile = "grass3"
        elif tileNum == 3:
            tile = "grass4"
        elif tileNum == 5:
            tile = "water1"
        elif tileNum == 6:
            tile = "water2"
        elif tileNum == 7:
            tile = "path1"
        start = tileTypes[tile]
        image = pygame.Surface((size,size))
        image.blit(self._sheet,(0,0),((start[0]*size),(start[1]*size),size,size))
        image = pygame.transform.scale(image,(size*scale,size*scale))
        return image


    def drawMap(self,scale,width,height):
        tiles = []
        for i in range (len(self._currentMap)):
            for j in range (len(self._currentMap[i])):
                tile = self.generateTile(self._currentMap[i][j], scale)
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
                row.append(random.randint(0,1))
            skeleton.append(row)
            count += 1
        return skeleton
    

    def placeItems(self,row,col,maxEnemy):
        count = 0
        collectNum = random.randint(1,5)
        while count < collectNum:
            type = random.randint(0,8)
            if type == 5:
                type = 6
            x = random.randint(1,self._colLim-2)
            y = random.randint(1,self._rowLim-2)
            if self._store[row][col][y][x] != 5 and self._store[row][col][y][x] != 6:
                self._infoStore[row][col].append([x*64, y*64, True, "collect",type])
                count += 1
            else:
                self._infoStore[row][col].append([x*64, y*64, True, "collect",5])
                count += 1


        count = 0
        enemyNum = random.randint(0,maxEnemy)
        while count < enemyNum:
            x = random.randint(1,self._colLim-2)
            y = random.randint(1,self._rowLim-2)
            if self._store[row][col][y][x] != 5:
                self._infoStore[row][col].append([x*64, y*64, True, "enemy",count]) 
                count += 1

        count = 0
        charNum = random.randint(0,1)
        while count < charNum:
            x = random.randint(1,self._colLim-2)
            y = random.randint(1,self._rowLim-2)
            if self._store[row][col][y][x] != 5:
                self._infoStore[row][col].append([x*64, y*64, True, "char"])
                count += 1

    def placePath(self):
        currentTmPos = [1,1]
        pathDrct = random.randint(0,1)
        acrossMap, downMap = False, False
        if pathDrct == 0:
            acrossMap = True
            currentTilePos = [random.randint(2,self._rowLim-2),0]
        else:
            downMap = True
            currentTilePos = [0,random.randint(2,self._rowLim-2)]

        valid = False
        while not valid:
            pathSet  = False
            while not pathSet:
                if currentTilePos[0] >= self._rowLim-1:
                    downMap = True 
                    pathSet = True
                elif currentTilePos[1] >= self._colLim-1:
                    pathSet = True
                    acrossMap = True
                self._store[currentTmPos[0]][currentTmPos[1]][currentTilePos[0]][currentTilePos[1]] = 7
                switch = random.randint(0,4)
                if acrossMap:
                    if switch == 1 and currentTilePos[0] < self._rowLim-2:
                        currentTilePos[0] += 1
                    currentTilePos[1] += 1
                elif downMap:
                    if switch == 1 and currentTilePos[1] < self._colLim-2:
                        currentTilePos[1] += 1
                    currentTilePos[0] += 1

            if acrossMap:
                currentTmPos[1] += 1
                currentTilePos[1] = 0
            elif downMap:
                currentTmPos[0] += 1
                currentTilePos[0] = 0

            acrossMap, downMap = False, False
            if currentTmPos[0] == 9 or currentTmPos[1] == 8:
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
            


        

    def placeFeatures(self,feature):
        areas = 0
        size = 0
        tileNum = 0
        if feature == "water":
            tileNum = 5
            size = random.randint(15,25)
            areas = random.randint(50,80)
        elif feature == "flower":
            tileNum = 2
            size = random.randint(15,25)
            areas = random.randint(40,60)
        elif feature == "bush":
            tileNum = 3
            size = random.randint(15,25)
            areas = random.randint(30,50)
        elif feature == "lilipad":
            tileNum = 6
            size = random.randint(1,5)
            areas = random.randint(30,50)
        elif feature == "empty":
            tileNum = 8
            size = random.randint(15,25)
            areas = random.randint(40,60)


        for _ in range(areas):
            startRow, startCol, starty, startx = random.randint(1,8), random.randint(1,7), random.randint(1,self._rowLim-1), random.randint(1,self._colLim-1)
            while self._store[startRow][startCol][starty][startx] == tileNum:
                startRow, startCol = random.randint(1,8), random.randint(1,7)
                starty, startx = random.randint(1,self._rowLim-1), random.randint(1,self._colLim-1)
            self._store[startRow][startCol][starty][startx] = tileNum

            for _ in range(size):
                new = False
                row, col = startRow, startCol 
                y, x = starty, startx
                while self._store[row][col][y][x] == tileNum and not new:
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
                self._store[row][col][y][x] = tileNum
                starty, startx = y, x

      


    def createAreaMap(self,diff):
        for row in range(len(self._store)):
            for col in range(len(self._store[row])):
                if self._store[row][col] != -1:
                    self._store[row][col] = self.generateMap()
                if row == 8 and col == 7:
                    self._infoStore[row][col] = "BOSS"
                elif row == 0 and col == 7:
                    self._infoStore[row][col] = "GATE"
        self.placeFeatures("flowers")
        self.placeFeatures("bush")
        self.placeFeatures("water")
        maxEnemy = 3
        if diff == "Easy":
            maxEnemy = 2
        elif diff == "Hard":
            maxEnemy = 4
        for r in range(len(self._store)):
            for c in range(len(self._store[r])):
                if self._store[r][c] != -1 and self._infoStore[r][c] != "BOSS" and self._infoStore[r][c] != "GATE":
                    self.placeItems(r,c,maxEnemy)
        self.placePath()


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

    

    
