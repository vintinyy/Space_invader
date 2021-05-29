import pygame
import random

#initalize 
pygame.init()

#initalize display
screen = pygame.display.set_mode((800,600))
background = pygame.image.load("c:\\Users\\vinti\\OneDrive\\Documents\\Python Projects\\Python\\Space_invader\\background.jpg")

#player
playerImage = pygame.image.load("c:\\Users\\vinti\\OneDrive\\Documents\\Python Projects\\Python\\Space_invader\\spaceship.png")
playerX = 370
playerY = 480
playerXchange = 0
playerYchange = 0
def player(X, Y):
    screen.blit(playerImage, (X,Y))

#enemy
class Enemy:
    def __init__(self):
        self.image = pygame.image.load("c:\\Users\\vinti\\OneDrive\\Documents\\Python Projects\\Python\\Space_invader\\alien.png")
        self.x = random.randint(0,736)
        self.y = random.randint(0,150)
        self.Xchange = 3
        self.Ychange = 20

    def setXchange(self, change):
        self.Xchange = change
    
    def adjustY(self):
        self.y += self.Ychange

    def adjustX(self):
        self.x += self.Xchange

    def draw(self):
        screen.blit(self.image, (self.x, self.y))
    
    def respawn(self):
        self.x = random.randint(0,736)
        self.y = random.randint(0,150)

numEnemies = 6
enemies = []
for i in range(numEnemies):
    enemies.append(Enemy())
   
#laser
laserImage = pygame.image.load("c:\\Users\\vinti\\OneDrive\\Documents\\Python Projects\\Python\\Space_invader\\assets\\pixel_laser_blue.png")
laserX = 0
laserY = 0
laserXchange = 3
laserYchange = 10
laserState = 'ready'

def laser(X, Y):
    global laserState
    laserState = 'fire'
    screen.blit(laserImage, (X -21, Y -20))

def isCollison(enemyX, enemyY, laserX, laserY):
    if(enemyX-64 <= laserX <= enemyX+64 and enemyY-64 <= laserY <= enemyY+64):
        return True
    return False

#game loop
running = True
while running:
    screen.blit(background,(0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:               
                playerXchange = -6
            if event.key == pygame.K_RIGHT:               
                playerXchange = 6
            if event.key == pygame.K_UP:               
                playerYchange = -6
            if event.key == pygame.K_DOWN:              
                playerYchange = 6
            if event.key == pygame.K_SPACE:
                laserX = playerX
                laserY = playerY
                laser(laserX, laserY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerXchange = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerYchange = 0


    #player movement
    playerX += playerXchange
    playerY += playerYchange

    #check for boundaries
    if playerX > 736:
        playerX = 736
    if playerX < 0:
        playerX = 0
    if playerY > 536:
        playerY = 536
    if playerY < 0:
        playerY = 0
            
    player(playerX, playerY)

    #enemy movement
    for enemy in enemies:
        if enemy.x < 0:
            enemy.setXchange(3)
            enemy.adjustY()
        if enemy.x > 736:
            enemy.setXchange(-3)
            enemy.adjustY()
        
        enemy.adjustX()
        #check for collison     
        if isCollison(enemy.x, enemy.y, laserX, laserY):
            enemy.respawn()
            laserY = playerY
            laserState = 'ready'

        enemy.draw()
    

    #laser movement
    if laserState == 'fire':
        laser(laserX, laserY)
        laserY -= laserYchange
        
    if laserY < 0:
        laserState = 'ready'      

    pygame.display.update()