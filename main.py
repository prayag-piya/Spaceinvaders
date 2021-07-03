import pygame, random, math

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
for i in range(8):
    x = random.randint(64, 100)
    img = pygame.image.load('rock.png')
    img = pygame.transform.scale(img, (x, x))
    rock.append(img)
    rockx.append(random.randrange(-10, 936))
    rocky.append(random.randrange(0 ,40))
    rmovex.append(random.randrange(-3, 3) + 1)
    rmovey.append(random.randrange(0, 3) + 1)

fired_bullet = []
bullet = pygame.image.load('bullet.png')
bulletx = 0
bullety = 0
bmovex = 0
bmovey = 10
newbullety = 0
newbulletx = 0
second_fire = False
bullet_state = "ready"

score = 0

def enemyImg(x, y):
    win.blit(enemy, (x, y))

def newBullet(x, y):
    win.blit(bullet, (x, y))

def playerImg(x, y):
    win.blit(player, (x, y))

def get_player_rect():
    return pygame.Rect(playerx, playery, 64, 64)

def get_enemy_rect():
    return pygame.Rect(enemyx, enemyY, 64, 64)

def rockImg(x, y, i):
    win.blit(rock[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
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
                if bullet_state == "ready":
                    bulletx = playerx
                    bullety= playery
                    bullet_state = "fire"
                else:
                    if bullety < 200:
                        newbulletx = playerx
                        newbullety = playery
                        second_fire = True
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

    collision = isCollision(enemyx, enemyY, bulletx, bullety)
    forsecond = isCollision(enemyx, enemyY, newbulletx, newbullety)

    if collision:
        bullety = playery
        bullet_state = "ready"
        score += 1
        enemyx = random.randint(0, 936)
        enemyY = random.randint(5, 10) * -1
        print(score)
    elif forsecond:
        newbullety = playery
        second_fire = False
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

    if bullety < 0:
        bullety = playery
        bullet_state = "ready"

    if newbullety < 0:
        newbullety = playery
        second_fire = False

    if bullet_state == "fire":
        fire_bullet(bulletx, bullety)
        bullety -= bmovey

    if second_fire:
        newBullet(newbulletx, newbullety)
        newbullety -= bmovey

    
    pygame.display.update()