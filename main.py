import pygame
import math
import random
from pygame import mixer

#initialize the pygame module
pygame.init()

#creating screen
screen = pygame.display.set_mode((800,600))


#background img
background = pygame.image.load('./images/background.png')

#background sound
mixer.music.load('./music/background.wav')
mixer.music.play(-1)


#Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('./images/spaceship.png')
pygame.display.set_icon(icon)


#player
playerimg = pygame.image.load('./images/space-invaders.png')
playerX = 370
playerY = 480
playerX_change = 0


#enemy
enemyimg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyimg.append(pygame.image.load('./images/enemy.png'))
    enemyX.append(random.randint(0,735))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(1)
    enemyY_change.append(40)


#bullet
#ready - can't see the bullet
#fire - bullet is currently moving

bulletimg = pygame.image.load('./images/bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 12
bullet_state = "ready"


# score
score_val = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10


#game over text
over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x,y):
    score = font.render("Score: " + str(score_val) , True , (255,255,255))
    screen.blit(score,(x,y))

def game_over_text():
    over_text = over_font.render(" GAME OVER " , True , (255,255,255))
    screen.blit(over_text,(200 , 250))


def player(x,y):
    screen.blit(playerimg, (x,y))

def enemy(x,y,i):
    screen.blit(enemyimg[i], (x,y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletimg, (x + 16,y + 10))

def isCollision(enemyX,enemyY,bulletX,bulletY):
    distance = math.sqrt( (math.pow(enemyX - bulletX , 2)) + (math.pow(enemyY - bulletY , 2)) )
    if distance < 27 :
        return True
    else:
        return False


#game loop
running = True
while running:

    #background
    screen.fill((0,0,0))

    #bg img
    screen.blit(background,(0,0))


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        #chek keystroke is pressed in left or right
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -10
            if event.key == pygame.K_RIGHT:
                playerX_change = 10
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound('./music/laser.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(playerX,bulletY)


        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0


    #set player into current position after changing movement also
    playerX += playerX_change

    #player boundaries
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736


    #enemy boundaries
    for i in range(num_of_enemies):
        
        #game over
        if enemyY[i] > 440 :
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 7
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -7
            enemyY[i] += enemyY_change[i]

        #Collision
        collision = isCollision(enemyX[i],enemyY[i],bulletX,bulletY)
        if collision:
            explosion_sound = mixer.Sound('./music/explosion.wav')
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_val += 1
            enemyX[i] = random.randint(0,735)
            enemyY[i] = random.randint(50,150)

        enemy( enemyX[i] , enemyY[i] , i )








    #bullet movement
    if bulletY <= 0 :
        bulletY = 480
        bullet_state = "ready"
    if bullet_state is "fire":
        fire_bullet(bulletX,bulletY)
        bulletY -= bulletY_change


   

    #calling player method
    player(playerX,playerY)
    show_score(textX,textY)
    pygame.display.update()