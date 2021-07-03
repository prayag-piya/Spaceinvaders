import pygame, random, math, time

SIZE = (1000, 600)

pygame.init()
win = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Star Invaders")

clock = pygame.time.Clock()

icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

bg = pygame.image.load('background.jpg')
bg = pygame.transform.scale(bg, (1000, 600))

player = pygame.image.load('spaceship.png')
playerx = 370
playery = 500
health = 20
movex = 0
movey = 0

enemy = pygame.image.load('alien.png')
enemyx = random.randint(0, 936)
enemyY = random.randint(20, 40) * -1
emovex = 3
emovey = 3

rock = []
rockx = []
rocky = []
rmovex = []
rmovey = []
rockRect = []
for i in range(8):
    x = random.randint(64, 100)
    img = pygame.image.load('rock.png')
    img = pygame.transform.scale(img, (x, x))
    rock.append(img)
    rx = random.randrange(-10, 936)
    ry = random.randrange(0 ,40)
    rockx.append(rx)
    rocky.append(ry)
    rmovex.append(random.randrange(-3, 3) + 1)
    rmovey.append(random.randrange(0, 3) + 1)
    rockRect.append(pygame.Rect(rx, ry, x, x))

fired_bullet = []
bulletx = []
bullety = []
# bulletRect = []
bmovex = 0
bmovey = 10
# bullet = pygame.image.load('bullet.png')
bullet_state = "ready"

score = 0

def enemyImg(x, y):
    win.blit(enemy, (x, y))

def playerImg(x, y):
    win.blit(player, (x, y))

def get_bullet_rect():
    bulletRect = []
    for i in range(len(fired_bullet)):
        bulletRect.append(pygame.Rect(bulletx[i], bullety[i], 32, 32))
    return bulletRect

def get_player_rect():
    return pygame.Rect(playerx, playery, 64, 64)

def get_enemy_rect():
    return pygame.Rect(enemyx, enemyY, 64, 64)


def rockImg(x, y, i):
    win.blit(rock[i], (x, y))

def fire_bullet(bullet, x, y):
    win.blit(bullet, (x+16, y-32))

def isCollision(enemyx, enemyY, bulletx, bullety):
    distance = math.sqrt((math.pow(enemyx-bulletx,2))+ (math.pow(enemyY- bullety,2)))
    #print(distance)
    if distance < 27:
        return True
    else:
        return False


running = True
while running:
    clock.tick(60)
    win.blit(bg, (0,0))
    
    playerImg(playerx, playery)
    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                movex = 5
            if event.key == pygame.K_LEFT:
                movex = -5
            if event.key == pygame.K_UP:
                movey -= 5
            if event.key == pygame.K_DOWN:
                movey = 5
            if event.key == pygame.K_SPACE:
                fired_bullet.append(pygame.image.load('bullet.png'))
                bullety.append(playery)
                bulletx.append(playerx)
                # bulletRect.append(pygame.Rect(playerx, playery, 32, 32))
                #adding new feature in another branch 
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                movex = 0
                movey = 0

    for i in range(8):
        rockImg(rockx[i], rocky[i], i)
        rockx[i] += rmovex[i]
        rocky[i] += rmovey[i]

        if rocky[i] >= 600:
            rmovex[i] = random.randrange(-3, 3)
            rockx[i] = random.randrange(-10, 936)
            rocky[i] = random.randrange(0, 40)

    playerx += movex
    playery += movey

    if playerx <= 0:
        playerx = 0
    elif playerx >= 936:
        playerx = 936
    
    if playery <= 0:
        playery = 0
    elif playery >= 536:
        playery = 536

    enemyY += emovey

    if enemyY > 610:
        enemyx = random.randint(0, 963)
        enemyY = random.randint(20, 40) * -1

    
    if len(fired_bullet) > 0:
        if bullety[0] <= 0:
            bullety.pop(0)
            bulletx.pop(0)
            fired_bullet.pop(0)

    index = len(fired_bullet)
    # print(index)

    for i in range(index):

        fire_bullet(fired_bullet[i], bulletx[i], bullety[i])
        bullety[i] -= bmovey

        # print(get_bullet_rect())

        collision = isCollision(enemyx, enemyY, bulletx[i], bullety[i])

        if collision:
            bullety[i] = playery
            score += 1
            enemyx = random.randint(0, 936)
            enemyY = random.randint(5, 10) * -1
            print(score) 

    enemyImg(enemyx, enemyY)

    enemyRect = get_enemy_rect()
    playerRect = get_player_rect()

    if enemyRect.colliderect(playerRect):
        health -= 10
        enemyx = random.randint(0 , 963)
        enemyY = random.randint(0, 10) * -1
                

    if health == 0:
        print("Game Over")
        running = False 

    
    pygame.display.update()