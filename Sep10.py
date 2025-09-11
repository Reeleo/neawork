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


 
def displayText(txt, fnt, colour, pos):
    txt = fnt.render(str(txt), True, colour)
    txtrect = txt.get_rect()
    txtrect.center = (pos)
    screen.blit(txt, txtrect)




#     #8
#     if x == "map":
#         pass
    
#     #9
#     if x == "minimap":
#         mini.posx, mini.posy, mini.width, mini.height = 100, 100, WIDTH-200, HEIGHT-192
#         mini.colour1, mini.colour2 = WHITE, GRASS
#         b1.posx, b1.posy, b1.text = 1187, 783, "RETURN"
#         mini.drawScreen()
#         b1.setSize()
#         b1.update()
#         areaMap.drawMiniMap(currentMap)
#         displayText(f"PlayerPosx = {areaMap.pos[1]}",font20,WHITE,1270,130)
#         displayText(f"PlayerPosy = {areaMap.pos[0]}",font20,WHITE,1270,160)
#         pass

#     #12
#     if x == "gate":
#         pass
    


def displayObject(type,obj):
    if type == "button":
        pos = obj.get_pos()
        size = obj.get_size()
        text = obj.get_text()
        collide = obj.collision()
        colours = obj.get_colours()
        if not collide:
            pygame.draw.rect(screen,colours[0],[pos[0]-5, pos[1]-5, size[0]+10, size[1]+10])
        pygame.draw.rect(screen,colours[1],[pos[0], pos[1], size[0], size[1]])
        displayText(text, font20, BLACK, [pos[0]+size[0]/2, pos[1]+size[1]/2])
    
    elif type == "player":
        pos = obj.get_pos()
        image = obj.update()
        screen.blit(image,(pos))
    
    elif type == "collect":
        pos = obj.get_pos()
        image, collision = obj.update(game.get_screen(),player.get_pos())
        screen.blit(image,(pos))
        if collision:
            playerpos = player.get_pos()
            playersize = player.get_size()
            displayText("SPACE", font20, WHITE, [playerpos[0]+playersize[0]/2, playerpos[1]-20])
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                obj.set_visible(False)
                player.collect[obj._type[0]] += 1

    elif type == "mini":
        pos = obj.get_pos()
        size = obj.get_size()
        text = obj.get_text()
        colours = obj.get_colours()
        pygame.draw.rect(screen, colours[0], [pos[0]-10, pos[1]-10, size[0]+20, size[1]+20])
        pygame.draw.rect(screen, colours[1], [pos[0], pos[1], size[0], size[1]])






def screenSetUp(x):
    #1
    if x == "menu":
        buttons.clear()
        buttons.append(ShapeClasses.Button([WIDTH/4-90,3*HEIGHT/4],[180,80],"EXIT"))
        buttons.append(ShapeClasses.Button([3*WIDTH/4-90, 3*HEIGHT/4],[180,80],"START"))
        buttons.append(ShapeClasses.Button([WIDTH/2-90, HEIGHT/2],[180,80],"HOW TO PLAY"))

    #2
    if x == "htp":
        buttons.clear()
        buttons.append(ShapeClasses.Button([WIDTH-300, 200],[180,80],"MENU"))

    #3
    if x == "savefiles":
        buttons.clear()
        buttons.append(ShapeClasses.Button([400,100],[1000,150],"Save1"))
        buttons.append(ShapeClasses.Button([400,300],[1000,150],"Save2"))
        buttons.append(ShapeClasses.Button([400,500],[1000,150],"Save3"))
        buttons.append(ShapeClasses.Button([WIDTH/4-200, 3*HEIGHT/4],[180,80],"MENU"))

    #4
    if x == "home":
        buttons.clear()
        player.set_posy(HEIGHT-200-player.get_size()[1])

    #5
    if x == "extract":
        buttons.clear()
        buttons.append(ShapeClasses.Button([1150,750],[180,80],"RETURN"))
        for i in range(12):
            buttons.append(ShapeClasses.Button([140+(i)*100, 200],[80,80],i))
        for j in range(12):
            cSprites.append(SpriteClasses.Collectable(j,[140+j*100, 200]))
        for k in range(12):
            cSprites[k].assign_type(game.collectTypes)
        mini.set_size([WIDTH-200, HEIGHT-200])
        mini.set_pos([100, 100])

    #6
    if x == "craft":
        buttons.clear()
        buttons.append(ShapeClasses.Button([1150,750],[180,80],"RETURN"))
        for i in range(12):
            buttons.append(ShapeClasses.Button([140+(i)*100, 200],[80,80],i))
        for j in range(12):
            cSprites.append(SpriteClasses.Collectable(j,[140+j*100, 200]))
        mini.set_size([WIDTH-200, HEIGHT-200])
        mini.set_pos([100, 100])

    #7
    if x == "pause":
        buttons.clear()
        for i in range(5):
            if i == 0:
                buttons.append(ShapeClasses.Button([900,250],[80,80],"+"))
            elif i == 1:
                buttons.append(ShapeClasses.Button([600,250],[80,80],"+"))
            elif i == 2:
                buttons.append(ShapeClasses.Button([350,250],[80,80],str(game.displayAll)))
            elif i == 3:
                buttons.append(ShapeClasses.Button([WIDTH/2, 3*HEIGHT/4],[180,80],"RETURN"))
            elif i == 4:
                buttons.append(ShapeClasses.Button([WIDTH/4-90, 3*HEIGHT/4],[180,80],"MENU"))
            elif i == 5:
                buttons.append(ShapeClasses.Button([WIDTH/3+20, 3*HEIGHT/4],[180,80],"SAVE"))

    

def screenDisplay(x):
    #1
    if x == "menu":
        screen.fill(BURG)
        pygame.draw.rect(screen,RED,[20,20,WIDTH-40, HEIGHT-40])
        pygame.draw.rect(screen,BLACK,[40,40,WIDTH-80, HEIGHT-80])
        displayText("game", font100, WHITE, [WIDTH/2, 200])
        for i in range(len(buttons)):
            displayObject("button",buttons[i])

    #2
    if x == "htp":
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
    if x == "savefiles":
        screen.fill(BURG)
        pygame.draw.rect(screen,RED,[20,20,WIDTH-40, HEIGHT-40])
        pygame.draw.rect(screen,BLACK,[40,40,WIDTH-80, HEIGHT-80])
        for i in range(len(buttons)):
            displayObject("button",buttons[i])

    #4
    if x == "home":
        screen.fill(BURG)
        pygame.draw.rect(screen,BLACK,[40, 40, WIDTH-80, HEIGHT-80])
        pygame.draw.rect(screen,BURG,[0, HEIGHT-200, WIDTH, 200])
    
    #5
    if x == "extract":
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
    if x == "craft":
        pygame.draw.rect(screen,WHITE,(100,HEIGHT/2-75,WIDTH-200,10))
        displayObject("mini",mini)
        displayText("Your Chemicals:", font20, WHITE, [212, 150])
        for i in range(len(buttons)):
            displayObject("button",buttons[i])

    #7
    if x == "pause":
        screen.fill(BURG)
        pygame.draw.rect(screen,RED,[20,20,WIDTH-40, HEIGHT-40])
        pygame.draw.rect(screen,BLACK,[40,40,WIDTH-80, HEIGHT-80])
        displayText(f"Difficulty: {game.diff}", font20, WHITE, [800, 300])
        displayText(f"Speed: {player.get_speed()}", font20, WHITE, [530, 300])
        displayText(f"AllMiniMap: ", font20, WHITE, [280, 300])
        for i in range(len(buttons)):
            displayObject("button",buttons[i])



def extraction(item):
    chances = game.itemChances[item]
    chem = chances[random.randint(0,len(chances)-1)][0]
    player.chemicals[chem] += 1
    player.collect[item] -= 1
    print(item, chem, player.chemicals[chem])

    qt.set_pos([WIDTH/2,700])
    qt.set_up((f"{item}, {chem}, {player.chemicals[chem]}"),time.time())
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
            extraction(extractItem)
            if player.collect[extractItem] > 0:
                extraction(extractItem)
        if qt.get_visible():
            print(qt.get_text())
            displayText(qt.get_text(),font20,qt.get_colours(),qt.get_pos())
            qt.update()
        pygame.display.update()
        clock.tick(FPS)

    player.movecheck(game.get_screen())
    displayObject("player", player)
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
                        if game.displayAll:
                            game.displayAll = False
                        else:
                            game.displayAll = True
                    elif i == 3:
                        cont = 2
                    elif i == 4:
                        cont = 3
                    elif i == 5:
                        saveGame()
    return cont




# def battleMode(opponant):
#     while opponant.battleTime:
#         cont = 0
#         eventSetUp("battle",opponant)

#         opponant.update()
#         opponant.battle()

#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 cont = 1
#             if event.type == pygame.KEYDOWN:
#                 if event.key == pygame.K_ESCAPE:
#                     cont = 1
#                 elif event.key == pygame.K_p:
#                     cont = 4

#         player.updateSprite()
#         pygame.display.update()
#         clock.tick(FPS)
#         if cont == 4:
#             break
#         elif cont != 0:
#             opponant.battleTime = False
#     return cont

# def mapScreen():
#     cont = 0
#     miniMap = False
#     areaMap.loadMap(player.boundaryCheck())
#     for i in range(len(cSprites)):
#         if cSprites[i].visible and not tb1.visible:
#             cSprites[i].update()
#     for j in range(len(eSprites)):
#         if eSprites[j].visible:
#             eSprites[j].update()
#             if eSprites[j].battleTime:
#                 cont = battleMode(eSprites[j])
#     if chr1.visible:
#         chr1.update()
#     if tb1.visible:
#         tb1.display()


#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             cont = 1
#         if event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_ESCAPE:
#                 cont = 3
#             elif event.key == pygame.K_p:
#                 cont = 2
#             elif event.key == pygame.K_m:
#                 miniMap = True
#                 screen.fill(BLACK)
#                 screenSetUp("minimap")

#     if time.time()-TIME >= tb1.startTime + 0.5:
#         chr1.cont = True
#     if time.time()-TIME >= tb1.startTime + 2:
#         tb1.visible = False

#     while miniMap:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 miniMap = False
#                 cont = 1
#             if event.type == pygame.KEYDOWN:
#                 if event.key == pygame.K_ESCAPE:
#                     miniMap = False
#                     cont = 1
#                 elif event.key == pygame.K_m:
#                     miniMap = False
#             elif event.type == pygame.MOUSEBUTTONDOWN:
#                 if b1.update():
#                     miniMap = False
#         pygame.display.update()
#         clock.tick(FPS)
#     player.movecheck()
#     player.updateSprite()
#     # player.testUpdate()
#     # leftFoot.test()
#     # rightFoot.test()
#     pygame.display.update()
#     clock.tick(FPS)
#     return cont


# def bossScreen():
    cont = 0
    eventSetUp("boss","")
    mini.drawScreen()
    userText = ""
    for i in range(4):
        buttonTemps[i].update()

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






player = SpriteClasses.Player()
game = GameClasses.GameSettings()

areaMap = GameClasses.AreaMap()
currentMap = GameClasses.TileMap()

buttons = []
cSprites = []
eSprites = []
nSprites = []

tb1 = ShapeClasses.TextBox(0,0,720,25)
mini = ShapeClasses.MiniWindow()
qt = ShapeClasses.QuickText()


menu = True
htp = False
savefiles = False
home = False
maps = False
pause = False
running = True
while running:

    screenSetUp("menu")
    while menu:
        cont = menuScreen()
        if cont == 1:
            menu = False
            running = False
            print("END")
            break
        elif cont == 2:
            menu = False
            savefiles = True
            print("saves")
            break
        elif cont == 3:
            menu = False
            htp = True
            print("hottoplay")
            break
    
    screenSetUp("htp")
    while htp:
        cont = htpScreen()
        if cont == 1:
            htp = False
            running = False
        elif cont == 2:
            htp = False
            menu = True

    screenSetUp("savefiles")
    while savefiles:
        cont = saveFileScreen()
        if cont == 1:
            savefiles = False
            running = False
        elif cont == 2:
            savefiles = False
            menu = True
        elif cont == 3:
            savefiles = False
            home = True
            game.screen = "home"
            player.set_posx(100)

    screenSetUp("home")
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

    screenSetUp("maps")
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

    screenSetUp("pause")
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