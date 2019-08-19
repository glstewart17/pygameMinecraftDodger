import pygame
import time
import random

# Start game 
pygame.init()

# Display size
displayWidth = 800
displayHeight = 600

# Set Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (200, 0, 0)
green = (0, 200, 0)
bright_red = (255, 0, 0)
bright_green = (0, 255, 0)

# Steve Dimensions
steveSize = 50

# Set up display
gameDisplay = pygame.display.set_mode((displayWidth, displayHeight))
pygame.display.set_caption("Minecraft Dodger")
clock = pygame.time.Clock()

# Load Images
backgroundImage = pygame.image.load('dirt.png')
steveImage = pygame.image.load('steve1.png')
creeperImage = pygame.image.load('creeper.png')

# Set up background image
background = {
      'rect': pygame.Rect(0, 0, 800, 600),
      'surface': pygame.transform.scale(backgroundImage, (800, 600)),
    }


# Count dodged
def things_dodged(count):
    font = pygame.font.SysFont(None, 25)
    text = font.render("Dodged: "+str(count), True, white)
    gameDisplay.blit(text, (2, 2))


# Text object
def text_objects(text, font):
    textSurface = font.render(text, True, white)
    return textSurface, textSurface.get_rect()


# Handle crash
def crash(count):
    crash = True
    largeText = pygame.font.Font('freesansbold.ttf', 60)
    TextSurf, TextRect = text_objects("You died!", largeText)
    TextRect.center = ((displayWidth/2), (displayHeight/2))
    gameDisplay.blit(TextSurf, TextRect)

    # Handle wuit event and make two buttons
    while crash:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        button("Play Again", 125, 400, 150, 50, green, bright_green, game_loop)
        button("Quit", 525, 400, 150, 50, red, bright_red, quitgame)
        pygame.display.update()
        clock.tick(15)


# Set up button
def button(msg, x, y, w, h, ic, ac, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac, (x, y, w, h))
        if click[0] == 1 and action != None:
            action()

    else:
        pygame.draw.rect(gameDisplay, ic, (x, y, w, h))

    smallText = pygame.font.Font("freesansbold.ttf", 20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ((x+(w/2)), (y+(h/2)))
    gameDisplay.blit(textSurf, textRect)


# Quit game
def quitgame():
    pygame.quit()
    quit()


# Intro sceen
def game_intro():

    intro = True

    while intro:
        for event in pygame.event.get():
            # print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # Display intro screen
        gameDisplay.blit(background['surface'], background['rect'])
        largeText = pygame.font.Font('freesansbold.ttf', 70)
        TextSurf, TextRect = text_objects("Minecraft Dodger", largeText)
        TextRect.center = ((displayWidth/2), (displayHeight/2))
        gameDisplay.blit(TextSurf, TextRect)
        button ("GO!",150,400,100,50,green,bright_green,game_loop)
        button ("Quit",550,400,100,50,red,bright_red,quitgame)
        pygame.display.update()
        clock.tick(15)


# Game loop    
def game_loop():

    steve =  {
      'rect': pygame.Rect(375, 500, steveSize, steveSize),
      'surface': pygame.transform.scale(steveImage, (steveSize, steveSize)),
    }
 
    dodged = 0
    
    gameExit = False

    # Set moves to false
    moveRight = False
    moveLeft = False
    moveDown = False
    moveUp = False

    monsters = []
    add = 0

    while not gameExit:

        # Handle game events
        for event in pygame.event.get():
            
            # Handle QUIT
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            # Handle KEYDOWN
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == ord('a'):
                    moveRight = False
                    moveLeft = True
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    moveLeft = False
                    moveRight = True
                if event.key == pygame.K_UP or event.key == ord('w'):
                    moveDown = False
                    moveUp = True
                if event.key == pygame.K_DOWN or event.key == ord('s'):
                    moveUp = False
                    moveDown = True

            # Handle KEYUP
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == ord('a'):
                    moveLeft = False
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    moveRight = False
                if event.key == pygame.K_UP or event.key == ord('w'):
                    moveUp = False
                if event.key == pygame.K_DOWN or event.key == ord('s'):
                    moveDown = False
        
        # Handle movement
        if moveDown == True and steve['rect'].bottom < displayHeight:
          steve['rect'].move_ip(0, 5)

        if moveUp == True and steve['rect'].top > 0:
          steve['rect'].move_ip(0, -5)

        if moveRight == True and steve['rect'].right < displayWidth:
            steve['rect'].move_ip(5, 0)

        if moveLeft == True and steve['rect'].left > 0:
            steve['rect'].move_ip(-5, 0)

        # Fill dispplay
        gameDisplay.blit(background['surface'], background['rect'])

        # Steve
        gameDisplay.blit(steve['surface'], steve['rect'])

        # Monster movement
        for mon in monsters:

          mon['rect'].move_ip(0, mon['speed'])

          if mon['rect'].top > displayHeight:
                monsters.remove(mon)
                dodged += 1

                # Add new monster
                monsterSize = random.randint(20, 100)
                monsterSpeed = random.randint(3, 8)
                monster = {'rect': pygame.Rect(random.randint(0, displayWidth - monsterSize), 0 - monsterSize, monsterSize, monsterSize),
                              'speed': monsterSpeed,
                              'surface': pygame.transform.scale(creeperImage, (monsterSize, monsterSize)),
                              }
                monsters.append(monster)

                # Contuinue
                continue

          gameDisplay.blit(mon['surface'], mon['rect'])

          # If player and monster interstect, crash
          if steve['rect'].colliderect(mon['rect']):
                things_dodged(dodged)
                crash(dodged)

        
        # Add monster
        if add % 25 == 1:
          monsterSize = random.randint(20, 100)
          monsterSpeed = random.randint(3, 8)
          monster = {'rect': pygame.Rect(random.randint(0, displayWidth - monsterSize), 0 - monsterSize, monsterSize, monsterSize),
                         'speed': monsterSpeed,
                         'surface': pygame.transform.scale(creeperImage, (monsterSize, monsterSize)),
                         }
          monsters.append(monster)


        # Display Dodged
        things_dodged(dodged)
        add+=1
        pygame.display.update()
        clock.tick(15)


# Start and end game
game_intro()
pygame.quit()
quit()