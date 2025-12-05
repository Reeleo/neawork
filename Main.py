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
RED = (255,0,0)
BURG = (100,0,0)
BUTTON2 = (60,180,60)
MINI = (10,50,40)
BLUE = (60,60,225)
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
            # signals the battle to start

# these displays non objects
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

# updates, displays and checks for collisions 
def displayObject(type,obj):
    # moving sprites
    if type == "player" or type == "enemy":
        if game.get_screen() == "home" and type == "player":
            # player will only be able to move left or right 
            screen.blit(obj.update(game.get_screen(),WIDTH,HEIGHT),(obj.get_pos()))
        else:
            if type == "player":
                screen.blit(obj.update(game.get_screen(),WIDTH,HEIGHT),(obj.get_pos()))
            else:
                checkCollision(obj)
                screen.blit(obj.update(player.get_pos()),(obj.get_pos()))
            
            pos = obj.get_pos()
            speed = obj.get_speed()
            obj.set_validWalk("all",[True,True,True,True])
            # valid walk tells the object that it can walk in a certain direction
            # [north (-y), east (+x), south (+y), west(-x)]
            tilePos = areaMap.get_waterPos()
            for i in range(len(tilePos)):
                for j in range(2):
                    if j == 0:
                        # left foot
                        foot = [pos[0]+35,pos[1]+102]
                    else:
                        # right foot
                        foot = [pos[0]+67,pos[1]+102]

                    if tilePos[i][1]*64 < foot[0]-speed < tilePos[i][1]*64+64 or tilePos[i][1]*64 < foot[0]+10-speed < tilePos[i][1]*64+64:
                        if tilePos[i][0]*64 < foot[1] < tilePos[i][0]*64+64 or tilePos[i][0]*64 < foot[1]+10 < tilePos[i][0]*64+64:
                            obj.set_validWalk(3,False)
                    if tilePos[i][1]*64 < foot[0]+speed < tilePos[i][1]*64+64 or tilePos[i][1]*64 < foot[0]+10+speed < tilePos[i][1]*64+64:
                        if tilePos[i][0]*64 < foot[1] < tilePos[i][0]*64+64 or tilePos[i][0]*64 < foot[1]+10 < tilePos[i][0]*64+64:
                            obj.set_validWalk(1,False)
                    if tilePos[i][1]*64 < foot[0] < tilePos[i][1]*64+64 or tilePos[i][1]*64 < foot[0] < tilePos[i][1]*64+64:
                        if tilePos[i][0]*64 < foot[1]+speed < tilePos[i][0]*64+64 or tilePos[i][0]*64 < foot[1]+10+speed < tilePos[i][0]*64+64:
                            obj.set_validWalk(2,False)
                    if tilePos[i][1]*64 < foot[0] < tilePos[i][1]*64+64 or tilePos[i][1]*64 < foot[0] < tilePos[i][1]*64+64:
                        if tilePos[i][0]*64 < foot[1]-speed < tilePos[i][0]*64+64 or tilePos[i][0]*64 < foot[1]+10-speed < tilePos[i][0]*64+64:
                            obj.set_validWalk(0,False)
            if type == "player":
                nextToWater = False
                drct = player.get_validWalk()
                for i in range(len(drct)):
                    if drct[i] == False:
                        nextToWater = True
                    break
                if nextToWater:
                    player.set_canGetWater(True)
                else:
                    player.set_canGetWater(False)

    # interactable sprites
    elif type == "collect" or type == "door" or type == "char" or type == "special":
        if type == "char" or type == "special":
            screen.blit(obj.update(),(obj.get_pos()))
        else:
            screen.blit(obj.update(game.get_screen()),(obj.get_pos()))

        if obj.collision(player.get_pos()):
            playerpos, playersize = player.get_pos(), player.get_size()
            if game.get_tutorial():
                displayText("SPACE", font20, WHITE, [playerpos[0]+playersize[0]/2, playerpos[1]-20])
            
            keys = pygame.key.get_pressed()
            if type == "collect":
                # doors will just be displayed but items can be collected
                if keys[pygame.K_SPACE]:
                    obj.set_visible(False)
                    player.inc_collect(obj._type[0])
                    areaMap.set_collected(obj.get_num())
                    # setting visible to false stops the object being displayed each tick
                    # removes it from the item stores for the map

            elif type == "char":
                if keys[pygame.K_SPACE] and obj.get_timer(time.time()) > 1.5:
                    quickTexts.append(ShapeClasses.QuickText([playerpos[0]+playersize[0]/2, playerpos[1]-20-50],obj.get_dialogue(),time.time()))
                    obj.set_timer(time.time())
                    # timer is set so the character can continue to talk after some seconds

            elif type == "special":      
                if keys[pygame.K_SPACE]:
                    obj.set_activated(True)
                # special sprites e.g. the boss will display a special screen when interacted with

    elif type == "button":
        pos = obj.get_pos()
        size = obj.get_size()
        text = obj.get_text()
        colours = obj.get_colours()
        if not obj.collision():
            pygame.draw.rect(screen,colours[0],[pos[0]-5, pos[1]-5, size[0]+10, size[1]+10])
        pygame.draw.rect(screen,colours[1],[pos[0], pos[1], size[0], size[1]])
        displayText(text, font20, BLACK, [pos[0]+size[0]/2, pos[1]+size[1]/2])
        # changes the colour of the button when the mouse hovers over it

    elif type == "mini":
        pos = obj.get_pos()
        size = obj.get_size()
        text = obj.get_text()
        colours = obj.get_colours()
        pygame.draw.rect(screen, colours[0], [pos[0]-10, pos[1]-10, size[0]+20, size[1]+20])
        pygame.draw.rect(screen, colours[1], [pos[0], pos[1], size[0], size[1]])
        # draws the borders and background for a mini screen

    elif type == "tile":
        screen.blit(obj[0],(obj[1]))
        
    elif type == "heart":
        screen.blit(obj.generateImage(0,3,32,32),(obj.get_pos()))

# for displaying messages 
def displayResult(t1,t2):
    pygame.draw.rect(screen,BLACK,[175,175,WIDTH-350, HEIGHT-350])
    pygame.draw.rect(screen,WHITE,[180,180,WIDTH-360, HEIGHT-360])
    pygame.draw.rect(screen,BLACK,[200,200,WIDTH-400, HEIGHT-400])
    displayText(t1, font100, WHITE, [WIDTH/2, 400])
    displayText(t2, font20, WHITE, [WIDTH/2, 550])

def qtHandelling():
    deleteing = 0
    for i in range(len(quickTexts)):
        if quickTexts[i].get_visible():
            displayText(quickTexts[i].get_text(),font20,quickTexts[i].get_colours(),[quickTexts[i].get_pos()[0],quickTexts[i].get_pos()[1]+i*30])
            if quickTexts[i].update(time.time()):
                # returns True if the current time - its start time is longer than the duration
                deleteing += 1
    for _ in range(deleteing):
        quickTexts.pop(0)


#---------------SETUP/DISPLAY---------------#
def screenSetUp(screenType):
    buttons.clear()

    #1 main menu screen
    if screenType == "menu":
        if game.get_music() == -1 and game.get_playMusic():
            pygame.mixer.music.load(music[0])
            pygame.mixer.music.play(-1)
            game.set_music(0)
        buttons.append(ShapeClasses.Button([WIDTH/4-90,3*HEIGHT/4],[180,80],"EXIT",RED))
        buttons.append(ShapeClasses.Button([3*WIDTH/4-90, 3*HEIGHT/4],[180,80],"START",RED))
        buttons.append(ShapeClasses.Button([WIDTH/2-90, HEIGHT/2],[180,80],"HOW TO PLAY",RED))

    #2 how to play screen
    if screenType == "htp":
        inputBoxes.clear()
        inputBoxes.append(ShapeClasses.InputBox([180,680],[450,80],"",RED))
        buttons.append(ShapeClasses.Button([WIDTH-300, 200],[180,80],"MENU",RED))

    #3 save file screen
    if screenType == "savefiles":
        buttons.append(ShapeClasses.Button([400,100],[1000,150],"Save1",RED))
        buttons.append(ShapeClasses.Button([400,300],[1000,150],"Save2",RED))
        buttons.append(ShapeClasses.Button([400,500],[1000,150],"Save3",RED))
        buttons.append(ShapeClasses.Button([WIDTH/4-200, 3*HEIGHT/4],[180,80],"MENU",RED))

    #4 home screen
    if screenType == "home":
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

    #5 iventory screen
    if screenType == "inventory":
        cSprites.clear()
        buttons.append(ShapeClasses.Button([1150,750],[180,80],"RETURN",BUTTON2))
        for j in range(12):
            cSprites.append(SpriteClasses.Collectable([120, 100+j*60],j))
        for k in range(12):
            cSprites[k].assign_type(game.get_collectTypes())
        if game.get_screen() == "home":
            buttons.append(ShapeClasses.Button([390,360],[400,80],"EXTRACT",BUTTON2))
            buttons.append(ShapeClasses.Button([850,360],[400,80],"CRAFT",BUTTON2))
            buttons.append(ShapeClasses.Button([390,480],[400,80],"ACHIEVEMENTS",BUTTON2))
            buttons.append(ShapeClasses.Button([850,480],[400,80],"HEAL",BUTTON2))
            buttons.append(ShapeClasses.Button([610,600],[400,80],"ADD QUESTIONS",BUTTON2))
        mini.set_size([WIDTH-200, HEIGHT-200])
        mini.set_pos([100, 100])
        
    #6 extraction screen
    if screenType == "extract":
        cSprites.clear()
        buttons.append(ShapeClasses.Button([1150,750],[180,80],"RETURN",BUTTON2))
        for i in range(12):
            buttons.append(ShapeClasses.Button([140+(i)*100, 200],[80,80],i,BUTTON2))
        for j in range(12):
            cSprites.append(SpriteClasses.Collectable([140+j*100, 200],j))
        for k in range(12):
            cSprites[k].assign_type(game.get_collectTypes())
        mini.set_size([WIDTH-200, HEIGHT-200])
        mini.set_pos([100, 100])

    #7 crfating selection screen
    if screenType == "craft":
        cSprites.clear()
        inputBoxes.clear()
        buttons.append(ShapeClasses.Button([1150,750],[180,80],"RETURN",BUTTON2))
        buttons.append(ShapeClasses.Button([660,200],[80,80],"GO",BUTTON2))
        inputBoxes.append(ShapeClasses.InputBox([320,200],[320,80],"",BUTTON2))

        mini.set_size([WIDTH-200, HEIGHT-200])
        mini.set_pos([100, 100])

    #8 periodic table screen
    if screenType == "pTable":
        buttons.append(ShapeClasses.Button([1240,610],[90,180],"RETURN",RED))
        mini.set_size([WIDTH-200, HEIGHT-255])
        mini.set_pos([100, 130])

    #9 achievements screen
    if screenType == "achieve":
        buttons.append(ShapeClasses.Button([1150,750],[180,80],"RETURN",BUTTON2))
        buttons.append(ShapeClasses.Button([140, 200],[280,80],"Beat the BOSS",BUTTON2))
        buttons.append(ShapeClasses.Button([460, 200],[280,80],"ESCAPE through the GATE",BUTTON2))
        mini.set_size([WIDTH-200, HEIGHT-200])
        mini.set_pos([100, 100])

    #10 question management screen
    if screenType == "addQuestions":
        inputBoxes.clear()
        buttons.append(ShapeClasses.Button([1150,750],[180,80],"RETURN",BUTTON2))
        buttons.append(ShapeClasses.Button([1260, 500],[80,80],"ADD",BUTTON2))
        buttons.append(ShapeClasses.Button([1260,300],[80,80],"1",BUTTON2))
        buttons.append(ShapeClasses.Button([1260, 400],[80,80],game.get_diff(),BUTTON2))
        buttons.append(ShapeClasses.Button([140,750],[180,80],"RESET",BUTTON2))
        inputBoxes.append(ShapeClasses.InputBox([150,350],[1060,80],"",BUTTON2))
        inputBoxes.append(ShapeClasses.InputBox([150,500],[250,80],"",BUTTON2))
        inputBoxes.append(ShapeClasses.InputBox([420,500],[250,80],"",BUTTON2))
        inputBoxes.append(ShapeClasses.InputBox([690,500],[250,80],"",BUTTON2))
        inputBoxes.append(ShapeClasses.InputBox([960,500],[250,80],"",BUTTON2))
        mini.set_size([WIDTH-200, HEIGHT-200])
        mini.set_pos([100, 100])

    #11 pause screen
    if screenType == "pause":
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

    #12 adventure screen
    if screenType == "maps":
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
        # blit list contains all objects on that need to be displayed on the screen
        # in order to be displayed they must be added to an object list
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
            
    #13 minimap screen
    if screenType == "minimap":
        mini.set_pos([100,100])
        mini.set_size([WIDTH-200, HEIGHT-192])
        buttons.append(ShapeClasses.Button([1187,783],[180,80],"RETURN",RED))

    #14 battle screen
    if screenType == "battle":
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
        sSprites.append(SpriteClasses.EnemyImage([30,180],))
        mini.set_size([WIDTH-200, HEIGHT-200])
        mini.set_pos([100, 100])
        for i in range(player.get_health()):
            hearts.append(SpriteClasses.Sprite([10+i*60, 20],[50,50],2.5,BLACK,pygame.image.load("collectablesSprites.bmp")))  

    #15 boss quest screen
    if screenType == "boss":
        quest = ["ester","nitrile","carbon","alcohol","amide"]
        buttons.append(ShapeClasses.Button([1150,750],[180,80],"RETURN",BUTTON2))
        buttons.append(ShapeClasses.Button([350,350],[200,80],quest[0],BUTTON2))
        buttons.append(ShapeClasses.Button([650,250],[200,80],quest[1],BUTTON2))
        buttons.append(ShapeClasses.Button([950,350],[200,80],quest[2],BUTTON2))
        buttons.append(ShapeClasses.Button([500,600],[200,80],quest[3],BUTTON2))
        buttons.append(ShapeClasses.Button([800,600],[200,80],quest[4],BUTTON2))
        mini.set_size([WIDTH-200, HEIGHT-200])
        mini.set_pos([100, 100])
    
    #16 gate screen
    if screenType == "gate":
        buttons.append(ShapeClasses.Button([1150,750],[180,80],"RETURN",BUTTON2))
        buttons.append(ShapeClasses.Button([WIDTH/2-50,HEIGHT/2-40],[100,80],"Give KEY",BUTTON2))
        mini.set_size([WIDTH-200, HEIGHT-200])
        mini.set_pos([100, 100])


def screenDisplay(screenType):
    #1 main menu screen
    if screenType == "menu":
        screen.fill(BURG)
        pygame.draw.rect(screen,RED,[20,20,WIDTH-40, HEIGHT-40])
        pygame.draw.rect(screen,BLACK,[40,40,WIDTH-80, HEIGHT-80])
        displayText("ChemCraft", font100, WHITE, [WIDTH/2, 200])
        for i in range(len(buttons)):
            displayObject("button",buttons[i])

    #2 how to play screen
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

    #3 save file screen
    if screenType == "savefiles":
        screen.fill(BURG)
        pygame.draw.rect(screen,RED,[20,20,WIDTH-40, HEIGHT-40])
        pygame.draw.rect(screen,BLACK,[40,40,WIDTH-80, HEIGHT-80])
        for i in range(len(buttons)):
            displayObject("button",buttons[i])

    #4 home screen
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
            displayText("press 'm' for minimap",font20,WHITE,[1300,65])
            displayText("press 'space' to interact",font20,WHITE,[132,590])
            displayText("press 'esc' to go back",font20,WHITE,[165,65])
        displayObject("door", doors[0])
        displayObject("door", doors[1])
        displayObject("player", player)
    
    #5 inventory screen
    if screenType == "inventory":
        pygame.draw.rect(screen,WHITE,(100,HEIGHT/2-75,WIDTH-200,10))
        displayObject("mini",mini)
        displayText("Your Collection:", font20, WHITE, [290, 140])
        for i in range(len(buttons)):
            displayObject("button",buttons[i])
        for j in range(len(cSprites)):
            displayObject("collect",cSprites[j])

        x, y = 530, 240
        xcount, ycount = 0, 0
        collection = player.get_collect()
        # displays the players item collection
        for item in collection:
            itemname = item
            if itemname == "wplant":
                itemname = "waterplant"
            elif itemname == "volrock":
                itemname = "volcanicrock"
            displayText(f"{itemname}: {collection[item]}", font20, WHITE, [x+xcount, y+ycount])
            xcount += 200
            if xcount == 800:
                xcount = 0 
                ycount += 40
  
    #6 extraction screen
    if screenType == "extract":
        pygame.draw.rect(screen,WHITE,(100,HEIGHT/2-75,WIDTH-200,10))
        displayObject("mini",mini)
        displayText("Your Collection:", font20, WHITE, [212, 150])
        for i in range(len(buttons)):
            displayObject("button",buttons[i])
        for j in range(len(cSprites)):
            displayObject("collect",cSprites[j])

        x, y = 200, 310
        xcount, ycount = 0, 0
        collection = player.get_collect()
        for item in collection:
            itemname = item
            if itemname == "wplant":
                itemname = "waterplant"
            elif itemname == "volrock":
                itemname = "volcanicrock"
            displayText(f"{itemname}: {collection[item]}", font20, WHITE, [x+xcount, y+ycount])
            xcount += 200
            if xcount >= 1010:
                xcount = 0 
                ycount += 30

    #7 crfating selection screen
    if screenType == "craft":
        pygame.draw.rect(screen,WHITE,(100,HEIGHT/2-75,WIDTH-200,10))
        displayObject("mini",mini)
        displayText("CRAFTING:", font20, WHITE, [212, 150])
        displayText("Synthesis of:", font20, WHITE, [222, 235])
        displayText("please use lowercase and no spaces", font20, WHITE, [642, 300])
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

    #8 periodic table screen
    if screenType == "pTable":
        pygame.draw.rect(screen,WHITE,(100,HEIGHT/2-75,WIDTH-200,10))
        displayObject("mini",mini)
        displayObject("button",buttons[0])
        displayImage(pygame.image.load("pTable.png"),[110,140],0.9,[WIDTH-250,HEIGHT-200])
    
    #9 achievements screen
    if screenType == "achieve":
        pygame.draw.rect(screen,WHITE,(100,HEIGHT/2-75,WIDTH-200,10))
        displayObject("mini",mini)
        displayText("Your Achievements:", font20, WHITE, [231, 150])
        for i in range(len(buttons)):
            displayObject("button",buttons[i])
        playerAchieve = player.get_achievements()
        for j in range(len(playerAchieve)):
            displayText(f"Achieved = {playerAchieve[j]}", font20, WHITE, [280+j*320, 310])

    #10 question management screen
    if screenType == "addQuestions":
        pygame.draw.rect(screen,WHITE,(100,HEIGHT/2-75,WIDTH-200,10))
        displayObject("mini",mini)
        displayText("Adding Questions:", font20, WHITE, [210, 140])
        displayText("The Question:", font20, WHITE, [213,330])
        displayText("The Answers:", font20, WHITE, [213,480])
        displayText("1", font20, WHITE, [270,610])
        displayText("2", font20, WHITE, [540,610])
        displayText("3", font20, WHITE, [810,610])
        displayText("4", font20, WHITE, [1090,610])
        for i in range(len(buttons)):
            displayObject("button",buttons[i])
        for j in range(len(inputBoxes)):
            displayObject("button",inputBoxes[j])
        
    #11 pause screen
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

    #12 adventure screen
    if screenType == "maps":
        # all the tiles and objects needing to be displayed
        tiles, blitList, setPlayer = areaMap.loadMap(player.get_pos(),player.get_size(),WIDTH,HEIGHT)
        player.set_pos(setPlayer,WIDTH,HEIGHT)
        # if the player passes into another screen setPlayer == 0(north), 1(east), 2(south), 3(west)
        # if setPlayer == -1 it means the screen will remain the same 
        if setPlayer != -1:
            # setting up an adventure screen area
            cSprites.clear()
            eSprites.clear()
            nSprites.clear()
            sSprites.clear()
            # if the area is a boss or gate area then it will be the only object displayed
            if blitList == "BOSS":
                sSprites.append(SpriteClasses.EnemyImage([WIDTH/2-250,HEIGHT/2-350],))
            elif blitList == "GATE":
                sSprites.append(SpriteClasses.Gate([WIDTH-200,HEIGHT/2],))
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

        # each tile and object now displayed
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
     
    #13 minimap screen
    if screenType == "minimap":
        displayObject("mini",mini)
        displayObject("button",buttons[0])
        tiles = areaMap.drawMiniMap(WIDTH,HEIGHT,game.get_showAll())
        for i in range(len(tiles)):
            for j in range(len(tiles[i])):
                displayObject("tile",tiles[i][j])
        pygame.draw.rect(screen,BLUE,[(areaMap.get_pos()[1]-1)*147+160,(areaMap.get_pos()[0]-1)*96+135,20,20])
        displayText(f"PlayerCol = {areaMap.get_pos()[1]}",font20,WHITE,[1270,130])
        displayText(f"PlayerRow = {areaMap.get_pos()[0]}",font20,WHITE,[1270,160])

    #14 battle screen
    if screenType == "battle":
        screen.fill(BLACK)
        displayObject("mini",mini)
        displayObject("special",sSprites[0])
        displayText("BATTLE:",font100,WHITE,[320, 180])
        
        for i in range(len(buttons)):
            displayObject("button",buttons[i])
        for j in range(len(hearts)):
            displayObject("heart",hearts[j])

    #15 boss screen
    if screenType == "boss":
        pygame.draw.rect(screen,WHITE,(100,HEIGHT/2-75,WIDTH-200,10))
        displayObject("mini",mini)
        displayText("BOSS:", font100, WHITE, [255, 150])
        for i in range(len(buttons)):
            displayObject("button",buttons[i])
    
    #16 gate screen
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
            # item collection
            for item in player.get_collect():
                player.set_collect(item,int(saveData[count])) 
                count += 1
        elif i == 1:
            # chemical collection
            for item in player.get_chemicals():
                player.set_chemicals(item, int(saveData[count]))
                count += 1
        elif i == 2:
            # settings and achivements 
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
            # any questions the player added
            if line == "":
                cont = False 
            else:
                questions.append(line)
        i += 1
    resetQuestions()
    # resets the questions to the original set questions
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
    # copies any new questions the player added 
    qFile = open("questions.txt","r")
    for _ in range(40):
        ogQuestions.append(qFile.readline())
    while cont:
        qData.append(qFile.readline())
        for j in range(len(qData)):
            if qData[j] == "!":
                cont = False
    for k in range(len(qData)):
        if qData[k] != "!":
            questionLine += qData[k] 
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
# extraction
def extraction(item):
    chances = game.get_itemChances()[item]
    randomNum = random.randint(0,len(chances)-1)
    chem = chances[randomNum][0]
    amount = chances[randomNum][1]
    player.set_extracted(item,chem,amount)
    chems = player.get_chemicals()
    quickTexts.append(ShapeClasses.QuickText([WIDTH/2,450],f"Extraction of: {item} - You recieve {chem} - {chem} count = {chems[chem]}",time.time()))
    return chem

# crafting functions  
def synthesis(setUp,items):
    if setUp:
        buttons.clear()
        inputBoxes.clear()
        buttons.append(ShapeClasses.Button([1150,750],[180,80],"RETURN",BUTTON2))
        buttons.append(ShapeClasses.Button([1230,650],[100,80],"CHECK",BUTTON2))
        buttons.append(ShapeClasses.Button([1230,250],[100,80],"HINT",BUTTON2))
        # items contains the reactants, prodcuts and conditions
        for i in range(len(items)):
            try:
                items[i] = items[i].split(".") 
                # splits up the different reactants/procuts/conditions
                # items = [[reactants list],[products list],[conditions list]]
            except:
                pass
        
        # adds input boxes depending on how many substances each item list contains
        for j in range(len(items)):
            if j != 0:
                for k in range(len(items[j])):
                    if j == 1 and k == 0:
                        inputBoxes.append(ShapeClasses.InputBox([290,400],[260,80],"",BUTTON2))
                    elif j == 1 and k == 1:
                        inputBoxes.pop(-1)
                        inputBoxes.append(ShapeClasses.InputBox([130,400],[260,80],"",BUTTON2))
                        inputBoxes.append(ShapeClasses.InputBox([430,400],[260,80],"",BUTTON2))

                    elif j == 2 and k == 0:
                        inputBoxes.append(ShapeClasses.InputBox([950,400],[260,80],"",BUTTON2))
                    elif j == 2 and k == 1:
                        inputBoxes.pop(-1)
                        inputBoxes.append(ShapeClasses.InputBox([790,400],[260,80],"",BUTTON2))
                        inputBoxes.append(ShapeClasses.InputBox([1090,400],[260,80],"",BUTTON2))

                    elif j == 3 and k == 0:
                        inputBoxes.append(ShapeClasses.InputBox([610,520],[260,80],"",BUTTON2))
                    elif j == 3 and k == 1:
                        inputBoxes.pop(-1)
                        inputBoxes.append(ShapeClasses.InputBox([450,520],[260,80],"",BUTTON2))
                        inputBoxes.append(ShapeClasses.InputBox([750,520],[260,80],"",BUTTON2))  
            
    else:
        # displays all the information text and updates objects
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
    # checks if the product chosen is valid (exists in the synthesis file) by linear search
    valid = False
    product = ""
    file = open("synthesisFile.txt","r")
    line = file.readline()
    data = line.split(",")
    for i in range(len(data)):
        # splits the data into each synthetic route 
        data[i] = data[i].split("/")
    for j in range(len(data)):
        # the first item in the synthetic route is what is being searched for
        if data[j][0] == txt:
            valid = True  
            product = data[j]
            break  
    if not valid:
        quickTexts.append(ShapeClasses.QuickText([800,240],f"INVALID",time.time()))
    file.close()
    return valid, product

def checkEquation(txt,check):
    # txt is what the player has inputed into input boxes
    # check is the correct synthetic route 
    # e.g. [['alcohol'], ['haloalkane', 'water'], ['alcohol', 'halogensalt'], ['heat']]
    for i in range(len(check)):
        # error handling to make sure the synthetic route items are separated
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
        # removes the first item in check as it is only used for searching

    validNum = 0
    reactants = []
    products = []
    others = []
    # separates check into reactants, products and conditions
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
    # separates the player input into reactant, products and conditions
    for k in range(len(reactants)):
        inputR.append(txt[k])
    for k in range(len(products)):
        inputP.append(txt[k+len(reactants)])
    for k in range(len(others)):
        inputO.append(txt[k+len(reactants)+len(products)])
    txt = [inputR,inputP,inputO]
    
    # each for loop checks if the check and player text match
    # this can be in any order and is measured by validNum 
    for r in range(len(reactants)):
        for t in range(len(txt[0])):
            if txt[0][t] == reactants[r]:
                validNum += 1
                txt[0][t] = ""
    
    for p in range(len(products)):
        for t in range(len(txt[1])):
            if txt[1][t] == products[p]:
                validNum += 1
                txt[1][t] = ""
    
    for o in range(len(others)):
        for t in range(len(txt[2])):
            if txt[2][t] == others[o]:
                validNum += 1
                txt[2][t] = ""
    
    length = 0
    for i in range(len(check)):
        for j in range(len(check[i])):
            length += 1

    # if the player has inputed the correct components length of check = validNum
    message = []
    if length == validNum:
        removeList = []
        chems = player.get_chemicals()
        # now checks if the player has the right amount of each substance
        for i in range(len(check[0])):
            if chems[check[0][i]] > 0:
                removeList.append([check[0][i],chems[check[0][i]]-1])
            else:
                message.append(f"you dont have {check[0][i]}")
                
        for j in range(len(check[2])):
            # most conditions don't require chemical collection such as heat or reflux
            # sufuricacid and nickel are both catalysts and the player is required to collect them
            if check[2][j] == "sufuricacid" or check[2][j] == "nickel":
                if chems[check[2][j]] > 0:
                    removeList.append([check[0][i],chems[check[0][i]]-1])
                else:
                    message.append(f"you dont have {check[2][j]}")

        if message == []:
            # if the player has enough chemicals then one of each used is removed
            for k in range(len(removeList)):
                player.set_chemicals(removeList[k][0],removeList[k][1])

    if validNum == length and message == []:
        return True, message
    return False, message

def displayTip(item):
    # find the tip by searching the tip file for the item
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
            break
    if index == -1:
        tip = "no tip"
    else:
        tip = lines[index][1]
    quickTexts.append(ShapeClasses.QuickText([1050,200],tip,time.time()))


def resetQuestions():
    data = []
    # rewrites the original questions
    file = open("questions.txt","r")
    for _ in range(40):
        data.append(file.readline())
    file.close()
    file = open("questions.txt","w")
    for i in range(len(data)):
        file.writelines(data[i])
    file.writelines("!")
    # ! is used to signal other functions to stop reading
    file.close()
    
def addingQuestion(data):
    cont = True
    filedata = []
    # rewrites the original questions with the new question at the end
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
    # ! added after new questions added
    file = open("questions.txt","w")
    for i in range(len(filedata)):
        file.writelines(filedata[i])
    file.close()


def fetchQuestions():
    chosenThree = []
    chosenQuestion = []
    qSet = []
    diff = game.get_diff()
    cont = True
    diff = "Testing"
    lines = []
    file = open("questions.txt","r")
    while cont:
        line = file.readline()
        qSet.append(line.split(","))
        lines.append(line)
        for i in range(len(lines)):
            if lines[i] == "!":
                cont = False
            # ! is at the end of the question file and signals for the function to stop reading
    for i in range(len(lines)-1):
        qSet[i][5] = int(qSet[i][5])
    file.close()

    # randomly selects 3 valid questions
    # valid if of the chosen difficulty and if unique to the other questions
    for _ in range(3):
        count = 0
        valid = False
        while not valid:
            repeat = False
            newChosen = random.randint(0,len(qSet)-2)
            for j in range(len(chosenThree)):
                if chosenThree[j] == newChosen:
                    repeat = True
                    # if a repeated question then regenerate a random number
            if not repeat and qSet[newChosen][6] == diff:
                valid  = True
            count += 1
            if count > 50:
                diff = "Testing"
        chosenThree.append(newChosen)
    chosenQuestion = [qSet[chosenThree[0]],qSet[chosenThree[1]],qSet[chosenThree[2]]]
    return chosenQuestion

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
                    if inputBoxes[box].get_takesInput():
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
                if inputBoxes[0].get_takesInput():
                    inputBoxes[0].set_takesInput(False)
                else:
                    inputBoxes[0].set_takesInput(True)

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
                        if inputBoxes[box].get_takesInput():
                            if event.key == pygame.K_BACKSPACE:
                                inputBoxes[box].decrease_text()
                            else:
                                inputBoxes[box].increase_text(event.unicode)
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i in range(len(buttons)):
                    if buttons[i].collision():
                        pygame.mixer.Sound.play(sounds[0])
                        if i == 0:
                            # return button
                            addQTime = False
                            cont = 2
                        elif i == 1:
                            # add button 
                            # only valid if all the input boxes have an input
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
                                # adds the question and displays a success message
                                addingQuestion(questionData)
                                displayResult("Success","your question has been added")
                                pygame.display.update()
                                time.sleep(1)
                            else:
                                quickTexts.append(ShapeClasses.QuickText([WIDTH/2,650],f"Invalid input",time.time()))  
                        elif i == 2:
                            # answer number button
                            num = buttons[i].get_text()
                            num = int(num) + 1
                            if num > 4:
                                num = 1
                            buttons[i].set_text(str(num))
                        elif i == 3:
                            # difficulty selection button
                            diff = buttons[i].get_text()
                            if diff == "Easy":
                                diff = "Medium"
                            elif diff == "Medium":
                                diff = "Hard"
                            else:
                                diff = "Easy"
                            buttons[i].set_text(str(diff))
                        elif i == 4:
                            # reset questions button
                            resetQuestions()
                            displayResult("Done","the questions have been reset")
                            pygame.display.update()
                            time.sleep(1)
                    # if input boxes are clicked, they are activated and all other boxes are deactivated
                    # any text the player inputs will only effect the activated input box
                    for k in range(len(inputBoxes)):
                        if inputBoxes[k].collision():
                            for box in range(len(inputBoxes)):
                                inputBoxes[box].set_takesInput(False)
                            inputBoxes[k].set_takesInput(True)
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
                        extractItems = ["","pebble","bug","flower",
                                        "leaf","fruit","wplant",
                                        "bush","rock","gem","volrock",
                                        "freshwater","saltwater"]
                        pygame.mixer.Sound.play(sounds[0])
                        if i == 0:
                            extractTime = False
                            cont = 2
                        else:
                            extractItem = extractItems[i]
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
                        if inputBoxes[box].get_takesInput():
                            if event.key == pygame.K_BACKSPACE:
                                inputBoxes[box].decrease_text()
                            elif event.key == pygame.K_RETURN:
                                synthesisTime = checkProduct(inputBoxes[0].get_text())
                            else:
                                inputBoxes[box].increase_text(event.unicode)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if buttons[0].collision():
                    # return button
                    pygame.mixer.Sound.play(sounds[0])
                    craftTime = False
                    cont = 2
                elif buttons[1].collision():
                    # check product button
                    pygame.mixer.Sound.play(sounds[0])
                    synthesisTime = checkProduct(inputBoxes[0].get_text())
                elif inputBoxes[0].collision():
                    inputBoxes[0].set_takesInput(True)

        # if a product has been selected then synthesis begins
        # this is where the player will input the correct synthetic route
        if synthesisTime[0] == True:
            # sets up the new screen
            synthesis(True,synthesisTime[1])
        while synthesisTime[0] == True:
            # displays the synthesis screen
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
                            if inputBoxes[box].get_takesInput():
                                if event.key == pygame.K_BACKSPACE:
                                    inputBoxes[box].decrease_text()
                                else:
                                    inputBoxes[box].increase_text(event.unicode)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if buttons[0].collision():
                        # return button
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
                        # check (a boolean) is whether the equation is valid
                        # message will contain any chemicals the player lacks
                        if check and message == []:
                            displayResult("SUCCESS",f"you recieve {synthesisTime[1][1]}")
                            for i in range(len(synthesisTime[1][1])):
                                player.inc_chemicals(synthesisTime[1][1][i])
                            pygame.display.update()
                            time.sleep(2)
                        elif message == []:
                            # the equation is incorrect
                            quickTexts.append(ShapeClasses.QuickText([840,240],f"Incorrect",time.time()))
                        else:
                            # the player lacks chemicals so the message is displayed to the player
                            for i in range(len(message)):
                                quickTexts.append(ShapeClasses.QuickText([840+100*i,240],f"{message[i]}",time.time()))
                    elif buttons[2].collision():
                        # tip button
                        pygame.mixer.Sound.play(sounds[0])
                        displayTip(synthesisTime[1][0])

                    else:
                        # input boxes activation/deactivation
                        for j in range(len(inputBoxes)):
                            if inputBoxes[j].collision():
                                for k in range(len(inputBoxes)):
                                    inputBoxes[k].set_takesInput(False)
                                inputBoxes[j].set_takesInput(True)
            qtHandelling()
            pygame.display.update()
            clock.tick(FPS)
        qtHandelling()
        pygame.display.update()
        clock.tick(FPS)
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
            if event.type == pygame.MOUSEBUTTONDOWN:
                if buttons[0].collision():
                    pygame.mixer.Sound.play(sounds[0])
                    pTableTime = False
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
                            # return button
                            inventoryTime = False
                            for i in range(12):
                                cSprites.pop(-1)
                        elif i == 1:
                            # extraction screen button
                            inventoryTime = False
                            extractTime = True
                        elif i == 2:
                            # crafting screen button
                            inventoryTime = False
                            craftTime = True
                        elif i == 3:
                            # achievement screen button
                            inventoryTime = False
                            achieveTime = True
                        elif i == 4:
                            # healing button
                            # the max health and cost of a heart depends on the chosen difficulty
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
                            # adding questions screen button
                            inventoryTime = False
                            addQTime = True

        # handles the transfer between inventory screen and these screens
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
                for i in range(len(buttons)):
                    if i >= len(buttons):
                        break
                    if i == 0:
                        # return button
                        if buttons[i].collision():
                            pygame.mixer.Sound.play(sounds[0])
                            bossTime = False
                    else:
                        if buttons[i].collision():
                            # quest completion buttons
                            pygame.mixer.Sound.play(sounds[0])
                            item = buttons[i].get_text()
                            count = player.get_chemicals()[item]
                            if count > 0:
                                buttons.pop(i)
                                player.dec_chemicals(item)
                                quickTexts.append(ShapeClasses.QuickText([840,240],f"Completed",time.time()))
                            else:
                                quickTexts.append(ShapeClasses.QuickText([740,400],f"You dont have enough {item}",time.time()))
        if len(buttons) == 1:
            # the player can use the key to open the gate for the achievement 
            displayResult("YOU BEAT THE BOSS",f"you recieve the KEY")
            player.set_hasKey()
            pygame.display.update()
            time.sleep(1)
        qtHandelling()
        pygame.display.update()
        clock.tick(FPS)
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
                    # return button
                    pygame.mixer.Sound.play(sounds[0])
                    gateTime = False
                elif buttons[1].collision():
                    # player wins if they click this and have the key
                    pygame.mixer.Sound.play(sounds[0])
                    if player.get_hasKey():
                        displayResult("YOU WIN!","")
                        pygame.display.update()
                        time.sleep(2)
                    else:
                        quickTexts.append(ShapeClasses.QuickText([WIDTH/2+10,HEIGHT/2+60],f"Do do not have the KEY",time.time()))
                        if game.get_tutorial():
                            quickTexts.append(ShapeClasses.QuickText([WIDTH/2+10,HEIGHT/2+60],f"HINT: You must defeat the BOSS",time.time()))
        qtHandelling()
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
        if event.type == pygame.MOUSEBUTTONDOWN:
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
            elif event.key == pygame.K_SPACE:
                if player.get_canGetWater():
                    # if player is positioned next to water they can collect it 
                    pos = player.get_pos()
                    quickTexts.append(ShapeClasses.QuickText([pos[0]+54,pos[1]-25],f"collect water",time.time()))
                    waterType = random.randint(0,2)
                    if waterType == 0 :
                        player.inc_collect("freshwater")
                    elif waterType == 1:
                        player.inc_collect("saltwater")

    # screen transitions
    if miniMap:
        screenSetUp("minimap")
        cont = miniMapMini()
    if pTableTime:
        screenSetUp("pTable")
        cont = pTableMini()
    
    for s in range(len(sSprites)):
        try:
            if sSprites[s].get_activated():
                if sSprites[s].get_type() == "enemyImage":
                    screenSetUp("enemyImage")
                    cont = bossMini()
                    sSprites[s].set_activated(False)
                elif sSprites[s].get_type() == "gate":
                    screenSetUp("gate")
                    cont = gateMini()
                    sSprites[s].set_activated(False)
        except:
            break

    # battles
    for e in range(len(eSprites)):
        battle = eSprites[e].get_battle()
        if battle:
            # prepares the battle buttons and quetsions
            screenSetUp("battle")
            eSprites[e].set_qSet(fetchQuestions())
            eSprites[e].set_qNum(0)

            while battle:
                screenDisplay("battle")
                pTableTime = False
                complete = False
                # qNum points to which question is currently being asked in the enemies question set
                question = eSprites[e].get_qSet()[eSprites[e].get_qNum()]
                answerNum = eSprites[e].get_qSet()[eSprites[e].get_qNum()][5]

                displayText(question[0],font20,WHITE,[960,250])
                buttons[0].set_text(question[1])
                buttons[1].set_text(question[2])
                buttons[2].set_text(question[3])
                buttons[3].set_text(question[4])
            
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        battle = False
                        cont = 1
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        for b in range(len(buttons)):
                            if buttons[b].collision():
                                pygame.mixer.Sound.play(sounds[0])
                                if b+1 == answerNum:
                                    if eSprites[e].get_qNum() == len(eSprites[e].get_qSet())-1:
                                        # if the 3 questions have been answered, end battle
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
                                        # else continue to the next question
                                        eSprites[e].set_qNum("inc")
                                else:
                                    # if the player gets a question wrong
                                    screen.fill(BURG)
                                    pygame.display.update()
                                    time.sleep(0.4) 
                                    player.decrease_health()
                                    hearts.pop()

                # handling players death and win
                if player.get_health() <= 0:
                    screen.fill(BURG)
                    displayResult("DEATH",f"you recieve nothing")
                    player.revive_self()
                    pygame.display.update()
                    time.sleep(1.5)
                    battle = False
                    if game.get_diff() == "Easy":
                        cont = 3
                        # easy mode returns the player to the home screen 
                        # player does not loose any progress
                    else:
                        # medium and hard mode return the player to the main menu
                        # the player looses any progress they didn't save
                        cont = 4
                elif complete:
                    screen.fill(BUTTON2)
                    reward = battleReward()
                    player.inc_chemicals(reward[0])
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
# objects are created inside lists so that they can easily be updated 
# and so they can easily be deleted 

#---------------MAIN---------------#
def main():
    running = "menu"
    # handles screen transitions
    # running represents the current screen type
    # running == "" allows the programme to end
    while running != "":
        # cont is an integer returned from screen subroutines 
        # if cont != 0 then a screen transition will occur
        # cont == 1 means the running will be set to "" and the programme will end 
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