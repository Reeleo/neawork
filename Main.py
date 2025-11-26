import pygame
import random
import time
import SpriteClasses
import ShapeClasses
import GameClasses
pygame.init()

#---------------GLOBAL CONSTANTS---------------#
font20 = pygame.font.Font("freesansbold.ttf", 20)
font100 = pygame.font.Font("freesansbold.ttf",100)
WIDTH, HEIGHT = 1472, 960
FPS = 40
BLACK = (0,0,0)
WHITE = (255,255,255)
GREY = (100,100,100)
RED = (255,0,0)
BURG = (100,0,0)
DARK = (50,0,0)
GREEN = (0,200,0)
GRASS = (0,50,0)
BLUE = (0,0,255)
SKY = (60,60,225)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chemistry Game") 
clock = pygame.time.Clock()
TIME = time.time()

music = ["Menu.mp3","DoctorWeird.mp3","ForestBattle.mp3"]
sounds = [pygame.mixer.Sound("click.mp3")]


#---------------DISPLAYING ITEMS---------------#
def checkCollision(enemy):
        pPos = player.get_pos()
        ePos = enemy.get_pos()
        pMask = pygame.mask.from_surface(player.updateSprite())
        eMask = pygame.mask.from_surface(enemy.updateSprite(True))
        
        pos = [abs(ePos[0]-pPos[0]),abs(ePos[1]-pPos[1])]
        if pMask.overlap(eMask, (pos)):
            enemy.set_battle(True)
    
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
            pPos = obj.get_pos()
            lfoot = [pPos[0]+35,pPos[1]+102]
            rfoot = [pPos[0]+67,pPos[1]+102]

            speed = obj.get_speed()
            obj.set_validWalk("all",[True,True,True,True])
            tilePos = areaMap.get_waterPos()
            for i in range(len(tilePos)):
                if tilePos[i][1]*64 < lfoot[0]-speed < tilePos[i][1]*64+64 or tilePos[i][1]*64 < lfoot[0]+10-speed < tilePos[i][1]*64+64:
                    if tilePos[i][0]*64 < lfoot[1] < tilePos[i][0]*64+64 or tilePos[i][0]*64 < lfoot[1]+10 < tilePos[i][0]*64+64:
                        obj.set_validWalk(3,False)
                if tilePos[i][1]*64 < lfoot[0]+speed < tilePos[i][1]*64+64 or tilePos[i][1]*64 < lfoot[0]+10+speed < tilePos[i][1]*64+64:
                    if tilePos[i][0]*64 < lfoot[1] < tilePos[i][0]*64+64 or tilePos[i][0]*64 < lfoot[1]+10 < tilePos[i][0]*64+64:
                        obj.set_validWalk(1,False)
                if tilePos[i][1]*64 < lfoot[0] < tilePos[i][1]*64+64 or tilePos[i][1]*64 < lfoot[0] < tilePos[i][1]*64+64:
                    if tilePos[i][0]*64 < lfoot[1]+speed < tilePos[i][0]*64+64 or tilePos[i][0]*64 < lfoot[1]+10+speed < tilePos[i][0]*64+64:
                        obj.set_validWalk(2,False)
                if tilePos[i][1]*64 < lfoot[0] < tilePos[i][1]*64+64 or tilePos[i][1]*64 < lfoot[0] < tilePos[i][1]*64+64:
                    if tilePos[i][0]*64 < lfoot[1]-speed < tilePos[i][0]*64+64 or tilePos[i][0]*64 < lfoot[1]+10-speed < tilePos[i][0]*64+64:
                        obj.set_validWalk(0,False)

            
                if tilePos[i][1]*64 < rfoot[0]-speed < tilePos[i][1]*64+64 or tilePos[i][1]*64 < rfoot[0]+10-speed < tilePos[i][1]*64+64:
                    if tilePos[i][0]*64 < rfoot[1] < tilePos[i][0]*64+64 or tilePos[i][0]*64 < rfoot[1]+10 < tilePos[i][0]*64+64:
                        obj.set_validWalk(3,False)
                if tilePos[i][1]*64 < rfoot[0]+speed < tilePos[i][1]*64+64 or tilePos[i][1]*64 < rfoot[0]+10+speed < tilePos[i][1]*64+64:
                    if tilePos[i][0]*64 < rfoot[1] < tilePos[i][0]*64+64 or tilePos[i][0]*64 < rfoot[1]+10 < tilePos[i][0]*64+64:
                        obj.set_validWalk(1,False)
                if tilePos[i][1]*64 < rfoot[0] < tilePos[i][1]*64+64 or tilePos[i][1]*64 < rfoot[0] < tilePos[i][1]*64+64:
                    if tilePos[i][0]*64 < rfoot[1]+speed < tilePos[i][0]*64+64 or tilePos[i][0]*64 < rfoot[1]+10+speed < tilePos[i][0]*64+64:
                        obj.set_validWalk(2,False)
                if tilePos[i][1]*64 < rfoot[0] < tilePos[i][1]*64+64 or tilePos[i][1]*64 < rfoot[0] < tilePos[i][1]*64+64:
                    if tilePos[i][0]*64 < rfoot[1]-speed < tilePos[i][0]*64+64 or tilePos[i][0]*64 < rfoot[1]+10-speed < tilePos[i][0]*64+64:
                        obj.set_validWalk(0,False)
            
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
        screen.blit(obj.update(player.get_pos()),(obj.get_pos()))
        ePos = player.get_pos()
        lfoot = [ePos[0]+35,ePos[1]+102]
        rfoot = [ePos[0]+67,ePos[1]+102]

        speed = obj.get_speed()
        obj.set_validWalk("all",[True,True,True,True])
        tilePos = areaMap.get_waterPos()
        for i in range(len(tilePos)):
            if tilePos[i][1]*64 < lfoot[0]-speed < tilePos[i][1]*64+64 or tilePos[i][1]*64 < lfoot[0]+10-speed < tilePos[i][1]*64+64:
                if tilePos[i][0]*64 < lfoot[1] < tilePos[i][0]*64+64 or tilePos[i][0]*64 < lfoot[1]+10 < tilePos[i][0]*64+64:
                    obj.set_validWalk(3,False)
            if tilePos[i][1]*64 < lfoot[0]+speed < tilePos[i][1]*64+64 or tilePos[i][1]*64 < lfoot[0]+10+speed < tilePos[i][1]*64+64:
                if tilePos[i][0]*64 < lfoot[1] < tilePos[i][0]*64+64 or tilePos[i][0]*64 < lfoot[1]+10 < tilePos[i][0]*64+64:
                    obj.set_validWalk(1,False)
            if tilePos[i][1]*64 < lfoot[0] < tilePos[i][1]*64+64 or tilePos[i][1]*64 < lfoot[0] < tilePos[i][1]*64+64:
                if tilePos[i][0]*64 < lfoot[1]+speed < tilePos[i][0]*64+64 or tilePos[i][0]*64 < lfoot[1]+10+speed < tilePos[i][0]*64+64:
                    obj.set_validWalk(2,False)
            if tilePos[i][1]*64 < lfoot[0] < tilePos[i][1]*64+64 or tilePos[i][1]*64 < lfoot[0] < tilePos[i][1]*64+64:
                if tilePos[i][0]*64 < lfoot[1]-speed < tilePos[i][0]*64+64 or tilePos[i][0]*64 < lfoot[1]+10-speed < tilePos[i][0]*64+64:
                    obj.set_validWalk(0,False)

        
            if tilePos[i][1]*64 < rfoot[0]-speed < tilePos[i][1]*64+64 or tilePos[i][1]*64 < rfoot[0]+10-speed < tilePos[i][1]*64+64:
                if tilePos[i][0]*64 < rfoot[1] < tilePos[i][0]*64+64 or tilePos[i][0]*64 < rfoot[1]+10 < tilePos[i][0]*64+64:
                    obj.set_validWalk(3,False)
            if tilePos[i][1]*64 < rfoot[0]+speed < tilePos[i][1]*64+64 or tilePos[i][1]*64 < rfoot[0]+10+speed < tilePos[i][1]*64+64:
                if tilePos[i][0]*64 < rfoot[1] < tilePos[i][0]*64+64 or tilePos[i][0]*64 < rfoot[1]+10 < tilePos[i][0]*64+64:
                    obj.set_validWalk(1,False)
            if tilePos[i][1]*64 < rfoot[0] < tilePos[i][1]*64+64 or tilePos[i][1]*64 < rfoot[0] < tilePos[i][1]*64+64:
                if tilePos[i][0]*64 < rfoot[1]+speed < tilePos[i][0]*64+64 or tilePos[i][0]*64 < rfoot[1]+10+speed < tilePos[i][0]*64+64:
                    obj.set_validWalk(2,False)
            if tilePos[i][1]*64 < rfoot[0] < tilePos[i][1]*64+64 or tilePos[i][1]*64 < rfoot[0] < tilePos[i][1]*64+64:
                if tilePos[i][0]*64 < rfoot[1]-speed < tilePos[i][0]*64+64 or tilePos[i][0]*64 < rfoot[1]+10-speed < tilePos[i][0]*64+64:
                    obj.set_validWalk(0,False)

    elif type == "char":
        screen.blit(obj.update(),(obj.get_pos()))
        if obj.collision(player.get_pos()):
            playerpos, playersize = player.get_pos(), player.get_size()
            displayText("SPACE", font20, WHITE, [playerpos[0]+playersize[0]/2, playerpos[1]-20])
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE] and obj.get_timer(time.time()) > 1.5:
                quickTexts.append(ShapeClasses.QuickText([playerpos[0]+playersize[0]/2, playerpos[1]-20-50],obj.get_dialogue(),time.time()))
                obj.set_timer(time.time())

    elif type == "special":
        screen.blit(obj.update(),(obj.get_pos()))
        if obj.collision(player.get_pos()):
            playerpos = player.get_pos()
            playersize = player.get_size()
            displayText("SPACE", font20, WHITE, [playerpos[0]+playersize[0]/2, playerpos[1]-20])
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                obj.set_specialTime(True)

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

def displayResult(t1,t2):
    pygame.draw.rect(screen,BLACK,[175,175,WIDTH-350, HEIGHT-350])
    pygame.draw.rect(screen,WHITE,[180,180,WIDTH-360, HEIGHT-360])
    pygame.draw.rect(screen,BLACK,[200,200,WIDTH-400, HEIGHT-400])
    displayText(t1, font100, WHITE, [WIDTH/2, 400])
    displayText(t2, font20, WHITE, [WIDTH/2, 550])

def qtHandelling():
    deleteing = []
    for i in range(len(quickTexts)):
        if quickTexts[i].get_visible():
            displayText(quickTexts[i].get_text(),font20,quickTexts[i].get_colours(),[quickTexts[i].get_pos()[0],quickTexts[i].get_pos()[1]+i*30])
            remove = quickTexts[i].update(time.time())
            if remove:
                deleteing.append(i)
    for _ in range(len(deleteing)):
        quickTexts.pop(0)


#---------------SETUP/DISPLAY---------------#
def screenSetUp(screenType):
    #1
    if screenType == "menu":
        buttons.clear()
        if game.get_music() == -1 and game.get_playMusic():
            pygame.mixer.music.load(music[0])
            pygame.mixer.music.play(-1)
            game.set_music(0)
        buttons.append(ShapeClasses.Button([WIDTH/4-90,3*HEIGHT/4],[180,80],"EXIT",RED))
        buttons.append(ShapeClasses.Button([3*WIDTH/4-90, 3*HEIGHT/4],[180,80],"START",RED))
        buttons.append(ShapeClasses.Button([WIDTH/2-90, HEIGHT/2],[180,80],"HOW TO PLAY",RED))

    #2
    if screenType == "htp":
        buttons.clear()
        inputBoxes.clear()
        inputBoxes.append(ShapeClasses.Button([180,680],[450,80],"",RED))
        buttons.append(ShapeClasses.Button([WIDTH-300, 200],[180,80],"MENU",RED))

    #3
    if screenType == "savefiles":
        buttons.clear()
        buttons.append(ShapeClasses.Button([400,100],[1000,150],"Save1",RED))
        buttons.append(ShapeClasses.Button([400,300],[1000,150],"Save2",RED))
        buttons.append(ShapeClasses.Button([400,500],[1000,150],"Save3",RED))
        buttons.append(ShapeClasses.Button([WIDTH/4-200, 3*HEIGHT/4],[180,80],"MENU",RED))

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
        doors[0].assign_type(game.get_collectTypes())
        doors[1].assign_type(game.get_collectTypes())
        player.set_validWalk("all",[True,True,True,True])

    #5
    if screenType == "inventory":
        buttons.clear()
        cSprites.clear()
        buttons.append(ShapeClasses.Button([1150,750],[180,80],"RETURN",GREEN))
        for j in range(12):
            cSprites.append(SpriteClasses.Collectable([120, 100+j*60],j))
        for k in range(12):
            cSprites[k].assign_type(game.get_collectTypes())
        if game.get_screen() == "home":
            buttons.append(ShapeClasses.Button([390,360],[400,80],"EXTRACT",GREEN))
            buttons.append(ShapeClasses.Button([850,360],[400,80],"CRAFT",GREEN))
            buttons.append(ShapeClasses.Button([390,480],[400,80],"ACHIEVEMENTS",GREEN))
            buttons.append(ShapeClasses.Button([850,480],[400,80],"HEAL",GREEN))
            buttons.append(ShapeClasses.Button([610,600],[400,80],"ADD QUESTIONS",GREEN))
        mini.set_size([WIDTH-200, HEIGHT-200])
        mini.set_pos([100, 100])
        
    #6
    if screenType == "extract":
        buttons.clear()
        cSprites.clear()
        buttons.append(ShapeClasses.Button([1150,750],[180,80],"RETURN",GREEN))
        for i in range(12):
            buttons.append(ShapeClasses.Button([140+(i)*100, 200],[80,80],i,GREEN))
        for j in range(12):
            cSprites.append(SpriteClasses.Collectable([140+j*100, 200],j))
        for k in range(12):
            cSprites[k].assign_type(game.get_collectTypes())
        mini.set_size([WIDTH-200, HEIGHT-200])
        mini.set_pos([100, 100])

    #7
    if screenType == "craft":
        buttons.clear()
        cSprites.clear()
        inputBoxes.clear()
        buttons.append(ShapeClasses.Button([1150,750],[180,80],"RETURN",GREEN))
        buttons.append(ShapeClasses.Button([660,200],[80,80],"GO",GREEN))
        inputBoxes.append(ShapeClasses.Button([320,200],[320,80],"",GREEN))

        mini.set_size([WIDTH-200, HEIGHT-200])
        mini.set_pos([100, 100])

    #8
    if screenType == "pTable":
        buttons.clear()
        buttons.append(ShapeClasses.Button([1240,610],[90,180],"RETURN",RED))
        mini.set_size([WIDTH-200, HEIGHT-255])
        mini.set_pos([100, 130])

    #9 
    if screenType == "achieve":
        buttons.clear()
        buttons.append(ShapeClasses.Button([1150,750],[180,80],"RETURN",GREEN))
        buttons.append(ShapeClasses.Button([140, 200],[280,80],"Beat the BOSS",GREEN))
        buttons.append(ShapeClasses.Button([460, 200],[280,80],"ESCAPE through the GATE",GREEN))
        mini.set_size([WIDTH-200, HEIGHT-200])
        mini.set_pos([100, 100])

    #10 
    if screenType == "addQuestions":
        buttons.clear()
        buttons.append(ShapeClasses.Button([1150,750],[180,80],"RETURN",GREEN))
        buttons.append(ShapeClasses.Button([1260, 500],[80,80],"ADD",GREEN))
        buttons.append(ShapeClasses.Button([1260,300],[80,80],"1",GREEN))
        buttons.append(ShapeClasses.Button([1260, 400],[80,80],game.get_diff(),GREEN))
        buttons.append(ShapeClasses.Button([140,750],[180,80],"RESET",GREEN))
        inputBoxes.append(ShapeClasses.Button([150,350],[1060,80],"",GREEN))
        inputBoxes.append(ShapeClasses.Button([150,500],[250,80],"",GREEN))
        inputBoxes.append(ShapeClasses.Button([420,500],[250,80],"",GREEN))
        inputBoxes.append(ShapeClasses.Button([690,500],[250,80],"",GREEN))
        inputBoxes.append(ShapeClasses.Button([960,500],[250,80],"",GREEN))
        mini.set_size([WIDTH-200, HEIGHT-200])
        mini.set_pos([100, 100])

    #11
    if screenType == "pause":
        buttons.clear()
        for i in range(8):
            if i == 0:
                buttons.append(ShapeClasses.Button([1000,350],[80,80],"+",RED))
            elif i == 1:
                buttons.append(ShapeClasses.Button([680,350],[80,80],"+",RED))
            elif i == 2:
                buttons.append(ShapeClasses.Button([400,350],[80,80],str(game.get_showAll()),RED))
            elif i == 3:
                buttons.append(ShapeClasses.Button([WIDTH/2+120, 3*HEIGHT/4],[180,80],"RETURN",RED))
            elif i == 4:
                buttons.append(ShapeClasses.Button([WIDTH/2-300, 3*HEIGHT/4],[180,80],"MENU",RED))
            elif i == 5:
                buttons.append(ShapeClasses.Button([WIDTH/2-90, 3*HEIGHT/4],[180,80],"SAVE",RED))
            elif i == 6:
                buttons.append(ShapeClasses.Button([400,450],[80,80],str(game.get_playMusic()),RED))
            elif i == 7:
                buttons.append(ShapeClasses.Button([1000,450],[80,80],str(game.get_tutorial()),RED))

    #12
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
        areaMap.createAreaMap(game.get_diff())
        tiles, blitList, setPlayer = areaMap.loadMap(player.get_pos(),player.get_size(),WIDTH,HEIGHT)
        for item in range(len(blitList)):
            if blitList[item][2]:
                if blitList[item][3] == "collect":
                    cSprites.append(SpriteClasses.Collectable([blitList[item][0],blitList[item][1]],blitList[item][4]))
                    cSprites[-1].assign_type(game.get_collectTypes())
                elif blitList[item][3] == "enemy":
                    eSprites.append(SpriteClasses.Enemy([blitList[item][0],blitList[item][1]],blitList[item][4],game.get_diff()))
                elif blitList[item][3] == "char":
                    nSprites.append(SpriteClasses.Character([blitList[item][0],blitList[item][1]],random.randint(1,10)))
        for i in range(player.get_health()):
            hearts.append(SpriteClasses.Sprite([2+i*60, 2],[50,50],2.5,BLACK,pygame.image.load("collectablesSprites.bmp")))
            
    #13
    if screenType == "minimap":
        buttons.clear()
        mini.set_pos([100,100])
        mini.set_size([WIDTH-200, HEIGHT-192])
        buttons.append(ShapeClasses.Button([1187,783],[180,80],"RETURN",RED))

    #14
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
                buttons.append(ShapeClasses.Button([615+i*380, 400],[360,80],i+1,RED))
            else:
                buttons.append(ShapeClasses.Button([615+(i-2)*380, 500],[360,80],i+1,RED))
        sSprites.append(SpriteClasses.Character([30,180],"enemyImage"))
        mini.set_size([WIDTH-200, HEIGHT-200])
        mini.set_pos([100, 100])
        for i in range(player.get_health()):
            hearts.append(SpriteClasses.Sprite([10+i*60, 20],[50,50],2.5,BLACK,pygame.image.load("collectablesSprites.bmp")))  

    #15
    if screenType == "boss":
        buttons.clear()
        buttons.append(ShapeClasses.Button([1150,750],[180,80],"RETURN",GREEN))
        buttons.append(ShapeClasses.Button([350,350],[200,80],"ester",GREEN))
        buttons.append(ShapeClasses.Button([650,250],[200,80],"nitrile",GREEN))
        buttons.append(ShapeClasses.Button([950,350],[200,80],"carbon",GREEN))
        buttons.append(ShapeClasses.Button([500,600],[200,80],"alcohol",GREEN))
        buttons.append(ShapeClasses.Button([800,600],[200,80],"amide",GREEN))
        mini.set_size([WIDTH-200, HEIGHT-200])
        mini.set_pos([100, 100])
    
    #16
    if screenType == "gate":
        buttons.clear()
        buttons.append(ShapeClasses.Button([1150,750],[180,80],"RETURN",GREEN))
        buttons.append(ShapeClasses.Button([WIDTH/2-50,HEIGHT/2-40],[100,80],"Give KEY",GREEN))
        mini.set_size([WIDTH-200, HEIGHT-200])
        mini.set_pos([100, 100])


def screenDisplay(screenType):
    #1
    if screenType == "menu":
        screen.fill(BURG)
        pygame.draw.rect(screen,RED,[20,20,WIDTH-40, HEIGHT-40])
        pygame.draw.rect(screen,BLACK,[40,40,WIDTH-80, HEIGHT-80])
        displayText("ChemCraft", font100, WHITE, [WIDTH/2, 200])
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
        displayText("Use the WASD buttons to move", font20, WHITE, [330, 550])
        displayText("Press SPACE to interact and pick up items", font20, WHITE, [830, 550])
        displayText("To use input boxes, click to activate and then type", font20, WHITE, [423,780])
        displayText("Use the mouse to interact", font20, WHITE, [1260, 310])
        displayText("with buttons and input boxes", font20, WHITE, [1260, 335])
        for i in range(len(buttons)):
            displayObject("button",buttons[i])
        for j in range(len(inputBoxes)):
            displayObject("button",inputBoxes[i])

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
        displayImage(pygame.image.load("homeBackground.png"),[WIDTH/2-400,120],2.5,[320,320])
        pygame.draw.rect(screen,BURG,[0, HEIGHT-180, WIDTH, 180])
        pygame.draw.rect(screen,BLACK,(0,780,WIDTH,10))
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
        y = 240
        xcount, ycount = 0, 0
        collection = player.get_collect()
        for item in collection:
            itemname = item
            if itemname == "wplant":
                itemname = "waterplant"
            elif itemname == "sorck":
                itemname = "smallrock"
            elif itemname == "lrock":
                itemname = "largerock"
            elif itemname == "volrock":
                itemname = "volcanicrock"
            displayText(f"{itemname}: {collection[item]}", font20, WHITE, [x+xcount, y+ycount])
            xcount += 200
            if xcount == 800:
                xcount = 0 
                ycount += 40
  
    #6
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
        displayText(f"PEBBLE: {collection["pebble"]}", font20, WHITE, [x, y])
        displayText(f"BUG: {collection["bug"]}", font20, WHITE, [x+200, y])
        displayText(f"FLOWER: {collection["flower"]}", font20, WHITE, [x+400, y])
        displayText(f"LEAF: {collection["leaf"]}", font20, WHITE, [x+600, y])
        displayText(f"FRUIT: {collection["fruit"]}", font20, WHITE, [x+800, y])
        displayText(f"WATER PLANT: {collection["wplant"]}", font20, WHITE, [x+1000, y])
        displayText(f"BUSH: {collection["bush"]}", font20, WHITE, [x, y+30])
        displayText(f"BIG ROCK: {collection["rock"]}", font20, WHITE, [x+200, y+30])
        displayText(f"GEMSTONE: {collection["gem"]}", font20, WHITE, [x+400, y+30])
        displayText(f"VOLCANIC ROCK: {collection["volrock"]}", font20, WHITE, [x+600, y+30])

        displayText(f"FRESHWATER: {collection["freshwater"]}", font20, WHITE, [x, y+60])
        displayText(f"SEAWATER: {collection["saltwater"]}", font20, WHITE, [x+200, y+60])

    #7
    if screenType == "craft":
        pygame.draw.rect(screen,WHITE,(100,HEIGHT/2-75,WIDTH-200,10))
        displayObject("mini",mini)
        displayText("CRAFTING:", font20, WHITE, [212, 150])
        displayText("Synthesis of:", font20, WHITE, [222, 235])
        displayText("please use lowercase", font20, WHITE, [642, 300])
        pygame.draw.rect(screen,WHITE,(100,HEIGHT/2-110,WIDTH-200,10))
        for i in range(len(buttons)):
            displayObject("button",buttons[i])
        for j in range(len(inputBoxes)):
            displayObject("button",inputBoxes[j])
        
        x = 270
        y = 460
        xcount, ycount = 0, 0
        collection = player.get_chemicals()
        for item in collection:
            itemname = item
            displayText(f"{itemname}: {collection[item]}", font20, WHITE, [x+xcount, y+ycount])
            xcount += 220
            if xcount >= 880:
                xcount = 0 
                ycount += 40

    #8
    if screenType == "pTable":
        pygame.draw.rect(screen,WHITE,(100,HEIGHT/2-75,WIDTH-200,10))
        displayObject("mini",mini)
        displayObject("button",buttons[0])
        displayImage(pygame.image.load("pTable.png"),[110,140],0.9,[WIDTH-250,HEIGHT-200])
    
    #9 
    if screenType == "achieve":
        pygame.draw.rect(screen,WHITE,(100,HEIGHT/2-75,WIDTH-200,10))
        displayObject("mini",mini)
        displayText("Your Achievements:", font20, WHITE, [231, 150])
        for i in range(len(buttons)):
            displayObject("button",buttons[i])
        playerAchieve = player.get_achievements()
        for j in range(len(playerAchieve)):
            displayText(f"Achieved = {playerAchieve[j]}", font20, WHITE, [280+j*320, 310])

    #10 
    if screenType == "addQuestions":
        pygame.draw.rect(screen,WHITE,(100,HEIGHT/2-75,WIDTH-200,10))
        displayObject("mini",mini)
        displayText("Adding Questions:", font20, WHITE, [210, 140])
        displayText("The Question:", font20, WHITE, [213,330])
        displayText("The Answers:", font20, WHITE, [213,480])
        for i in range(len(buttons)):
            displayObject("button",buttons[i])
        for j in range(len(inputBoxes)):
            displayObject("button",inputBoxes[j])
        
    #11
    if screenType == "pause":
        screen.fill(BURG)  
        pygame.draw.rect(screen,RED,[20,20,WIDTH-40, HEIGHT-40])
        pygame.draw.rect(screen,BLACK,[40,40,WIDTH-80, HEIGHT-80])
        displayText(f"Difficulty: {game.get_diff()}", font20, WHITE, [900, 390])
        displayText(f"Speed: {player.get_speed()}", font20, WHITE, [620, 390])
        displayText(f"Display whole MiniMap: ", font20, WHITE, [270, 390])
        displayText(f"Play Music: ", font20, WHITE, [330, 490])
        displayText(f"Show Tutorial: ", font20, WHITE, [920, 490])
        if game.get_tutorial():
            displayText("(Displays tips)", font20, WHITE, [1170, 490])
            displayText("(Effects Health and Questions)", font20, WHITE, [1250, 390])
        for i in range(len(buttons)):
            displayObject("button",buttons[i])

    #12
    if screenType == "maps":
        tiles, blitList, setPlayer = areaMap.loadMap(player.get_pos(),player.get_size(),WIDTH,HEIGHT)
        player.set_pos(setPlayer,WIDTH,HEIGHT)
        if setPlayer != -1:
            cSprites.clear()
            eSprites.clear()
            nSprites.clear()
            sSprites.clear()
            if blitList == "BOSS":
                sSprites.append(SpriteClasses.Character([WIDTH/2-250,HEIGHT/2-350],"boss"))
            elif blitList == "GATE":
                sSprites.append(SpriteClasses.Character([WIDTH-200,HEIGHT/2],"gate"))
            else:
                for item in range(len(blitList)):
                    if blitList[item][2]:
                        if blitList[item][3] == "collect":
                            cSprites.append(SpriteClasses.Collectable([blitList[item][0],blitList[item][1]],blitList[item][4]))
                            cSprites[-1].assign_type(game.get_collectTypes())
                        elif blitList[item][3] == "enemy":
                            eSprites.append(SpriteClasses.Enemy([blitList[item][0],blitList[item][1]],blitList[item][4],game.get_diff()))
                        elif blitList[item][3] == "char":
                            nSprites.append(SpriteClasses.Character([blitList[item][0],blitList[item][1]],random.randint(1,10)))

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
     
    #13
    if screenType == "minimap":
        displayObject("mini",mini)
        displayObject("button",buttons[0])
        tiles = areaMap.drawMiniMap(WIDTH,HEIGHT,game.get_showAll())
        for i in range(len(tiles)):
            for j in range(len(tiles[i])):
                displayObject("tile",tiles[i][j])
        pygame.draw.rect(screen,SKY,[(areaMap.get_pos()[1]-1)*147+160,(areaMap.get_pos()[0]-1)*96+135,20,20])
        displayText(f"PlayerCol = {areaMap.get_pos()[1]}",font20,WHITE,[1270,130])
        displayText(f"PlayerRow = {areaMap.get_pos()[0]}",font20,WHITE,[1270,160])

    #14
    if screenType == "battle":
        screen.fill(BLACK)
        displayObject("mini",mini)
        displayObject("special",sSprites[0])
        displayText("BATTLE:",font100,WHITE,[320, 180])
        
        for i in range(len(buttons)):
            displayObject("button",buttons[i])
        for j in range(len(hearts)):
            displayObject("heart",hearts[j])

    #15
    if screenType == "boss":
        pygame.draw.rect(screen,WHITE,(100,HEIGHT/2-75,WIDTH-200,10))
        displayObject("mini",mini)
        displayText("BOSS:", font100, WHITE, [255, 150])
        for i in range(len(buttons)):
            displayObject("button",buttons[i])
    
    #16
    if screenType == "gate":
        pygame.draw.rect(screen,WHITE,(100,HEIGHT/2-75,WIDTH-200,10))
        displayObject("mini",mini)
        displayText("GATE:", font100, WHITE, [255, 150])
        displayText("Do you have the KEY:", font20, WHITE, [215, 250])
        for i in range(len(buttons)):
            displayObject("button",buttons[i])


#---------------PLAYER DATA---------------#
def loadGame():
    i = 0
    cont = True
    if game.get_saveFile() == 1:
        file = open("saveData1.txt","r")
    elif game.get_saveFile() == 2:
        file = open("saveData2.txt","r")
    elif game.get_saveFile() == 3:
        file = open("saveData3.txt","r")
    questions = []
    while cont:
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
            player.set_speed(saveData[1],"set")
            if saveData[2] == "True":
                player.set_hasKey()
            if saveData[3] == "False":
                game.set_tutorial(False)
            if saveData[4] == "True":
                player.set_achievements(True,0)
            else:
                player.set_achievements(False,0)
            if saveData[5] == "True":
                player.set_achievements(True,1)
            else:
                player.set_achievements(False,1)
        elif i > 2:
            if line == "":
                cont = False 
            else:
                questions.append(line)
        i += 1
    resetQuestions()
    for j in range(len(questions)):
        addingQuestion(questions[j])
    player.set_int()
    file.close()

def saveGame():
    if game.get_saveFile() == 1:
        file = open("saveData1.txt","w")
    elif game.get_saveFile() == 2:
        file = open("saveData2.txt","w")
    elif game.get_saveFile() == 3:
        file = open("saveData3.txt","w")
    collectLine = ""
    chemicalLine = ""
    gameLine = ""
    collection = player.get_collect()
    chemicals = player.get_chemicals()
    for item in player.get_collect():
        collectLine += str(collection[item])+","
    for chem in player.get_chemicals():
        chemicalLine += str(chemicals[chem])+","
    gameLine += f"{game.get_diff()},{str(player.get_speed())},{str(player.get_hasKey())},{str(game.get_tutorial())},{player.get_achievements()[0]},{player.get_achievements()[1]},"
    
    cont = True
    qData = []
    ogQuestions = []
    questionLine = ""
    qFile = open("questions.txt","r")
    for _ in range(40):
        ogQuestions.append(qFile.readline())
    while cont:
        qData.append(qFile.readline())
        for j in range(len(qData)):
            if qData[j] == "!":
                cont = False
    print(qData)
    for k in range(len(qData)):
        if qData[k] != "!":
            questionLine += qData[k] 
    print(questionLine)
    qFile.close()

    file.writelines(collectLine)
    file.writelines("\n") 
    file.writelines(chemicalLine)
    file.writelines("\n") 
    file.writelines(gameLine)
    file.writelines("\n")
    file.writelines(questionLine)
    file.close()

#---------------SCREEN SUBFUNCTIONS---------------#
def extraction(item):
    chances = game.get_itemChances()[item]
    randomNum = random.randint(0,len(chances)-1)
    chem = chances[randomNum][0]
    amount = chances[randomNum][1]
    player.set_extracted(item,chem,amount)
    chems = player.get_chemicals()
    quickTexts.append(ShapeClasses.QuickText([550,500],f"{item}, {chem}, {chems[chem]}",time.time()))
    return chem
    
def synthesis(setUp,items):
    if setUp:
        buttons.clear()
        inputBoxes.clear()
        buttons.append(ShapeClasses.Button([1150,750],[180,80],"RETURN",GREEN))
        buttons.append(ShapeClasses.Button([1230,650],[100,80],"CHECK",GREEN))
        buttons.append(ShapeClasses.Button([1230,250],[100,80],"HINT",GREEN))
        for i in range(len(items)):
            try:
                items[i] = items[i].split(".") 
            except:
                pass

        for j in range(len(items)):
            if j != 0:
                for k in range(len(items[j])):
                    if j == 1 and k == 0:
                        inputBoxes.append(ShapeClasses.Button([290,400],[260,80],"",GREEN))
                    elif j == 1 and k == 1:
                        inputBoxes.pop(-1)
                        inputBoxes.append(ShapeClasses.Button([130,400],[260,80],"",GREEN))
                        inputBoxes.append(ShapeClasses.Button([430,400],[260,80],"",GREEN))

                    elif j == 2 and k == 0:
                        inputBoxes.append(ShapeClasses.Button([950,400],[260,80],"",GREEN))
                    elif j == 2 and k == 1:
                        inputBoxes.pop(-1)
                        inputBoxes.append(ShapeClasses.Button([790,400],[260,80],"",GREEN))
                        inputBoxes.append(ShapeClasses.Button([1090,400],[260,80],"",GREEN))

                    elif j == 3 and k == 0:
                        inputBoxes.append(ShapeClasses.Button([610,520],[260,80],"",GREEN))
                    elif j == 3 and k == 1:
                        inputBoxes.pop(-1)
                        inputBoxes.append(ShapeClasses.Button([450,520],[260,80],"",GREEN))
                        inputBoxes.append(ShapeClasses.Button([750,520],[260,80],"",GREEN))  
            
    else:
        pygame.draw.rect(screen,WHITE,(100,HEIGHT/2-75,WIDTH-200,10))
        displayObject("mini",mini)
        displayText("CRAFTING: Input the correct reactants, conditions and products", font20, WHITE, [440, 140])
        displayText("reactants:", font20, WHITE, [410, 350])
        displayText("products:", font20, WHITE, [1070, 350])
        displayText("catalyst/condition:", font20, WHITE, [350, 565])
        displayText("-->", font20, WHITE, [740, 440])
        for i in range(len(buttons)):
            displayObject("button",buttons[i])
        for j in range(len(inputBoxes)):
            displayObject("button",inputBoxes[j])

def checkProduct(txt):
    valid = False
    product = ""
    file = open("synthesisFile.txt","r")
    line = file.readline()
    data = line.split(",")
    for i in range(len(data)):
        data[i] = data[i].split("/")
    for j in range(len(data)):
        if data[j][0] == txt:
            valid = True  
            product = data[j]
            break  
    if not valid:
        quickTexts.append(ShapeClasses.QuickText([800,240],f"INVALID",time.time()))
    file.close()
    return valid, product

def checkEquation(txt,check):
    for i in range(len(check)):
        try:
            check[i] = check[i].split(".") 
        except:
            pass
    length = 0
    for j in range(len(check)):
        for k in range(len(check[j])):
            length += 1
    if length > len(txt):
        check.pop(0)

    validlen = 0
    reactants = []
    products = []
    others = []
    for i in range(len(check)):
        for j in range(len(check[i])):
            if i == 0:
                reactants.append(check[i][j])
            elif i == 1:
                products.append(check[i][j])
            elif i == 2:
                others.append(check[i][j])
    inputR = []
    inputP = []
    inputO = []
    for k in range(len(reactants)):
        inputR.append(txt[k])
    for k in range(len(products)):
        inputP.append(txt[k+len(reactants)])
    for k in range(len(others)):
        inputO.append(txt[k+len(reactants)+len(products)])
    txt = [inputR,inputP,inputO]
        
    for r in range(len(reactants)):
        for t in range(len(txt[0])):
            if txt[0][t] == reactants[r]:
                validlen += 1
                txt[0][t] = ""
    
    for p in range(len(products)):
        for t in range(len(txt[1])):
            if txt[1][t] == products[p]:
                validlen += 1
                txt[1][t] = ""
    
    for o in range(len(others)):
        for t in range(len(txt[2])):
            if txt[2][t] == others[o]:
                validlen += 1
                txt[2][t] = ""
    
    length = 0
    for i in range(len(check)):
        for j in range(len(check[i])):
            length += 1

    message = []
    if length == validlen:
        removeList = []
        chems = player.get_chemicals()
        for i in range(len(check[0])):
            if chems[check[0][i]] > 0:
                removeList.append([check[0][i],chems[check[0][i]]-1])
            else:
                message.append(f"you dont have {check[0][i]}")
                
        for j in range(len(check[2])):
            if check[2][j] == "sufuricacid" or check[2][j] == "nickle":
                if chems[check[2][j]] > 0:
                    removeList.append([check[0][i],chems[check[0][i]]-1])
                else:
                    message.append(f"you dont have {check[2][j]}")
        
        for k in range(len(removeList)):
            player.set_chemicals(removeList[k][0],removeList[k][1])

    if validlen == length and message == []:
        return True, message
    return False, message


def fetchQuestions():
    c = []
    chosen = []
    qSet = []
    diff = game.get_diff()
    diff = "Testing"
    cont = True
    lines = []
    file = open("questions.txt","r")
    while cont:
        line = file.readline()
        qSet.append(line.split(","))
        lines.append(line)
        for i in range(len(lines)):
            if lines[i] == "!":
                cont = False
    for i in range(len(lines)-1):
        qSet[i][5] = int(qSet[i][5])
    file.close()

    for _ in range(3):
        count = 0
        valid = False
        while not valid:
            repeat = False
            c1 = random.randint(0,19)
            for j in range(len(c)):
                if c[j] == c1:
                    repeat = True
            if not repeat and qSet[c1][6] == diff:
                valid  = True
            count += 1
            if count > 40:
                diff = "Testing"
        c.append(c1)
    chosen = [qSet[c[0]],qSet[c[1]],qSet[c[2]]]
    return chosen

def resetQuestions():
    data = []
    file = open("questions.txt","r")
    for i in range(40):
        data.append(file.readline())
    file.close()
    file = open("questions.txt","w")
    for j in range(len(data)):
        file.writelines(data[j])
    file.writelines("!")
    file.close()
    
def addingQuestion(data):
    cont = True
    filedata = []
    file = open("questions.txt","r")
    while cont:
        line = file.readline()
        filedata.append(line)
        for i in range(len(filedata)):
            if filedata[i] == "!":
                cont = False
    file.close()
    filedata[-1] = data
    filedata.append("!")
    file = open("questions.txt","w")
    for i in range(len(filedata)):
        file.writelines(filedata[i])
    file.close()

def displayTip(item):
    file = open("tipsfile.txt","r")
    lines = []
    cont = True
    while cont:
        lines.append(file.readline())
        for i in range(len(lines)):
            if lines[i] == "!":
                cont = False
    file.close()
    index = -1
    for k in range(len(lines)):
        lines[k] = lines[k].split(",")
        if lines[k][0] == item[0]:
            index = k
            print("found")
            break
    if index == -1:
        tip = "no tip"
    else:
        tip = lines[index][1]
    print(item)
    quickTexts.append(ShapeClasses.QuickText([1050,200],tip,time.time()))

def battleReward():
    rewards = game.get_rewards()
    choice = random.randint(0,len(rewards)-1)
    num = random.randint(1,4)
    return rewards[choice],num


#---------------SCREEN FUNCTIONS---------------#
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
            else:
                for box in range(len(inputBoxes)):
                    if inputBoxes[box].get_isInput():
                        if event.key == pygame.K_BACKSPACE:
                            inputBoxes[box].decrease_text()
                        elif event.key == pygame.K_RETURN:
                            inputBoxes[box].set_text("")
                        else:
                            inputBoxes[box].increase_text(event.unicode)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if buttons[0].collision():
                pygame.mixer.Sound.play(sounds[0])
                cont = 2
            elif inputBoxes[0].collision():
                if inputBoxes[0].get_isInput():
                    inputBoxes[0].set_isInput(False)
                else:
                    inputBoxes[0].set_isInput(True)

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
                        displayText("Saved", font20, WHITE, [WIDTH/2, 3*HEIGHT/4-40])
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
    qtHandelling()
    clock.tick(FPS)
    pygame.display.update()
    return cont


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
                    cont = 2
            if event.type == pygame.MOUSEBUTTONDOWN:
                if buttons[0].collision():
                    pygame.mixer.Sound.play(sounds[0])
                    pTableTime = False
                    cont = 2
        pygame.display.update()
        clock.tick(FPS)
    return cont 

def achieveMini():
    cont = 0
    achieveTime = True
    while achieveTime:
        screenDisplay("achieve")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                achieveTime = False
                cont = 1
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    achieveTime = False
                    cont = 2
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i in range(len(buttons)):
                    if buttons[i].collision():
                        pygame.mixer.Sound.play(sounds[0])
                        achieveTime = False
                        cont = 2
        pygame.display.update()
        clock.tick(FPS)
    return cont 

def addQMini():
    cont = 0
    addQTime = True
    while addQTime:
        screenDisplay("addQuestions")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                addQTime = False
                cont = 1
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    addQTime = False
                    cont = 2
                else:
                    for box in range(len(inputBoxes)):
                        if inputBoxes[box].get_isInput():
                            if event.key == pygame.K_BACKSPACE:
                                inputBoxes[box].decrease_text()
                            else:
                                inputBoxes[box].increase_text(event.unicode)
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i in range(len(buttons)):
                    if buttons[i].collision():
                        pygame.mixer.Sound.play(sounds[0])
                        if i == 0:
                            addQTime = False
                            cont = 2
                        elif i == 1:
                            questionData = ""
                            valid = True
                            for j in range(len(inputBoxes)):
                                text = inputBoxes[j].get_text()
                                if text == "":
                                    valid = False
                                    break
                                else:
                                    questionData += text + ","
                            questionData += buttons[2].get_text() + "," + buttons[3].get_text() + ",\n"
                            if valid:
                                addingQuestion(questionData)
                                displayResult("Success","your question has been added")
                                pygame.display.update()
                                time.sleep(1)
                            else:
                                quickTexts.append(ShapeClasses.QuickText([WIDTH/2,650],f"Invalid input",time.time()))  
                        elif i == 2:
                            num = buttons[i].get_text()
                            num = int(num) + 1
                            if num > 4:
                                num = 1
                            buttons[i].set_text(str(num))
                        elif i == 3:
                            diff = buttons[i].get_text()
                            if diff == "Easy":
                                diff = "Medium"
                            elif diff == "Medium":
                                diff = "Hard"
                            else:
                                diff = "Easy"
                            buttons[i].set_text(str(diff))
                        elif i == 4:
                            resetQuestions()
                            displayResult("Done","the questions have been reset")
                            pygame.display.update()
                            time.sleep(1)
                    for k in range(len(inputBoxes)):
                        if inputBoxes[k].collision():
                            for box in range(len(inputBoxes)):
                                inputBoxes[box].set_isInput(False)
                            inputBoxes[k].set_isInput(True)
        qtHandelling()
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
                    cont = 2
                elif event.key == pygame.K_c:
                    player.set_collect("pebble",10000)
                    player.set_collect("bug",10000)
                    player.set_collect("rock",10000)
                    player.set_collect("freshwater",10000)
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i in range(len(buttons)):
                    if buttons[i].collision():
                        pygame.mixer.Sound.play(sounds[0])
                        if i == 0:
                            extractTime = False
                            cont = 2
                        elif i == 1:
                            extractItem = "pebble"
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
                            extractItem = "bush"
                        elif i == 8:
                            extractItem = "rock"
                        elif i == 9:
                            extractItem = "gem"
                        elif i == 10:
                            extractItem = "volrock"
                        elif i == 11:
                            extractItem = "freshwater"
                        elif i == 12:
                            extractItem = "saltwater"
        if extractItem != 0:
            if player.get_collect()[extractItem] > 0:
                extraction(extractItem)
        qtHandelling()
        pygame.display.update()
        clock.tick(FPS)
    return cont 

def craftMini():
    cont = 0
    craftTime = True
    while craftTime:
        screenDisplay("craft")
        synthesisTime = [False,""]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                craftTime = False
                cont = 1
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    craftTime = False
                    cont = 2
                else:
                    for box in range(len(inputBoxes)):
                        if inputBoxes[box].get_isInput():
                            if event.key == pygame.K_BACKSPACE:
                                inputBoxes[box].decrease_text()
                            elif event.key == pygame.K_RETURN:
                                synthesisTime = checkProduct(inputBoxes[0].get_text())
                            else:
                                inputBoxes[box].increase_text(event.unicode)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if buttons[0].collision():
                    pygame.mixer.Sound.play(sounds[0])
                    craftTime = False
                    cont = 2
                elif buttons[1].collision():
                    pygame.mixer.Sound.play(sounds[0])
                    synthesisTime = checkProduct(inputBoxes[0].get_text())
                elif inputBoxes[0].collision():
                    inputBoxes[0].set_isInput(True)

        if synthesisTime[0] == True:
            synthesis(True,synthesisTime[1])
        while synthesisTime[0] == True:
            synthesis(False,synthesisTime[1])
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    synthesisTime = (False,"")
                    craftTime = False
                    cont = 1
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        synthesisTime = (False,"")
                        craftTime = False
                        cont = 2
                    else:
                        for box in range(len(inputBoxes)):
                            if inputBoxes[box].get_isInput():
                                if event.key == pygame.K_BACKSPACE:
                                    inputBoxes[box].decrease_text()
                                else:
                                    inputBoxes[box].increase_text(event.unicode)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if buttons[0].collision():
                        pygame.mixer.Sound.play(sounds[0])
                        synthesisTime = (False,"")
                        craftTime = False
                        cont = 2
                    elif buttons[1].collision():
                        pygame.mixer.Sound.play(sounds[0])
                        playerInput = []
                        for i in range(len(inputBoxes)):
                            playerInput.append(inputBoxes[i].get_text())
                        check, message = checkEquation(playerInput, synthesisTime[1])
                        if check and message == []:
                            displayResult("SUCCESS",f"you recieve {synthesisTime[1][1]}")
                            for i in range(len(synthesisTime[1][1])):
                                player.inc_chemicals(synthesisTime[1][1][i])
                            pygame.display.update()
                            time.sleep(2)
                        elif message == []:
                            quickTexts.append(ShapeClasses.QuickText([840,240],f"Incorrect",time.time()))
                        else:
                            for i in range(len(message)):
                                quickTexts.append(ShapeClasses.QuickText([840+100*i,240],f"{message[i]}",time.time()))
                    elif buttons[2].collision():
                        pygame.mixer.Sound.play(sounds[0])
                        displayTip(synthesisTime[1][0])

                    else:
                        for j in range(len(inputBoxes)):
                            if inputBoxes[j].collision():
                                for k in range(len(inputBoxes)):
                                    inputBoxes[k].set_isInput(False)
                                inputBoxes[j].set_isInput(True)
            qtHandelling()
            pygame.display.update()
            clock.tick(FPS)
        qtHandelling()
        pygame.display.update()
        clock.tick(FPS)
    return cont 

def inventoryMini():
    cont = 0
    inventoryTime,extractTime,craftTime,achieveTime,addQTime = True,False,False,False,False
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
                        elif i == 3:
                            inventoryTime = False
                            achieveTime = True
                        elif i == 4:
                            cost = 20
                            maxHealth = 5
                            if game.get_diff() == "Easy":
                                cost = 10
                                maxHealth = 8
                            elif game.get_diff() == "Hard":
                                cost = 50
                                maxHealth = 3
                            if player.get_carbonCount() > cost and player.get_health() < maxHealth+1:
                                player.heal_self()
                                quickTexts.append(ShapeClasses.QuickText([830,700],f"You Gained A heart!",time.time()))
                            elif player.get_carbonCount() > cost:
                                quickTexts.append(ShapeClasses.QuickText([830,700],f"You are on max health ({maxHealth})",time.time()))
                            else:
                                quickTexts.append(ShapeClasses.QuickText([800,700],f"You dont have enough carbon (1 heart = {cost}C)",time.time()))
                        elif i == 5:
                            inventoryTime = False
                            addQTime = True


        if extractTime:
            screenSetUp("extract")
            cont = extractMini()
        elif craftTime:
            screenSetUp("craft")
            cont = craftMini()  
        elif achieveTime:
            screenSetUp("achieve")
            cont = achieveMini()  
        elif addQTime:
            screenSetUp("addQuestions")
            cont = addQMini()
     
        qtHandelling()
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
                        if game.get_tutorial():
                            displayResult("Adventure!","Collect resources, battle enemies, talk with guides")
                            pygame.display.update()
                            time.sleep(1)
                        cont = 3
            elif event.key == pygame.K_e:
                inventoryTime  = True
            elif event.key == pygame.K_q:
                pTableTime  = True

    if inventoryTime:
        screenSetUp("inventory")
        cont = inventoryMini()
        while cont == 2:
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

def bossMini():
    cont = 0
    bossTime = True
    while bossTime:
        screenDisplay("boss")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                bossTime = False
                cont = 1
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    bossTime = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if buttons[0].collision():
                    pygame.mixer.Sound.play(sounds[0])
                    bossTime = False
                for i in range(len(buttons)):
                    if i >= len(buttons):
                        break
                    if i != 0:
                        if buttons[i].collision():
                            pygame.mixer.Sound.play(sounds[0])
                            item = buttons[i].get_text()
                            count = player.get_chemicals()[item]
                            if count > 0:
                                buttons.pop(i)
                                player.dec_chemicals(item)
                                quickTexts.append(ShapeClasses.QuickText([840,240],f"Completed",time.time()))
                            else:
                                quickTexts.append(ShapeClasses.QuickText([740,400],f"Do dont have enough {item}",time.time()))
        if len(buttons) == 1:
            displayResult("YOU BEAT THE BOSS",f"you recieve the KEY")
            player.set_hasKey()
        qtHandelling()
        pygame.display.update()
        clock.tick(FPS)
    for s in range(len(sSprites)):
        if sSprites[s].get_type() == "boss":
            sSprites[s].set_specialTime(False)
    return cont 

def gateMini():
    cont = 0
    gateTime = True
    while gateTime:
        screenDisplay("gate")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gateTime = False
                cont = 1
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    gateTime = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if buttons[0].collision():
                    pygame.mixer.Sound.play(sounds[0])
                    gateTime = False
                elif buttons[1].collision():
                    pygame.mixer.Sound.play(sounds[0])
                    print(player.get_hasKey())
                    if player.get_hasKey():
                        pygame.draw.rect(screen,BLACK,[175,175,WIDTH-350, HEIGHT-350])
                        pygame.draw.rect(screen,WHITE,[180,180,WIDTH-360, HEIGHT-360])
                        pygame.draw.rect(screen,BLACK,[200,200,WIDTH-400, HEIGHT-400])
                        displayText("YOU WIN!!!", font100, WHITE, [WIDTH/2, 400])
                        player.win()
                        pygame.display.update()
                        time.sleep(10)
                    else:
                        quickTexts.append(ShapeClasses.QuickText([WIDTH/2+10,HEIGHT/2+60],f"Do do not have the KEY",time.time()))
                        if game.get_tutorial():
                            quickTexts.append(ShapeClasses.QuickText([WIDTH/2+10,HEIGHT/2+60],f"HINT: You must defeat the BOSS",time.time()))
        qtHandelling()
        pygame.display.update()
        clock.tick(FPS)
    for s in range(len(sSprites)):
        if sSprites[s].get_type() == "gate":
            sSprites[s].set_specialTime(False)
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
            elif event.key == pygame.K_l:
                player._pos = [500,500]

    if miniMap:
        screenSetUp("minimap")
        cont = miniMapMini()
    if pTableTime:
        screenSetUp("pTable")
        cont = pTableMini()
    
    for s in range(len(sSprites)):
        if sSprites[s].get_specialTime():
            if sSprites[s].get_type() == "boss":
                screenSetUp("boss")
                cont = bossMini()
            elif sSprites[s].get_type() == "gate":
                screenSetUp("gate")
                cont = gateMini()

    for e in range(len(eSprites)):
        battle = eSprites[e].get_battle()
        if battle:
            screenSetUp("battle")
            eSprites[e].set_qSet(fetchQuestions())
            eSprites[e].set_qNum(0)

            while battle:
                screenDisplay("battle")
                complete = False
                questions = eSprites[e].get_qSet()[eSprites[e].get_qNum()]
                answer = eSprites[e].get_qSet()[eSprites[e].get_qNum()][5]

                displayText(questions[0],font20,WHITE,[960,250])
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
                        for b in range(len(buttons)):
                            if buttons[b].collision():
                                pygame.mixer.Sound.play(sounds[0])
                                if b+1 == answer:
                                    if eSprites[e].get_qNum() == len(eSprites[e].get_qSet())-1:
                                        areaMap.set_collected(eSprites[e].get_num())
                                        eSprites.remove(eSprites[e])
                                        sSprites.clear()
                                        pygame.mixer.music.stop()
                                        if game.get_playMusic():
                                            pygame.mixer.music.load(music[1])
                                            pygame.mixer.music.play(-1)
                                            game.set_music(1)
                                        complete = True
                                    else:
                                        eSprites[e].set_qNum("inc")
                                else:
                                    screen.fill(BURG)
                                    pygame.display.update()
                                    time.sleep(0.4) 
                                    player.decrease_health()
                                    hearts.pop()

                if player.get_health() <= 0:
                    screen.fill(BURG)
                    displayResult("DEATH",f"you recieve nothing")
                    player.revive_self()
                    pygame.display.update()
                    time.sleep(1.5)
                    battle = False
                    if game.get_diff() == "Easy":
                        cont = 3
                    else:
                        cont = 4
                elif complete:
                    screen.fill(GREEN)
                    reward = battleReward()
                    displayResult("WELL DONE",f"you recieve {reward[1]} {reward[0]}")
                    pygame.display.update()
                    time.sleep(1)
                    battle = False
                pygame.display.update()
                clock.tick(FPS)
            break
    
    qtHandelling()
    pygame.display.update()
    clock.tick(FPS)
    return cont





#---------------GLOBAL OBJECTS---------------#
player = SpriteClasses.Player()
game = GameClasses.GameSettings()
areaMap = GameClasses.AreaMap()
mini = ShapeClasses.MiniWindow()
areaMap.reset()
buttons = []
inputBoxes = []
quickTexts = []
cSprites = []
eSprites = []
nSprites = []
sSprites = []
doors = []
hearts = []


#---------------MAIN---------------#
def main():
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
            elif cont == 4:
                running = "menu"

        pygame.display.update()
        clock.tick(FPS)
    pygame.quit()
#---------------MAIN---------------#


if __name__ == "__main__":
    main()