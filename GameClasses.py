import pygame
import random


#---------------GAME SETTINGS---------------#
class GameSettings():
    def __init__(self):
        # settings 
        self._saveFile = 0
        self._diff = "Easy"
        self._screen = "menu"
        self._showAll = False
        self._music = -1
        self._playMusic = False
        self._showTutorial = True
        # for extracting item
        # the key values are the collected item and the array contains each chemical and how much the player will recieve
        self._itemChances = {"pebble":[["carbon",1]],
                        "bug":[["carbon",1],["cyanide salt",1],["carboxylic acid",1]], 
                        "flower":[["carbon",1],["amine",1],["alkane",1]], 
                        "leaf":[["carbon",1],["oxygen",1],["ester",1],["amino acid",1]],
                        "fruit":[["carbon",1],["water",1],["glucose",1],["amino acid",1]],
                        "wplant":[["carbon",1],["oxygen",1],["ester",1],["water",1],["silicon",1]],
                        "bush":[["carbon",3],["oxygen",1],["ester",1],["amino acid",1]],
                        "rock":[["carbon",3],["silicon",1],["magnesium",1]],
                        "gem":[["carbon",3],["magnesium",1],["nickel",1]],
                        "volrock":[["carbon",3],["sulfur",1],["ammonia",1]],
                        "freshwater":[["water",3],["carbon dioxide",1],["oxygen",1]],
                        "saltwater":[["water",3],["carbon dioxide",1],["oxygen",1],["halogensalt",1]]}
        # random rewards for the player to recieve after winning a battle
        self._battleRewards = ["thionyl chloride","potassium dichromate","sodium borohydride","alcohol","alkane","alkene","ester",
                               "carbon","water","halogen salt","carboxylic acid","halogen"]

    # getters
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
    def get_itemChances(self):
        return self._itemChances
    def get_rewards(self):
        return self._battleRewards

    # setters (used when loding a save file and when changing settings)
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
    
    # cycles the difficulty through easy medium and hard
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
        # pos is the position of the current map on the area map
        # currentMap is the current chunk being displayed
        self._rowLim = 15
        self._colLim = 23
        self._mapStore = []
        self._discovered = []
        self._infoStore = []
        # stores of tile and item information
        self._sheet = pygame.image.load("grasslandsTiles.bmp")
    
    def reset(self):
        # resets the stores to empty
        ''' empty map store (-1 is the border and 0 is an empty chunk )
        [[-1, -1, -1, -1, -1, -1, -1, -1, -1], 
            [-1, 0, 0, 0, 0, 0, 0, 0, -1],
            [-1, 0, 0, 0, 0, 0, 0, 0, -1],
            [-1, 0, 0, 0, 0, 0, 0, 0, -1], 
            [-1, 0, 0, 0, 0, 0, 0, 0, -1], 
            [-1, 0, 0, 0, 0, 0, 0, 0, -1], 
            [-1, 0, 0, 0, 0, 0, 0, 0, -1], 
            [-1, 0, 0, 0, 0, 0, 0, 0, -1], 
            [-1, 0, 0, 0, 0, 0, 0, 0, -1], 
        [-1, -1, -1, -1, -1, -1, -1, -1, -1]]

        empty infoStore (each [] represents a chunk)
        [[[], [], [], [], [], [], [], [], []],
        [[], [], [], [], [], [], [], [], []], 
        [[], [], [], [], [], [], [], [], []], 
        [[], [], [], [], [], [], [], [], []], 
        [[], [], [], [], [], [], [], [], []], 
        [[], [], [], [], [], [], [], [], []], 
        [[], [], [], [], [], [], [], [], []], 
        [[], [], [], [], [], [], [], [], []], 
        [[], [], [], [], [], [], [], [], []], 
        [[], [], [], [], [], [], [], [], []]]

        empty discovered (-1 is a border and 0 represnts a non discovered map, 1 represents discovrered)
        [[-1, -1, -1, -1, -1, -1, -1, -1, -1], 
            [-1, 1, 0, 0, 0, 0, 0, 0, -1], 
            [-1, 0, 0, 0, 0, 0, 0, 0, -1],
            [-1, 0, 0, 0, 0, 0, 0, 0, -1],
            [-1, 0, 0, 0, 0, 0, 0, 0, -1],
            [-1, 0, 0, 0, 0, 0, 0, 0, -1], 
            [-1, 0, 0, 0, 0, 0, 0, 0, -1], 
            [-1, 0, 0, 0, 0, 0, 0, 0, -1], 
            [-1, 0, 0, 0, 0, 0, 0, 0, -1], 
        [-1, -1, -1, -1, -1, -1, -1, -1, -1]]
        ''' 

        self._mapStore = []
        self._discovered = []
        self._infoStore = []
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
            self._mapStore.append(rows[0])
            self._discovered.append(rows[1])
            self._infoStore.append(rows[2])
            for k in range(len(self._infoStore)):
                for l in range(len(self._infoStore[k])):
                    self._infoStore[k][l] = []
        self._discovered[self._pos[0]][self._pos[1]] = 1

    # getters / setters
    def get_pos(self):
        return self._pos
    def get_waterPos(self):
        positions = []
        for i in range(len(self._mapStore[self._pos[0]][self._pos[1]])):
            for j in range(len(self._mapStore[self._pos[0]][self._pos[1]][i])):
                if self._mapStore[self._pos[0]][self._pos[1]][i][j] == 5 or self._mapStore[self._pos[0]][self._pos[1]][i][j] == 6:
                    positions.append([i,j])
        return positions
    
    def set_collected(self,itemNum):
        # used to remove items after they have been collected
        info = self._infoStore[self._pos[0]][self._pos[1]]
        for i in range(len(info)):
            try:
                if info[i][4] == itemNum:
                    self._infoStore[self._pos[0]][self._pos[1]][i][2] = False
                    # false will set the item to invisible when map is loaded
            except:
                pass


    def placePath(self):
        currentTmPos = [1,1]
        # current tile map position
        # randomly chooses if the starting direction will be accross or down 
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
                # pathSet is True if there is a path going across the current chunk
                if currentTilePos[0] >= self._rowLim-1:
                    # if the current tile is at left border then the tile path must continue down
                    downMap = True 
                    pathSet = True
                elif currentTilePos[1] >= self._colLim-1:
                    # if the current tile is at left border then the tile path must continue across
                    pathSet = True
                    acrossMap = True

                self._mapStore[currentTmPos[0]][currentTmPos[1]][currentTilePos[0]][currentTilePos[1]] = 7
                switch = random.randint(0,4)
                # switch randomly changes the direction of the path within the chunk
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
                # if in the bottom right corner than a valid path has been made
                valid = True
            elif currentTmPos[0] == 8:
                # if at the bottom then the path can only continue across
                acrossMap = True
            elif currentTmPos[1] == 7:
                # if at the left wall then the path can only continue down
                downMap = True
            else:
                # randomly changes the direction of the path between chunks
                pathDrct = random.randint(0,1)
                if pathDrct == 0:
                    acrossMap = True
                else:
                    downMap = True   

    def placeItems(self,row,col,maxEnemy):
        count = 0
        collectNum = random.randint(1,5)
        # generates a random number of items and loops until count(how many items have been places) is equal to that number
        while count < collectNum:
            # chooses a random type
            type = random.randint(0,8)
            if type == 5:
                # if a water plant is chosen it is set to the next type instead
                type = 6
            x = random.randint(1,self._colLim-2)
            y = random.randint(1,self._rowLim-2)
            if self._mapStore[row][col][y][x] != 5 and self._mapStore[row][col][y][x] != 6:
                self._infoStore[row][col].append([x*64, y*64, True, "collect",type])
                # grass tiles can have any types of item except water plant
                # infoStore stores the position of the item, if it is visible, its object type(collect) and its sub type()
                count += 1
            else:
                # if the tile is a water tile (tile 5 or 6) then a water plant will be places
                self._infoStore[row][col].append([x*64, y*64, True, "collect",5])
                count += 1

        # does the same for enemies and characters 
        count = 0
        enemyNum = random.randint(0,maxEnemy)
        while count < enemyNum:
            x = random.randint(1,self._colLim-2)
            y = random.randint(1,self._rowLim-2)
            if self._mapStore[row][col][y][x] != 5:
                self._infoStore[row][col].append([x*64, y*64, True, "enemy",count]) 
                # there will be multiple enemies so count will be their unique key 
                # for example when an enemy is defeated its key will be used to search for it in infoStore in order to set its visiblity to False
                count += 1

        count = 0
        charNum = random.randint(0,1)
        while count < charNum:
            x = random.randint(1,self._colLim-2)
            y = random.randint(1,self._rowLim-2)
            if self._mapStore[row][col][y][x] != 5:
                self._infoStore[row][col].append([x*64, y*64, True, "char"])
                # there will only be a max of one character in each chunk so it doesnt need a key
                count += 1

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

        for _ in range(areas):
            # random starting position is chosen
            # startRow/startCol are the coordinates of the cunk and startx/starty are the coordinates of the tile
            startRow, startCol, starty, startx = random.randint(1,8), random.randint(1,7), random.randint(1,self._rowLim-1), random.randint(1,self._colLim-1)
            while self._mapStore[startRow][startCol][starty][startx] == tileNum:
                # finds a new starting tile if the tile type is already changed
                startRow, startCol = random.randint(1,8), random.randint(1,7)
                starty, startx = random.randint(1,self._rowLim-1), random.randint(1,self._colLim-1)
            self._mapStore[startRow][startCol][starty][startx] = tileNum

            # after choosing a starting tile, it then generates the clump
            for _ in range(size):
                new = False
                row, col = startRow, startCol 
                y, x = starty, startx
                while self._mapStore[row][col][y][x] == tileNum and not new:
                    drct = random.randint(0,3)
                    new = False
                    # chooses a random direction to expand the clump by
                    # then checks if that direction has not been changed already (if so sets new to True, else chooses another direction)
                    # also makes sure the direction does not cause the selected position to leave the boundaries of the chunk
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
                self._mapStore[row][col][y][x] = tileNum
                # the new startx/starty is the changed tile
                starty, startx = y, x

    def generateMap(self):
        count = 0
        skeleton = []
        for _ in range(self._rowLim):
            row = []
            for _ in range(self._colLim):
                row.append(random.randint(0,1))
            skeleton.append(row)
            count += 1
        # generates a 2D array of random 0s and 1s (representing the two types of grass tile)
        return skeleton

    def createAreaMap(self,diff):
        # creates randomly generated maps each time the player enters the adventure screen
        for row in range(len(self._mapStore)):
            for col in range(len(self._mapStore[row])):
                if self._mapStore[row][col] != -1:
                    # for every 0 in the empty map it is replaced by a generated map
                    self._mapStore[row][col] = self.generateMap()
                # special chunks for boss and gate (they will have generated tiles but no items)
                if row == 8 and col == 7:
                    self._infoStore[row][col] = "BOSS"
                elif row == 0 and col == 7:
                    self._infoStore[row][col] = "GATE"
        # fetures are special types of tiles that will generate in clumps instead of randomly scattered like the grass tiles
        self.placeFeatures("flowers")
        self.placeFeatures("bush")
        self.placeFeatures("water")

        # placing enemies is dependant on the difficulty 
        maxEnemy = 3
        if diff == "Easy":
            maxEnemy = 2
        elif diff == "Hard":
            maxEnemy = 4

        # places items on generated map chunks
        for r in range(len(self._mapStore)):
            for c in range(len(self._mapStore[r])):
                if self._mapStore[r][c] != -1 and self._infoStore[r][c] != "BOSS" and self._infoStore[r][c] != "GATE":
                    self.placeItems(r,c,maxEnemy)
                    # r(row) and c(col) specify the posiion of the chunk
        # finally generates the path from the start to the boss
        self.placePath()

    
    def generateTile(self,tileNum, scale):
        size = 32
        # each tile is 32x32 on the tile sheet
        tile = "empty"
        tileTypes = {"grass1":[0,0],"grass2":[1,1],"grass3":[0,1],"grass4":[2,1],
                    "water1":[1,0],"water2":[2,0],
                    "path1":[0,2],"empty":[1,2]}
        # dictionary that specifies the coordinates on the tile sheet of each tile type
        # tileNums which is what the mapStore is made up of mapps to a tile type 
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
        # start is the coordinates on the tile sheet
        image = pygame.Surface((size,size))
        image.blit(self._sheet,(0,0),((start[0]*size),(start[1]*size),size,size))
        image = pygame.transform.scale(image,(size*scale,size*scale))
        # tranforms the surface by the scale for either regular map or mini map size
        return image

    def drawMap(self,scale,width,height):
        tiles = []
        for i in range (len(self._currentMap)):
            for j in range (len(self._currentMap[i])):
                tile = self.generateTile(self._currentMap[i][j], scale)
                if scale == 2:
                    # drawing a regular sized map
                    tiles.append([tile,[j*32*scale,i*32*scale]])
                else:
                    # drawing a mini map so the scale is smaller
                    tiles.append([tile,[100+width*scale*0.5*(self._pos[1]-1)+j*32*scale,100+height*scale*0.5*(self._pos[0]-1)+i*32*scale]])
        # returns an 2D array of pygame surfaces with tile images on them
        return tiles

    def loadMap(self,playerpos,playersize,w,h):
        resetPlayer = -1
        # resetPlayer determines if the player will traverse onto another chunk 
        # this is determined by checking if the players position is near any of the boundaries and if there are chunks in that direction 
        # if the mapStore in the direction the player is travelling is equal to -1 this means the player is at the areaMap border so the player will not be able to more any further in that direction
        if playerpos[0] <= 10 and self._mapStore[self._pos[0]][self._pos[1]-1] != -1:
                # west
                resetPlayer = 3
                self._pos[1] -= 1
        elif playerpos[0] >= w-playersize[0] and self._mapStore[self._pos[0]][self._pos[1]+1] != -1:
                # east
                resetPlayer = 1
                self._pos[1] += 1
        elif playerpos[1] <= 10 and self._mapStore[self._pos[0]-1][self._pos[1]] != -1:
                # north
                resetPlayer = 0
                self._pos[0] -= 1
        elif playerpos[1] >= h-playersize[1] and self._mapStore[self._pos[0]+1][self._pos[1]] != -1:
                # south
                resetPlayer = 2
                self._pos[0] += 1
        # sets the currentMap using the posiion coordinates
        # if a new map has been found then its position on the discovered array is set to 1
        self._currentMap = self._mapStore[self._pos[0]][self._pos[1]]
        self._discovered[self._pos[0]][self._pos[1]] = 1
        if self._pos[0] == 1 and self._pos[1] == 7:
            info = "GATE"
        elif self._pos[0] == 8 and self._pos[1] == 7:
            info = "BOSS"
        else:
            info = self._infoStore[self._pos[0]][self._pos[1]]
        # returns to the main code the tiles from drawMap, info of objects on that chunk, and resetPlayer which will set the players new position is required
        return self.drawMap(2,w,h), info, resetPlayer

    def drawMiniMap(self,width,height,showAll):
        tiles = []
        currentCol, currentRow = self._pos[0], self._pos[1] 
        for row in range(len(self._mapStore)):
            for col in range(len(self._mapStore[row])):
                if self._mapStore[row][col] != -1:
                    # draws all the chunks that have been discovered
                    # if showAll (a game setting the player can change in the pause menu) is on then it will load all the chunks despite discovered
                    if self._discovered[row][col] == 1 or showAll:
                        self._pos[0], self._pos[1] = row, col
                        self._currentMap = self._mapStore[row][col]
                        tiles.append(self.drawMap(0.2,width,height))
        self._pos[0], self._pos[1] = currentCol, currentRow
        self._currentMap = self._mapStore[self._pos[0]][self._pos[1]]
        # returns all the surfaces of tiles that need to be displayed on the screen
        return tiles

    

    
