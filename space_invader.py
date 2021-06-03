import pygame
import random
from pygame import mixer

#initalize 
pygame.init()

#initalize display
screen = pygame.display.set_mode((800,600))
background = pygame.image.load("c:\\Users\\vinti\\OneDrive\\Documents\\Python Projects\\Python\\Space_invader\\assets\\background.jpg")

#score
score_value = 0
font = pygame.font.Font("freesansbold.ttf", 32)
textX = 10
textY = 10
overFont = pygame.font.Font("freesansbold.ttf", 64)


def showScore(x,y):
    score = font.render("Score: " + str(score_value), True, (255,255,255))
    screen.blit(score, (x,y))

def gameOver():
    overText = overFont.render("Game Over", True, (255,255,255))
    screen.blit(overText, (200,250))

#player
class Player:
    def __init__(self):
        self.image = pygame.image.load("c:\\Users\\vinti\\OneDrive\\Documents\\Python Projects\\Python\\Space_invader\\assets\\spaceship.png")
        self.X = 370
        self.Y = 480
        self.Xchange = 0
        self.Ychange = 0
        self.health = 100


    def draw(self):
        screen.blit(self.image, (self.X, self.Y))
    
    def damage(self, amount):
        self.health -= amount
    
    def heal(self, amount):
        self.health += amount

    #def die():
    
    def setXchange(self, change):
        self.Xchange = change
    
    def setYchange(self, change):
        self.Ychange = change
    
    def adjustY(self):
        self.Y += self.Ychange

    def adjustX(self):
        self.X += self.Xchange

player = Player()


#enemy
class Enemy:
    def __init__(self):
        self.image = pygame.image.load("c:\\Users\\vinti\\OneDrive\\Documents\\Python Projects\\Python\\Space_invader\\assets\\alien.png")
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
    e = Enemy()
    enemies.append(e)
   
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
    showScore(textX,textY)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:               
                player.setXchange(-6)
            if event.key == pygame.K_RIGHT:               
                player.setXchange(6)
            if event.key == pygame.K_UP:               
                player.setYchange(-6) 
            if event.key == pygame.K_DOWN:              
                player.setYchange(6)
            if event.key == pygame.K_SPACE:
                laserX = player.X
                laserY = player.Y
                laser(laserX, laserY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player.setXchange(0)
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                player.setYchange(0)
        


    #player movement
    player.adjustX()
    player.adjustY()

    #check for boundaries
    if player.X > 736:
        player.X = 736
    if player.X < 0:
        player.X = 0
    if player.Y > 536:
        player.Y = 536
    if player.Y < 0:
        player.Y = 0
            
    player.draw()

    #enemy movement
    for enemy in enemies:
        if enemy.x < 0:
            enemy.setXchange(3)
            enemy.adjustY()
        if enemy.x > 736:
            enemy.setXchange(-3)
            enemy.adjustY()
        if enemy.y > 550:
            player.damage(25)

        #check for player health
        if player.health <= 0:
            gameOver()
            break
        
        enemy.adjustX()
        #check for collison     
        if isCollison(enemy.x, enemy.y, laserX, laserY):
            enemy.respawn()
            laserY = player.Y
            laserState = 'ready'
            score_value+=1
            explosionSound = mixer.Sound("assets\\explosion.wav")
            explosionSound.play()

        enemy.draw()
    

    #laser movement
    if laserState == 'fire':
        laser(laserX, laserY)
        laserY -= laserYchange
        
    if laserY < 0:
        laserState = 'ready'      

    pygame.display.update()