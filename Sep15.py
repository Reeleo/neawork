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

music = ["Menu.mp3","DoctorWeird.mp3","ForestBattle.mp3"]
sounds = [pygame.mixer.Sound("click.mp3")]


def checkCollision(enemy):
        pPos = player.get_pos()
        ePos = enemy.get_pos()
        pMask = pygame.mask.from_surface(player.updateSprite())
        eMask = pygame.mask.from_surface(enemy.updateSprite(True))
        
        pos = [abs(ePos[0]-pPos[0]),abs(ePos[1]-pPos[1])]
        if pMask.overlap(eMask, (pos)):
            enemy.set_battle(True)

def fetchQuestions():
    c = []
    chosen = []
    qSet = []
    file = open("questions.txt","r")
    for _ in range(18):
        line = file.readline()
        qSet.append(line.split(","))
    for i in range(18):
        qSet[i][5] = int(qSet[i][5])
    file.close()
    for _ in range(3):
        valid = False
        while not valid:
            c1 = random.randint(0,17)
            repeat = False
            for j in range(len(c)):
                if c[j] == c1:
                    repeat = True
            if not repeat:
                valid = True
        c.append(c1)
    chosen = [qSet[c[0]],qSet[c[1]],qSet[c[2]]]
    return chosen

    
def displayText(txt,fnt,colour,pos):
    txt = fnt.render(str(txt), True, colour)
    txtrect = txt.get_rect()
    txtrect.center = (pos)
    screen.blit(txt, txtrect)

def displayImage(image,pos,scale,size):
    surface = pygame.Surface((size))
    surface.blit(image,(0,0),((0),(0),size[0],size[1]))
    surface = pygame.transform.scale(surface,(size[0]*scale,size[1]*scale))
    screen.blit(surface,(pos))

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
        if game.get_screen() == "home":
            screen.blit(obj.update(game.get_screen(),WIDTH,HEIGHT),(obj.get_pos()))
        else:
            screen.blit(obj.update(game.get_screen(),WIDTH,HEIGHT),(obj.get_pos()))
            pPos = player.get_pos()
            lfoot = [pPos[0]+35,pPos[1]+102]
            rfoot = [pPos[0]+67,pPos[1]+102]

            speed = player.get_speed()
            player.set_validWalk("all",[True,True,True,True])
            tilePos = areaMap.get_waterPos()
            for i in range(len(tilePos)):
                wMask = pygame.mask.from_surface(areaMap.get_tile(3,2))

                if tilePos[i][1]*64 < lfoot[0]-speed < tilePos[i][1]*64+64 or tilePos[i][1]*64 < lfoot[0]+10-speed < tilePos[i][1]*64+64:
                    if tilePos[i][0]*64 < lfoot[1] < tilePos[i][0]*64+64 or tilePos[i][0]*64 < lfoot[1]+10 < tilePos[i][0]*64+64:
                        player.set_validWalk(3,False)
                if tilePos[i][1]*64 < lfoot[0]+speed < tilePos[i][1]*64+64 or tilePos[i][1]*64 < lfoot[0]+10+speed < tilePos[i][1]*64+64:
                    if tilePos[i][0]*64 < lfoot[1] < tilePos[i][0]*64+64 or tilePos[i][0]*64 < lfoot[1]+10 < tilePos[i][0]*64+64:
                        player.set_validWalk(1,False)
                if tilePos[i][1]*64 < lfoot[0] < tilePos[i][1]*64+64 or tilePos[i][1]*64 < lfoot[0] < tilePos[i][1]*64+64:
                    if tilePos[i][0]*64 < lfoot[1]+speed < tilePos[i][0]*64+64 or tilePos[i][0]*64 < lfoot[1]+10+speed < tilePos[i][0]*64+64:
                        player.set_validWalk(2,False)
                if tilePos[i][1]*64 < lfoot[0] < tilePos[i][1]*64+64 or tilePos[i][1]*64 < lfoot[0] < tilePos[i][1]*64+64:
                    if tilePos[i][0]*64 < lfoot[1]-speed < tilePos[i][0]*64+64 or tilePos[i][0]*64 < lfoot[1]+10-speed < tilePos[i][0]*64+64:
                        player.set_validWalk(0,False)

            
                if tilePos[i][1]*64 < rfoot[0]-speed < tilePos[i][1]*64+64 or tilePos[i][1]*64 < rfoot[0]+10-speed < tilePos[i][1]*64+64:
                    if tilePos[i][0]*64 < rfoot[1] < tilePos[i][0]*64+64 or tilePos[i][0]*64 < rfoot[1]+10 < tilePos[i][0]*64+64:
                        player.set_validWalk(3,False)
                if tilePos[i][1]*64 < rfoot[0]+speed < tilePos[i][1]*64+64 or tilePos[i][1]*64 < rfoot[0]+10+speed < tilePos[i][1]*64+64:
                    if tilePos[i][0]*64 < rfoot[1] < tilePos[i][0]*64+64 or tilePos[i][0]*64 < rfoot[1]+10 < tilePos[i][0]*64+64:
                        player.set_validWalk(1,False)
                if tilePos[i][1]*64 < rfoot[0] < tilePos[i][1]*64+64 or tilePos[i][1]*64 < rfoot[0] < tilePos[i][1]*64+64:
                    if tilePos[i][0]*64 < rfoot[1]+speed < tilePos[i][0]*64+64 or tilePos[i][0]*64 < rfoot[1]+10+speed < tilePos[i][0]*64+64:
                        player.set_validWalk(2,False)
                if tilePos[i][1]*64 < rfoot[0] < tilePos[i][1]*64+64 or tilePos[i][1]*64 < rfoot[0] < tilePos[i][1]*64+64:
                    if tilePos[i][0]*64 < rfoot[1]-speed < tilePos[i][0]*64+64 or tilePos[i][0]*64 < rfoot[1]+10-speed < tilePos[i][0]*64+64:
                        player.set_validWalk(0,False)
            
    elif type == "collect":
        screen.blit(obj.update(game.get_screen()),(obj.get_pos()))
        if obj.collision(player.get_pos()):
            playerpos = player.get_pos()
            playersize = player.get_size()
            displayText("SPACE", font20, WHITE, [playerpos[0]+playersize[0]/2, playerpos[1]-20])
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                obj.set_visible(False)
                player.inc_collect(obj._type[0])
                areaMap.set_collected(obj.get_num())
    
    elif type == "door":
        screen.blit(obj.update(game.get_screen()),(obj.get_pos()))
        if obj.collision(player.get_pos()):
            playerpos = player.get_pos()
            playersize = player.get_size()
            displayText("SPACE", font20, WHITE, [playerpos[0]+playersize[0]/2, playerpos[1]-20])

    elif type == "enemy":
        checkCollision(obj)
        screen.blit(obj.update(player.get_pos(),WIDTH,HEIGHT),(obj.get_pos()))
    
    elif type == "char":
        screen.blit(obj.update(),(obj.get_pos()))
        if obj.collision(player.get_pos()):
            playerpos = player.get_pos()
            playersize = player.get_size()
            displayText("SPACE", font20, WHITE, [playerpos[0]+playersize[0]/2, playerpos[1]-20])
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                print("HELLO")

    elif type == "special":
        screen.blit(obj.update(),(obj.get_pos()))
        if  obj.collision(player.get_pos()):
            playerpos = player.get_pos()
            playersize = player.get_size()
            displayText("SPACE", font20, WHITE, [playerpos[0]+playersize[0]/2, playerpos[1]-20])
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                print("BOSS TIME")

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
        screen.blit(obj.get_image(0,3,32,32),(obj.get_pos()))
         



def screenSetUp(screenType):
    #1
    if screenType == "menu":
        buttons.clear()
        if game.get_music() == -1 and game.get_playMusic():
            pygame.mixer.music.load(music[0])
            pygame.mixer.music.play(-1)
            game.set_music(0)
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
        cSprites.clear()
        pygame.mixer.music.stop()
        game.set_music(-1)
        game.set_screen("home")
        player.set_posx(WIDTH/2-player.get_size()[0]/2)
        player.set_posy(HEIGHT-200-player.get_size()[1])
        doors.append(SpriteClasses.Collectable([1273,608],12))
        doors.append(SpriteClasses.Collectable([22,608],12))
        doors[0].assign_type(game.collectTypes)
        doors[1].assign_type(game.collectTypes)

    #5
    if screenType == "inventory":
        buttons.clear()
        cSprites.clear()
        buttons.append(ShapeClasses.Button([1150,750],[180,80],"RETURN"))
        for j in range(12):
            cSprites.append(SpriteClasses.Collectable([120, 100+j*60],j))
        for k in range(12):
            cSprites[k].assign_type(game.collectTypes)
        if game.get_screen() == "home":
            buttons.append(ShapeClasses.Button([850,460],[400,80],"EXTRACT"))
            buttons.append(ShapeClasses.Button([390,460],[400,80],"CRAFT"))
        mini.set_size([WIDTH-200, HEIGHT-200])
        mini.set_pos([100, 100])
        
    #6
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

    #7
    if screenType == "craft":
        buttons.clear()
        cSprites.clear()
        buttons.append(ShapeClasses.Button([1150,750],[180,80],"RETURN"))
        for i in range(12):
            buttons.append(ShapeClasses.Button([140+(i)*100, 200],[80,80],i))
        for j in range(12):
            cSprites.append(SpriteClasses.Collectable(j,[140+j*100, 200]))
        mini.set_size([WIDTH-200, HEIGHT-200])
        mini.set_pos([100, 100])

    #8
    if screenType == "pTable":
        buttons.clear()

        buttons.append(ShapeClasses.Button([1240,610],[90,180],"RETURN"))
        mini.set_size([WIDTH-200, HEIGHT-255])
        mini.set_pos([100, 130])

    #9
    if screenType == "pause":
        buttons.clear()
        for i in range(8):
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
            elif i == 6:
                buttons.append(ShapeClasses.Button([350,350],[80,80],str(game.get_playMusic())))
            elif i == 7:
                buttons.append(ShapeClasses.Button([900,350],[80,80],str(game.get_tutorial())))

    #10
    if screenType == "maps":
        buttons.clear()
        cSprites.clear()
        eSprites.clear()
        nSprites.clear()
        sSprites.clear()
        hearts.clear()
        if game.get_music() == -1 and game.get_playMusic():
            pygame.mixer.music.stop()
            pygame.mixer.music.load(music[1])
            pygame.mixer.music.play(-1)
            game.set_music(1)
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
        for i in range(player.get_health()):
            hearts.append(SpriteClasses.Sprite([2+i*60, 2],[50,50],2.5,BLACK,pygame.image.load("collectablesSprites.bmp")))
        
    #11
    if screenType == "minimap":
        buttons.clear()
        mini.set_pos([100,100])
        mini.set_size([WIDTH-200, HEIGHT-192])
        buttons.append(ShapeClasses.Button([1187,783],[180,80],"RETURN"))

    #12
    if screenType == "battle":
        buttons.clear()
        sSprites.clear()
        hearts.clear()
        if game.get_music() == 1 and game.get_playMusic():
            pygame.mixer.music.stop()
            pygame.mixer.music.load(music[2])
            pygame.mixer.music.play(-1)
            game.set_music(2)

        for i in range(4):
            if i < 2:
                buttons.append(ShapeClasses.Button([615+i*380, 400],[360,80],i+1))
            else:
                buttons.append(ShapeClasses.Button([615+(i-2)*380, 500],[360,80],i+1))
        sSprites.append(SpriteClasses.Character([30,180],"enemy"))
        mini.set_size([WIDTH-200, HEIGHT-200])
        mini.set_pos([100, 100])
        for i in range(player.get_health()):
            hearts.append(SpriteClasses.Sprite([10+i*60, 20],[50,50],2.5,BLACK,pygame.image.load("collectablesSprites.bmp")))  

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
        pygame.draw.rect(screen,BLACK,[20, 20, WIDTH-40, HEIGHT-40])
        pygame.draw.rect(screen,BURG,[50, 50, WIDTH-100, HEIGHT-100])
        #displayImage(pygame.image.load("homeBackground.png"),[WIDTH/2-480,50],3,[320,320])
        displayImage(pygame.image.load("homeBackground.png"),[WIDTH/2-400,120],2.5,[320,320])
        pygame.draw.rect(screen,BURG,[0, HEIGHT-180, WIDTH, 180])
        if game.get_tutorial():
            displayText("press 'q' for periodic table",font20,WHITE,[1086,360])
            displayText("press 'e' for inventory",font20,WHITE,[455,535])
            displayText("press 'p' for pause",font20,WHITE,[736,220])
            displayText("press 'space' to interact",font20,WHITE,[132,590])
            displayText("press 'esc' to go back",font20,WHITE,[165,65])
        displayObject("door", doors[0])
        displayObject("door", doors[1])
        displayObject("player", player)
    
    #5
    if screenType == "inventory":
        pygame.draw.rect(screen,WHITE,(100,HEIGHT/2-75,WIDTH-200,10))
        displayObject("mini",mini)
        displayText("Your Collection:", font20, WHITE, [290, 140])
        for i in range(len(buttons)):
            displayObject("button",buttons[i])
        for j in range(len(cSprites)):
            displayObject("collect",cSprites[j])

        x = 530
        y = 340
        collection = player.get_collect()
        displayText(f"BACTERIA: {collection["bacteria"]}", font20, WHITE, [x, y])
        displayText(f"BUG: {collection["bug"]}", font20, WHITE, [x+200, y])
        displayText(f"FLOWER: {collection["flower"]}", font20, WHITE, [x, y+40])
        displayText(f"LEAF: {collection["leaf"]}", font20, WHITE, [x+200, y+40])
        displayText(f"FRUIT: {collection["fruit"]}", font20, WHITE, [x+400, y+40])
        displayText(f"OCEAN PLANT: {collection["wplant"]}", font20, WHITE, [x+600, y+40])
        displayText(f"SMALL ROCK: {collection["srock"]}", font20, WHITE, [x, y+80])
        displayText(f"BIG ROCK: {collection["lrock"]}", font20, WHITE, [x+200, y+80])
        displayText(f"VOLCANIC ROCK: {collection["volrock"]}", font20, WHITE, [x+400, y+80])
        displayText(f"GEMSTONE: {collection["gem"]}", font20, WHITE, [x+600, y+80])

        displayText(f"FRESHWATER: {collection["freshwater"]}", font20, WHITE, [x+400, y])
        displayText(f"SEAWATER: {collection["saltwater"]}", font20, WHITE, [x+600, y])
  
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
        collection = player.get_collect()
        displayText(f"BACTERIA: {collection["bacteria"]}", font20, WHITE, [x, y])
        displayText(f"BUG: {collection["bug"]}", font20, WHITE, [x+200, y])
        displayText(f"FLOWER: {collection["flower"]}", font20, WHITE, [x+400, y])
        displayText(f"LEAF: {collection["leaf"]}", font20, WHITE, [x+600, y])
        displayText(f"FRUIT: {collection["fruit"]}", font20, WHITE, [x+800, y])
        displayText(f"OCEAN PLANT: {collection["wplant"]}", font20, WHITE, [x+1000, y])
        displayText(f"SMALL ROCK: {collection["srock"]}", font20, WHITE, [x, y+30])
        displayText(f"BIG ROCK: {collection["lrock"]}", font20, WHITE, [x+200, y+30])
        displayText(f"VOLCANIC ROCK: {collection["volrock"]}", font20, WHITE, [x+400, y+30])
        displayText(f"GEMSTONE: {collection["gem"]}", font20, WHITE, [x+600, y+30])

        displayText(f"FRESHWATER: {collection["freshwater"]}", font20, WHITE, [x, y+60])
        displayText(f"SEAWATER: {collection["saltwater"]}", font20, WHITE, [x+200, y+60])

    #6
    if screenType == "craft":
        pygame.draw.rect(screen,WHITE,(100,HEIGHT/2-75,WIDTH-200,10))
        displayObject("mini",mini)
        displayText("Your Chemicals:", font20, WHITE, [212, 150])
        for i in range(len(buttons)):
            displayObject("button",buttons[i])

    #7
    if screenType == "pTable":
        pygame.draw.rect(screen,WHITE,(100,HEIGHT/2-75,WIDTH-200,10))
        displayObject("mini",mini)
        displayObject("button",buttons[0])
        displayImage(pygame.image.load("pTable.png"),[110,140],0.9,[WIDTH-250,HEIGHT-200])

    #8
    if screenType == "pause":
        screen.fill(BURG)
        pygame.draw.rect(screen,RED,[20,20,WIDTH-40, HEIGHT-40])
        pygame.draw.rect(screen,BLACK,[40,40,WIDTH-80, HEIGHT-80])
        displayText(f"Difficulty: {game.get_diff()}", font20, WHITE, [800, 300])
        displayText(f"Speed: {player.get_speed()}", font20, WHITE, [530, 300])
        displayText(f"AllMiniMap: ", font20, WHITE, [280, 300])
        displayText(f"PlayMusic: ", font20, WHITE, [280, 400])
        displayText(f"Show Tutorial: ", font20, WHITE, [820, 400])
        for i in range(len(buttons)):
            displayObject("button",buttons[i])

    #9
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
     
    #10
    if screenType == "minimap":
        displayObject("mini",mini)
        displayObject("button",buttons[0])
        tiles = areaMap.drawMiniMap(WIDTH,HEIGHT,game.get_showAll())
        for i in range(len(tiles)):
            for j in range(len(tiles[i])):
                displayObject("tile",tiles[i][j])
        displayText(f"PlayerCol = {areaMap.get_pos()[1]}",font20,WHITE,[1270,130])
        displayText(f"PlayerRow = {areaMap.get_pos()[0]}",font20,WHITE,[1270,160])

    #11
    if screenType == "battle":
        screen.fill(BLACK)
        displayObject("mini",mini)
        displayObject("special",sSprites[0])
        displayText("BATTLE:",font100,WHITE,[320, 180])
        
        for i in range(len(buttons)):
            displayObject("button",buttons[i])
        for j in range(len(hearts)):
            displayObject("heart",hearts[j])







 
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
            for item in player.get_collect():
                player.set_collect(item,int(saveData[count])) 
                count += 1
        elif i == 1:
            for item in player.get_chemicals():
                player.set_chemicals(item, int(saveData[count]))
                count += 1
        elif i == 2:
            game.set_diff(saveData[0])
        elif i == 3:
            player.set_speed(saveData[0],"set")
    player.set_int()
    file.close()
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
    collection = player.get_collect()
    chemicals = player.get_chemicals()
    for item in player.get_collect():
        collectLine += str(collection[item])+","
    for chem in player.get_chemicals():
        chemicalLine += str(chemicals[chem])+","
    gameLine1 += game.get_diff()
    gameLine2 += str(player.get_speed())
    file.writelines(collectLine)
    file.writelines("\n") 
    file.writelines(chemicalLine)
    file.writelines("\n") 
    file.writelines(gameLine1)
    file.writelines(gameLine2)
    file.close()
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
                    pygame.mixer.Sound.play(sounds[0])
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
                pygame.mixer.Sound.play(sounds[0])
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
                    pygame.mixer.Sound.play(sounds[0])
                    if i == 3:
                        cont = 2
                    else:
                        cont = 3
                        game.set_saveFile(i+1)
                        loadGame()
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
                    pygame.mixer.Sound.play(sounds[0])
                    if i == 0:
                        game.inc_diff()
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
                    elif i == 6:
                        game.set_playMusic()
                        buttons[i].set_text(game.get_playMusic())
                        if not game.get_playMusic():
                            pygame.mixer.music.stop()
                            game.set_music(-1)
                        else:
                            if game.get_screen() == "grassland":
                                pygame.mixer.music.load(music[1])
                                pygame.mixer.music.play(-1)
                                game.set_music(1)
                    elif i == 7:
                        if game.get_tutorial():
                            game.set_tutorial(False)
                        else:
                            game.set_tutorial(True)
                        buttons[i].set_text(game.get_tutorial())

    return cont


def extraction(item):
    chances = game.itemChances[item]
    chem = chances[random.randint(0,len(chances)-1)][0]
    player.extract(item,chem)
    chems = player.get_chemicals()
    quickTexts.append(ShapeClasses.QuickText([550,500],f"{item}, {chem}, {chems[chem]}",time.time()))
    print(item, chem, chems[chem])
    return chem
    
def pTableMini():
    cont = 0
    pTableTime = True
    while pTableTime:
        screenDisplay("pTable")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pTableTime = False
                cont = 1
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pTableTime = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if buttons[0].collision():
                    pTableTime = False
        pygame.display.update()
        clock.tick(FPS)
    return cont 

def extractMini():
    cont = 0
    extractTime = True
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
                elif event.key == pygame.K_c:
                    player.set_collect("bacteria",10000)
                    player.set_collect("leaf",10000)
                    player.set_collect("srock",10000)
                    player.set_collect("freshwater",10000)
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i in range(len(buttons)):
                    if buttons[i].collision():
                        pygame.mixer.Sound.play(sounds[0])
                        if i == 0:
                            extractTime = False
                        elif i == 1:
                            extractItem = "bacteria"
                        elif i == 2:
                            extractItem = "bug"
                        elif i == 3:
                            extractItem = "flower"
                        elif i == 4:
                            extractItem = "leaf"
                        elif i == 5:
                            extractItem = "fruit"
                        elif i == 6:
                            extractItem = "wplant"
                        elif i == 7:
                            extractItem = "srock"
                        elif i == 8:
                            extractItem = "lrock"
                        elif i == 9:
                            extractItem = "volrock"
                        elif i == 10:
                            extractItem = "gem"
                        elif i == 11:
                            extractItem = "freshwater"
                        elif i == 12:
                            extractItem = "saltwater"
        if extractItem != 0:
            if player.get_collect()[extractItem] > 0:
                extraction(extractItem)
        deleteing = []
        for i in range(len(quickTexts)):
            if quickTexts[i].get_visible():
                print(quickTexts[i].get_text())
                displayText(quickTexts[i].get_text(),font20,quickTexts[i].get_colours(),[quickTexts[i].get_pos()[0],quickTexts[i].get_pos()[1]+i*30])
                remove = quickTexts[i].update()
                if remove:
                    deleteing.append(i)
        print(len(quickTexts))
        for _ in range(len(deleteing)):
            quickTexts.pop(0)
        pygame.display.update()
        clock.tick(FPS)
    return cont 

def craftMini():
    cont = 0
    craftTime = True
    while craftTime:
        screenDisplay("craft")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                craftTime = False
                cont = 1
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    craftTime = False
                elif event.key == pygame.K_SPACE:
                    craftTime = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if buttons[0].collision():
                    pygame.mixer.Sound.play(sounds[0])
                    craftTime = False
        pygame.display.update()
        clock.tick(FPS)
    return cont 

def inventoryMini():
    cont = 0
    inventoryTime, extractTime, craftTime = True, False, False
    while inventoryTime:
        screenDisplay("inventory")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                inventoryTime = False
                cont = 1
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    inventoryTime = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i in range(len(buttons)):
                    if buttons[i].collision():
                        pygame.mixer.Sound.play(sounds[0])
                        if i == 0:
                            inventoryTime = False
                            for i in range(12):
                                cSprites.pop(-1)
                        elif i == 1:
                            inventoryTime = False
                            extractTime = True
                        elif i == 2:
                            inventoryTime = False
                            craftTime = True

        if extractTime:
            screenSetUp("extract")
            cont = extractMini()
        if craftTime:
            screenSetUp("craft")
            cont = craftMini()

        pygame.display.update()
        clock.tick(FPS)
    return cont 


def homeScreen():
    cont = 0
    inventoryTime, pTableTime = False, False
    screenDisplay("home")
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            cont = 1
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                cont = 2
            elif event.key == pygame.K_SPACE:
                for i in range(len(doors)):
                    if doors[i].collision(player.get_pos()):
                        cont = 3
                cont = 3
            elif event.key == pygame.K_e:
                inventoryTime  = True
            elif event.key == pygame.K_q:
                pTableTime  = True

    if inventoryTime:
        screenSetUp("inventory")
        cont = inventoryMini()
    if pTableTime:
        screenSetUp("pTable")
        cont = pTableMini()

    pygame.display.update()
    clock.tick(FPS)
    return cont



def miniMapMini():
    cont = 0
    miniMap = True
    while miniMap:
        screenDisplay("minimap")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                miniMap = False
                cont = 1
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    miniMap = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if buttons[0].collision():
                    pygame.mixer.Sound.play(sounds[0])
                    miniMap = False
        pygame.display.update()
        clock.tick(FPS)
    return cont 

def mapScreen():
    cont = 0
    miniMap, pTableTime, battle = False, False, False
    screenDisplay("maps")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            cont = 1
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                cont = 3
            elif event.key == pygame.K_p:
                cont = 2
            elif event.key == pygame.K_q:
                pTableTime = True
            elif event.key == pygame.K_m:
                miniMap = True

    if miniMap:
        screenSetUp("minimap")
        cont = miniMapMini()
    if pTableTime:
        screenSetUp("pTable")
        cont = pTableMini()

    for i in range(len(eSprites)):
        battle = eSprites[i].get_battle()
        if battle:
            screenSetUp("battle")
            eSprites[i].set_qSet(fetchQuestions())
            eSprites[i].set_qNum(0)

            while battle:
                screenDisplay("battle")
                complete = False
                questions = eSprites[i].get_qSet()[eSprites[i].get_qNum()]
                answer = eSprites[i].get_qSet()[eSprites[i].get_qNum()][5]

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
                        elif event.key == pygame.K_q:
                            print("q")
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        for j in range(len(buttons)):
                            if buttons[j].collision():
                                pygame.mixer.Sound.play(sounds[0])
                                if j+1 == answer:
                                    print("CORRECT")
                                    if eSprites[i].get_qNum() == len(eSprites[i].get_qSet())-1:
                                        print("ENd")
                                        eSprites.remove(eSprites[i])
                                        sSprites.clear()
                                        pygame.mixer.music.stop()
                                        if game.get_playMusic():
                                            pygame.mixer.music.load(music[1])
                                            pygame.mixer.music.play(-1)
                                            game.set_music(1)
                                        complete = True
                                    else:
                                        eSprites[i].set_qNum("inc")
                                else:
                                    print("INCORRECT")
                                    screen.fill(BURG)
                                    pygame.display.update()
                                    time.sleep(0.4) 
                                    player.decrease_health()
                                    hearts.pop()

                if player.get_health() <= 0:
                    print("DEATH")
                    screen.fill(BURG)
                    pygame.display.update()
                    time.sleep(1.5)
                    battle = False
                    cont = 1
                elif complete:
                    print("WON")
                    screen.fill(GREEN)
                    pygame.display.update()
                    time.sleep(0.5)
                    battle = False
                pygame.display.update()
                clock.tick(FPS)
            break

    pygame.display.update()
    clock.tick(FPS)
    return cont






player = SpriteClasses.Player()
game = GameClasses.GameSettings()
areaMap = GameClasses.AreaMap()
areaMap.reset()
mini = ShapeClasses.MiniWindow([100,100],[WIDTH-200, HEIGHT-200])
buttons = []
quickTexts = []
cSprites = []
eSprites = []
nSprites = []
sSprites = []
doors = []
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

    if running == "maps" and game.get_screen() == "home":
        areaMap.reset()
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