import pygame
import random
import bananaClass
pygame.init()
WIDTH, HEIGHT = 800, 800
SCALE = 2.5
FPS = 40
BLACK = (0,0,0)
WHITE = (255,255,255)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Testing")
clock = pygame.time.Clock()



def updateBananas(bananaList):
    for i in range (len(bananaList)):
        scale = bananaList[i].get_scale()
        image = bananaList[i].get_sheet()
        image = pygame.transform.scale(image,(230*scale,200*scale))
        surface = pygame.Surface((230*scale,200*scale))
        surface.blit(image,(0,0),((0),(0),600,600))
        screen.blit(surface,bananaList[i].get_pos())
        bananaList[i].grow()

        


bananaList = []
running = True
while running:
    screen.fill(BLACK)
    if len(bananaList) > 0:
        updateBananas(bananaList)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            num = len(bananaList)
            pos = pygame.mouse.get_pos()
            pos = [pos[0]-115,pos[1]-100]
            bananaList.append(bananaClass.Banana(num,pos))
    pygame.display.update()
    clock.tick(FPS)
pygame.quit()


