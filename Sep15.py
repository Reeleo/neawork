import pygame
import random
import time
import SpriteClasses
import ShapeClasses
import GameClasses
pygame.init()

font20 = pygame.font.Font('freesansbold.ttf', 20)
font100 = pygame.font.Font('freesansbold.ttf',100)
WIDTH, HEIGHT = 1472, 960
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


def checkCollision(enemy):
        pPos = player.get_pos()
        ePos = enemy.get_pos()
        pMask = pygame.mask.from_surface(player.updateSprite())
        eMask = pygame.mask.from_surface(enemy.updateSprite(True))
        
        pos = [abs(ePos[0]-pPos[0]),abs(ePos[1]-pPos[1])]
        if pMask.overlap(eMask, (pos)):
            enemy.set_battle(True)

def fetchQuestions():
    return [["jello","i","ii","iii","iv"],["jello2","i","ii","iii","iv"]]

  
def displayText(txt, fnt, colour, pos):
    txt = fnt.render(str(txt), True, colour)
    txtrect = txt.get_rect()
    txtrect.center = (pos)
    screen.blit(txt, txtrect)


def displayObject(type,obj):
    if type == "button":
        pos = obj.get_pos()
        size = obj.get_size()
        text = obj.get_text()
        colours = obj.get_colours()
        if not obj.collision():
            pygame.draw.rect(screen,colours[0],[pos[0]-5, pos[1]-5, size[0]+10, size[1]+10])
        pygame.draw.rect(screen,colours[1],[pos[0], pos[1], size[0], size[1]])
        displayText(text, font20, BLACK, [pos[0]+size[0]/2, pos[1]+size[1]/2])
    
    elif type == "player":
        screen.blit(obj.update(game.get_screen(),WIDTH,HEIGHT),(obj.get_pos()))
    
    elif type == "collect":
        screen.blit(obj.update(game.get_screen()),(obj.get_pos()))
        if  obj.collision(player.get_pos()):
            playerpos = player.get_pos()
            playersize = player.get_size()
            displayText("SPACE", font20, WHITE, [playerpos[0]+playersize[0]/2, playerpos[1]-20])
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                obj.set_visible(False)
                player.collect[obj._type[0]] += 1
                areaMap.set_collected(obj.get_num())
    
    elif type == "enemy":
        checkCollision(obj)
        screen.blit(obj.update(player.get_pos(),WIDTH,HEIGHT),(obj.get_pos()))
    
    elif type == "char":
        screen.blit(obj.update(),(obj.get_pos()))

    elif type == "special":
        screen.blit(obj.update(),(obj.get_pos()))

    elif type == "mini":
        pos = obj.get_pos()
        size = obj.get_size()
        text = obj.get_text()
        colours = obj.get_colours()
        pygame.draw.rect(screen, colours[0], [pos[0]-10, pos[1]-10, size[0]+20, size[1]+20])
        pygame.draw.rect(screen, colours[1], [pos[0], pos[1], size[0], size[1]])

    elif type == "tile":
        screen.blit(obj[0],(obj[1]))
        
    elif type == "heart":
        screen.blit(obj.get_image(0,0,80,80),(obj.get_pos()))

            
            




def screenSetUp(screenType):
    #1
    if screenType == "menu":
        buttons.clear()
        buttons.append(ShapeClasses.Button([WIDTH/4-90,3*HEIGHT/4],[180,80],"EXIT"))
        buttons.append(ShapeClasses.Button([3*WIDTH/4-90, 3*HEIGHT/4],[180,80],"START"))
        buttons.append(ShapeClasses.Button([WIDTH/2-90, HEIGHT/2],[180,80],"HOW TO PLAY"))

    #2
    if screenType == "htp":
        buttons.clear()
        buttons.append(ShapeClasses.Button([WIDTH-300, 200],[180,80],"MENU"))

    #3
    if screenType == "savefiles":
        buttons.clear()
        buttons.append(ShapeClasses.Button([400,100],[1000,150],"Save1"))
        buttons.append(ShapeClasses.Button([400,300],[1000,150],"Save2"))
        buttons.append(ShapeClasses.Button([400,500],[1000,150],"Save3"))
        buttons.append(ShapeClasses.Button([WIDTH/4-200, 3*HEIGHT/4],[180,80],"MENU"))

    #4
    if screenType == "home":
        buttons.clear()
        game.set_screen("home")
        player.set_posx(100)
        player.set_posy(HEIGHT-200-player.get_size()[1])

    #5
    if screenType == "extract":
        buttons.clear()
        cSprites.clear()
        buttons.append(ShapeClasses.Button([1150,750],[180,80],"RETURN"))
        for i in range(12):
            buttons.append(ShapeClasses.Button([140+(i)*100, 200],[80,80],i))
        for j in range(12):
            cSprites.append(SpriteClasses.Collectable([140+j*100, 200],j))
        for k in range(12):
            cSprites[k].assign_type(game.collectTypes)
        mini.set_size([WIDTH-200, HEIGHT-200])
        mini.set_pos([100, 100])

    #6
    if screenType == "craft":
        buttons.clear()
        buttons.append(ShapeClasses.Button([1150,750],[180,80],"RETURN"))
        for i in range(12):
            buttons.append(ShapeClasses.Button([140+(i)*100, 200],[80,80],i))
        for j in range(12):
            cSprites.append(SpriteClasses.Collectable(j,[140+j*100, 200]))
        mini.set_size([WIDTH-200, HEIGHT-200])
        mini.set_pos([100, 100])

    #7
    if screenType == "pause":
        buttons.clear()
        for i in range(6):
            if i == 0:
                buttons.append(ShapeClasses.Button([900,250],[80,80],"+"))
            elif i == 1:
                buttons.append(ShapeClasses.Button([600,250],[80,80],"+"))
            elif i == 2:
                buttons.append(ShapeClasses.Button([350,250],[80,80],str(game.get_showAll())))
            elif i == 3:
                buttons.append(ShapeClasses.Button([WIDTH/2, 3*HEIGHT/4],[180,80],"RETURN"))
            elif i == 4:
                buttons.append(ShapeClasses.Button([WIDTH/4-90, 3*HEIGHT/4],[180,80],"MENU"))
            elif i == 5:
                buttons.append(ShapeClasses.Button([WIDTH/3+20, 3*HEIGHT/4],[180,80],"SAVE"))

    #8
    if screenType == "maps":
        buttons.clear()
        cSprites.clear()
        eSprites.clear()
        nSprites.clear()
        sSprites.clear()
        game.set_screen("grassland")
        areaMap.createAreaMap()
        tiles, blitList, setPlayer = areaMap.loadMap(player.get_pos(),player.get_size(),WIDTH,HEIGHT)
        for item in range(len(blitList)):
            if blitList[item][2]:
                if blitList[item][3] == "collect":
                    cSprites.append(SpriteClasses.Collectable([blitList[item][0],blitList[item][1]],blitList[item][4]))
                    cSprites[-1].assign_type(game.collectTypes)
                elif blitList[item][3] == "enemy":
                    eSprites.append(SpriteClasses.Enemy([blitList[item][0],blitList[item][1]]))
                elif blitList[item][3] == "char":
                    nSprites.append(SpriteClasses.Character([blitList[item][0],blitList[item][1]],""))
        for i in range(3):
            hearts.append(SpriteClasses.Sprite([10+i*60, 20],[20,20],0.6,RED,pygame.image.load("collectablesSprites.bmp")))
        
    #9
    if screenType == "minimap":
        buttons.clear()
        mini.set_pos([100,100])
        mini.set_size([WIDTH-200, HEIGHT-192])
        buttons.append(ShapeClasses.Button([1187,783],[180,80],"RETURN"))

    #10
    if screenType == "battle":
        buttons.clear()
        sSprites.clear()
        for i in range(4):
            if i < 2:
                buttons.append(ShapeClasses.Button([615+i*380, 400],[360,80],i+1))
            else:
                buttons.append(ShapeClasses.Button([615+(i-2)*380, 500],[360,80],i+1))
        sSprites.append(SpriteClasses.Character([30,180],"enemy"))
        mini.set_size([WIDTH-200, HEIGHT-200])
        mini.set_pos([100, 100])
        



def screenDisplay(screenType):
    #1
    if screenType == "menu":
        screen.fill(BURG)
        pygame.draw.rect(screen,RED,[20,20,WIDTH-40, HEIGHT-40])
        pygame.draw.rect(screen,BLACK,[40,40,WIDTH-80, HEIGHT-80])
        displayText("game", font100, WHITE, [WIDTH/2, 200])
        for i in range(len(buttons)):
            displayObject("button",buttons[i])

    #2
    if screenType == "htp":
        screen.fill(BURG)
        pygame.draw.rect(screen,RED,[20,20,WIDTH-40, HEIGHT-40])
        pygame.draw.rect(screen,BLACK,[40,40,WIDTH-80, HEIGHT-80])
        surface = pygame.Surface((213,146)).convert_alpha()
        surface.blit(pygame.image.load("htpImage.bmp"),(0,0),((0),(0),213,146))
        surface = pygame.transform.scale(surface,(213*6,146*5))
        screen.blit(surface,(100,100))
        for i in range(len(buttons)):
            displayObject("button",buttons[i])

    #3
    if screenType == "savefiles":
        screen.fill(BURG)
        pygame.draw.rect(screen,RED,[20,20,WIDTH-40, HEIGHT-40])
        pygame.draw.rect(screen,BLACK,[40,40,WIDTH-80, HEIGHT-80])
        for i in range(len(buttons)):
            displayObject("button",buttons[i])

    #4
    if screenType == "home":
        screen.fill(BURG)
        pygame.draw.rect(screen,BLACK,[40, 40, WIDTH-80, HEIGHT-80])
        pygame.draw.rect(screen,BURG,[0, HEIGHT-200, WIDTH, 200])
        displayObject("player", player)
    
    #5
    if screenType == "extract":
        pygame.draw.rect(screen,WHITE,(100,HEIGHT/2-75,WIDTH-200,10))
        displayObject("mini",mini)
        displayText("Your Collection:", font20, WHITE, [212, 150])
        for i in range(len(buttons)):
            displayObject("button",buttons[i])
        for j in range(len(cSprites)):
            displayObject("collect",cSprites[j])

        x = 210
        y = 310
        displayText(f"BACTERIA: {player.collect["bct"]}", font20, WHITE, [x, y])
        displayText(f"BUG: {player.collect["bug"]}", font20, WHITE, [x+200, y])
        displayText(f"FLOWER: {player.collect["flw"]}", font20, WHITE, [x+400, y])
        displayText(f"LEAF: {player.collect["lef"]}", font20, WHITE, [x+600, y])
        displayText(f"FRUIT: {player.collect["frt"]}", font20, WHITE, [x+800, y])
        displayText(f"OCEAN PLANT: {player.collect["wpl"]}", font20, WHITE, [x+1000, y])
        displayText(f"SMALL ROCK: {player.collect["srk"]}", font20, WHITE, [x, y+30])
        displayText(f"BIG ROCK: {player.collect["brk"]}", font20, WHITE, [x+200, y+30])
        displayText(f"VOLCANIC ROCK: {player.collect["vrk"]}", font20, WHITE, [x+400, y+30])
        displayText(f"GEMSTONE: {player.collect["gem"]}", font20, WHITE, [x+600, y+30])

        displayText(f"WATER: {player.collect["wtr"]}", font20, WHITE, [x, y+60])
        displayText(f"SEAWATER: {player.collect["swt"]}", font20, WHITE, [x+200, y+60])

    #6
    if screenType == "craft":
        pygame.draw.rect(screen,WHITE,(100,HEIGHT/2-75,WIDTH-200,10))
        displayObject("mini",mini)
        displayText("Your Chemicals:", font20, WHITE, [212, 150])
        for i in range(len(buttons)):
            displayObject("button",buttons[i])

    #7
    if screenType == "pause":
        screen.fill(BURG)
        pygame.draw.rect(screen,RED,[20,20,WIDTH-40, HEIGHT-40])
        pygame.draw.rect(screen,BLACK,[40,40,WIDTH-80, HEIGHT-80])
        displayText(f"Difficulty: {game.diff}", font20, WHITE, [800, 300])
        displayText(f"Speed: {player.get_speed()}", font20, WHITE, [530, 300])
        displayText(f"AllMiniMap: ", font20, WHITE, [280, 300])
        for i in range(len(buttons)):
            displayObject("button",buttons[i])

    #8 
    if screenType == "maps":
        tiles, blitList, setPlayer = areaMap.loadMap(player.get_pos(),player.get_size(),WIDTH,HEIGHT)
        player.set_pos(setPlayer,WIDTH,HEIGHT)
        if setPlayer != -1:
            cSprites.clear()
            eSprites.clear()
            nSprites.clear()
            sSprites.clear()
            if blitList == "BOSS":
                sSprites.append(SpriteClasses.Character([WIDTH/2-300,HEIGHT/2-200],"boss"))
            elif blitList == "GATE":
                sSprites.append(SpriteClasses.Character([WIDTH/2-300,HEIGHT/2-200],"gate"))
            else:
                for item in range(len(blitList)):
                    if blitList[item][2]:
                        if blitList[item][3] == "collect":
                            cSprites.append(SpriteClasses.Collectable([blitList[item][0],blitList[item][1]],blitList[item][4]))
                            cSprites[-1].assign_type(game.collectTypes)
                        elif blitList[item][3] == "enemy":
                            eSprites.append(SpriteClasses.Enemy([blitList[item][0],blitList[item][1]]))
                        elif blitList[item][3] == "char":
                            nSprites.append(SpriteClasses.Character([blitList[item][0],blitList[item][1]],""))

        for tile in range(len(tiles)):
            displayObject("tile",tiles[tile])
        for c in range(len(cSprites)):
            if cSprites[c].get_visible():
                displayObject("collect",cSprites[c])
        for e in range(len(eSprites)):
            if eSprites[e].get_visible():
                displayObject("enemy",eSprites[e])
        for n in range(len(nSprites)):
            if nSprites[n].get_visible():
                displayObject("char",nSprites[n])
        for s in range(len(sSprites)):
            displayObject("special",sSprites[s])
        for h in range(len(hearts)):
            displayObject("heart",hearts[h])
        displayObject("player", player)
     
    #9
    if screenType == "minimap":
        displayObject("mini",mini)
        displayObject("button",buttons[0])
        tiles = areaMap.drawMiniMap(WIDTH,HEIGHT,game.get_showAll())
        for i in range(len(tiles)):
            for j in range(len(tiles[i])):
                displayObject("tile",tiles[i][j])
        displayText(f"PlayerCol = {areaMap.get_pos()[1]}",font20,WHITE,[1270,130])
        displayText(f"PlayerRow = {areaMap.get_pos()[0]}",font20,WHITE,[1270,160])

    #10
    if screenType == "battle":
        displayObject("mini",mini)
        displayObject("special",sSprites[0])
        displayText("BATTLE:",font100,WHITE,[320, 180])
        
        for i in range(len(buttons)):
            displayObject("button",buttons[i])






def extraction(item):
    chances = game.itemChances[item]
    chem = chances[random.randint(0,len(chances)-1)][0]
    player.chemicals[chem] += 1
    player.collect[item] -= 1
    quickTexts.append(ShapeClasses.QuickText([WIDTH/2,700],f"{item}, {chem}, {player.chemicals[chem]}",time.time()))
    print(item, chem, player.chemicals[chem])
    return chem
     



def loadGame():
    if game.get_saveFile() == 1:
        file = open("saveData1.txt","r")
    elif game.get_saveFile() == 2:
        file = open("saveData2.txt","r")
    elif game.get_saveFile() == 3:
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
            player.set_speed(int(saveData[0]),"set")
    print("LOADED")

def saveGame():
    if game.get_saveFile() == 1:
        file = open("saveData1.txt","w")
    elif game.get_saveFile() == 2:
        file = open("saveData2.txt","w")
    elif game.get_saveFile() == 3:
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
    gameLine2 += str(player.get_speed())
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
    screenDisplay("menu")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            cont = 1
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                cont = 1
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i in range(len(buttons)):
                if buttons[i].collision():
                    cont = i + 1
    pygame.display.update()
    clock.tick(FPS)
    return cont


def htpScreen():
    cont = 0
    screenDisplay("htp")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            cont = 1
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                cont = 1
        if event.type == pygame.MOUSEBUTTONDOWN:
            if buttons[0].collision():
                cont = 2
    pygame.display.update()
    clock.tick(FPS)
    return cont


def saveFileScreen():
    cont = 0
    screenDisplay("savefiles")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            cont = 1
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                cont = 1
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i in range(len(buttons)):
                if buttons[i].collision():
                    if i == 3:
                        cont = 2
                    else:
                        cont = 3
                        game.set_saveFile(i+1)
    pygame.display.update()
    clock.tick(FPS)
    return cont


def homeScreen():
    cont = 0
    craftTime, extractTime = False, False
    screenDisplay("home")
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

    if craftTime:
        screenSetUp("craft")
    while craftTime:
        screenDisplay("craft")
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
                if buttons[0].collision():
                    craftTime = False
        pygame.display.update()
        clock.tick(FPS)

    if extractTime:
        screenSetUp("extract")
    while extractTime:
        screenDisplay("extract")
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
                for i in range(len(buttons)):
                    if buttons[i].collision():
                        if i == 0:
                            extractTime = False
                        elif i == 1:
                            extractItem = "bct"
                        elif i == 2:
                            extractItem = "bug"
                        elif i == 3:
                            extractItem = "flw"
                        elif i == 4:
                            extractItem = "lef"
                        elif i == 5:
                            extractItem = "frt"
                        elif i == 6:
                            extractItem = "wpl"
                        elif i == 7:
                            extractItem = "srk"
                        elif i == 8:
                            extractItem = "brk"
                        elif i == 9:
                            extractItem = "vrk"
                        elif i == 10:
                            extractItem = "gem"
                        elif i == 11:
                            extractItem = "wtr"
                        elif i == 12:
                            extractItem = "swt"
        if extractItem != 0:
            if player.collect[extractItem] > 0:
                extraction(extractItem)
        if len(quickTexts) > 0:
            if quickTexts[0].get_visible():
                print(quickTexts[0].get_text())
                displayText(quickTexts[0].get_text(),font20,quickTexts[0].get_colours(),quickTexts[0].get_pos())
                quickTexts[0].update()
        pygame.display.update()
        clock.tick(FPS)

    pygame.display.update()
    clock.tick(FPS)
    return cont



def pauseScreen():
    cont = 0
    screenDisplay("pause")
    pygame.display.update()
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            cont = 1
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i in range(len(buttons)):
                if buttons[i].collision():
                    if i == 0:
                        game.increaseDiff()
                    elif i == 1:
                        if player.get_speed() <= 50:
                            player.set_speed(5,"inc")
                        else:
                            player.set_speed(10,"set")
                    elif i == 2:
                        game.set_showAll()
                        buttons[i].set_text(game.get_showAll())
                    elif i == 3:
                        cont = 2
                    elif i == 4:
                        cont = 3
                    elif i == 5:
                        saveGame()
    return cont



def mapScreen():
    cont = 0
    miniMap = False
    screenDisplay("maps")
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

    if miniMap:
        screenSetUp("minimap")
    while miniMap:
        screenDisplay("minimap")
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
                if buttons[0].collision():
                    miniMap = False
        pygame.display.update()
        clock.tick(FPS)

    battle = False
    for i in range(len(eSprites)):
        battle = eSprites[i].get_battle()
        if battle:
            screenSetUp("battle")
            eSprites[i].set_qSet(fetchQuestions())
            eSprites[i].set_qNum(0)

            while battle:
                screenDisplay("battle")
                questions = eSprites[i].get_qSet()[eSprites[i].get_qNum()]
                    

                displayText(questions[0],font20,WHITE,[900,200])
                buttons[0].set_text(questions[1])
                buttons[1].set_text(questions[2])
                buttons[2].set_text(questions[3])
                buttons[3].set_text(questions[4])

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        battle = False
                        cont = 1
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            battle = False
                            cont = 1
                        elif event.key == pygame.K_b:
                            battle = False
                            for i in range(len(eSprites)):
                                eSprites[i].set_battle(False)
                            player.set_posx(30)
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        for j in range(len(buttons)):
                            if buttons[j].collision():
                                print("button",j)
                pygame.display.update()
                clock.tick(FPS)
            break

    pygame.display.update()
    clock.tick(FPS)
    return cont






player = SpriteClasses.Player()
game = GameClasses.GameSettings()
areaMap = GameClasses.AreaMap()
mini = ShapeClasses.MiniWindow([100,100],[WIDTH-200, HEIGHT-200])
buttons = []
quickTexts = []
cSprites = []
eSprites = []
nSprites = []
sSprites = []
hearts = []


running = "menu"
while running != "":

    if running == "menu":
        screenSetUp("menu")
    while running == "menu":
        cont = menuScreen()
        if cont == 1:
            running = ""
            break
        elif cont == 2:
            running = "savefiles"
            break
        elif cont == 3:
            running = "htp"
            break
    
    if running == "htp":
        screenSetUp("htp")
    while running == "htp":
        cont = htpScreen()
        if cont == 1:
            running = ""
        elif cont == 2:
            running = "menu"

    if running == "savefiles":
        screenSetUp("savefiles")
    while running == "savefiles":
        cont = saveFileScreen()
        if cont == 1:
            running = ""
        elif cont == 2:
            running = "menu"
        elif cont == 3:
            running = "home"

    if running == "home":
        screenSetUp("home")
    while running == "home":
        cont = homeScreen()
        if cont == 1:
            running = ""
        elif cont == 2:
            running = "pause"
        elif cont == 3:
            running = "maps"

    if running == "pause":
        screenSetUp("pause")
    while running == "pause":
        cont = pauseScreen()
        if cont == 1:
            running = ""
        elif cont == 2:
            if game.get_screen() == "home":
                running = "home"
            elif game.get_screen() == "grassland":
                running = "maps"
        elif cont == 3:
            running = "menu"

    if running == "maps":
        screenSetUp("maps")
    while running == "maps":
        cont = mapScreen()
        if cont == 1:
            running = ""
        elif cont == 2:
            running = "pause"
        elif cont == 3:
            running = "home"

    pygame.display.update()
    clock.tick(FPS)
pygame.quit()