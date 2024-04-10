import math
import random

from pygame.locals import *
import pygame
from pygame import mixer

pygame.init()

#crear la pantalla
screen = pygame.display.set_mode((800, 600))

start = pygame.font.SysFont('Monospace', 56)
start_value = 'COMENZAR'

#agregar un fondo
background = pygame.image.load('./background.png')

# titulo de ventana e icono
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('./ufo.png')
pygame.display.set_icon(icon)

# puntos
score_value = 0
font = pygame.font.SysFont('Monospace', 32)

textX = 10
textY = 10

# jugador
playerImg = pygame.image.load('./player.png')
playerX = 370
playerY = 480
playerX_change = 0

def player(x, y):
    screen.blit(playerImg, (x, y))

# enemigos
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('./enemy.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

# balas
# estado -> ready - para que la bala no se vea en pantalla
# estado -> fire - la bala se mueve

bulletImg = pygame.image.load('./bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False

# Inicio
running = True
while running:

    # color de fondo de la ventana original
    screen.fill((0, 0, 0))

    # seteamos la imagen elegida para el bg
    screen.blit(background, (0, 0))

    # para salir del juego presionando la X en la ventana
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # eventos del teclado
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bulletSound = mixer.Sound("./laser.wav")
                    bulletSound.play()
                    # coordinamos la posicion de la bala con la del jugador
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        # dejamos de mover al jugador si soltamos la tecla presionada
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

        # se termina el juego si matamos 10 enemigos
        if score_value == 10:
            running = False

    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # movimientos del enemigo
    for i in range(num_of_enemies):

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]
 
        enemy(enemyX[i], enemyY[i], i)

        # configuraciones de ataque, sonido de explosión 
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosionSound = mixer.Sound("./explosion.wav")
            explosionSound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

    # moviemientos de bala
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
