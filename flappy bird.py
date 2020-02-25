import random
import os
import sys
import pygame
from pygame.locals import *

FPS = 35
SCREENWIDTH = 950
SCREENHEIGHT = 710
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
GROUNDY = SCREENHEIGHT*0.85
GAME_SPRITES = {}
GAME_SOUNDS = {}
PLAYER = 'game/bird/download.png'
BACKGROUND = 'game/background/background.png'
PIPE = 'game/pipe/6d2a698f31595a1.png'

def welcome():
    playerx = int(SCREENWIDTH/2.4)
    playery = int(SCREENHEIGHT*0.15)
    messagex = int(SCREENWIDTH - GAME_SPRITES['player'].get_width())/4.5
    messagey = (SCREENHEIGHT*0.2)
    basex=0

    while True:
        GAME_SOUNDS['FIRST'].play()
        for event in pygame.event.get():
            if (event.type == QUIT) or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            elif (  (event.type == KEYDOWN) and (event.key == K_SPACE or event.key == K_UP)):
                return
            else:
                SCREEN.blit(GAME_SPRITES['background'], (0, 0))
                SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))
                SCREEN.blit(GAME_SPRITES['messag'], (messagex, messagey))
                SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
                SCREEN.blit(GAME_SPRITES['base'], (335, GROUNDY))
                SCREEN.blit(GAME_SPRITES['base'], (670, GROUNDY))
                pygame.display.update()
                FPSCLOCK.tick(FPS)


def game():
    score = 0
    playerx = int(SCREENWIDTH/5)
    playery = int(SCREENWIDTH/2)
    basex = 0

    pipe1 = getRandomPipe()

    pipe2 = getRandomPipe()

    upperpipes = [
        {'x':(SCREENWIDTH+200), 'y':pipe1[0]['y']},
        {'x':(SCREENWIDTH + 200 + (SCREENWIDTH/2)), 'y':pipe2[0]['y']}
    ]
    lowerpipes = [
        {'x':(SCREENWIDTH+200), 'y':pipe1[1]['y']},
        {'x':(SCREENWIDTH + 200 + (SCREENWIDTH/2)), 'y':pipe2[1]['y']}
    ]


    pipevelX = -4
    playerVelY = -9
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAccY = 1

    playerAccV = -8
    playerFlapped = False

    while True:
        GAME_SOUNDS['FIRST'].play()

        for event in pygame.event.get():
            if (event.type == QUIT) or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            elif (event.type == KEYDOWN) and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0:
                    playerVelY = playerAccV
                    playerFlapped = True
        crasheTest = iscollide(playerx, playery, upperpipes, lowerpipes)

        if crasheTest:
            return


        playerMidPos = playerx + GAME_SPRITES['player'].get_width()/2
        for pipe in upperpipes:
            pipeMidPos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width()/2
            if pipeMidPos<= playerMidPos < pipeMidPos+4:
                score += 1
                print(f"your score is {score}")

        if playerVelY < playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY
        if playerFlapped:
            playerFlapped = False

        playerHeight = GAME_SPRITES['player'].get_height()
        playery = playery + min(playerVelY, GROUNDY - playery- playerHeight)

        for upperpipe, lowerpipe in zip(upperpipes, lowerpipes):
            upperpipe['x']+=pipevelX
            lowerpipe['x']+=pipevelX

        if 0<upperpipes[0]['x']<5 :
            newpipe = getRandomPipe()
            upperpipes.append(newpipe[0])
            lowerpipes.append(newpipe[1])

        if upperpipes[0]['x']< -GAME_SPRITES['pipe'][0].get_width():
            upperpipes.pop(0)
            lowerpipes.pop(0)

        SCREEN.blit(GAME_SPRITES['background'], (0, 0))
        for upperpipe, lowerpipe in zip(upperpipes, lowerpipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0], (upperpipe['x'], upperpipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1], (lowerpipe['x'], lowerpipe['y']))
        SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
        SCREEN.blit(GAME_SPRITES['base'], (335, GROUNDY))
        SCREEN.blit(GAME_SPRITES['base'], (670, GROUNDY))
        SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))
        myDigit = [int(x) for x in list(str(score))]
        width = 0

        for digit in myDigit:
            width += GAME_SPRITES['num'][digit].get_width()
        xoffset = (SCREENWIDTH - width)/2
        for digit in myDigit:
            SCREEN.blit(GAME_SPRITES['num'][digit],(xoffset, SCREENHEIGHT*0.12))
            xoffset+=GAME_SPRITES['num'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def iscollide(playerx, playery, upperpipes, lowerpipes):
    if playery> GROUNDY-25 or playery<0:
        return True

    for pipe in upperpipes:
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()

        if (playery <= pipeHeight + pipe['y'] and abs(playerx - pipe['x']) <= GAME_SPRITES['player'].get_width()):
             return True

    for pipe in lowerpipes:
        if (playery + GAME_SPRITES['player'].get_height()>=pipe['y'] and  abs(playerx - pipe['x'])<=GAME_SPRITES['player'].get_width() ):
             return True


def getRandomPipe():

    pipeHeight = GAME_SPRITES['pipe'][0].get_height()
    offset = SCREENHEIGHT/3
    y2 = offset + random.randrange(0, int(SCREENHEIGHT - GAME_SPRITES['base'].get_height() - 1.2*offset))
    y1 = pipeHeight - y2 + offset
    pipex = SCREENWIDTH + 10
    pipe = (
        {'x':pipex, 'y':-y1},
        {'x':pipex, 'y': y2}
    )

    return pipe






if __name__ == "__main__":

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('flappy bird with shivam')
    GAME_SPRITES['num'] = (
        pygame.image.load('game/numbers/0-Number-PNG.png').convert_alpha(),
        pygame.image.load('game/numbers/1-Number-PNG.png').convert_alpha(),
        pygame.image.load('game/numbers/2-Number-PNG.png').convert_alpha(),
        pygame.image.load('game/numbers/3-Number-PNG.png').convert_alpha(),
        pygame.image.load('game/numbers/4-Number-PNG.png').convert_alpha(),
        pygame.image.load('game/numbers/5-Number-PNG.png').convert_alpha(),
        pygame.image.load('game/numbers/6-Number-PNG.png').convert_alpha(),
        pygame.image.load('game/numbers/7-Number-PNG.png').convert_alpha(),
        pygame.image.load('game/numbers/8-Number-PNG.png').convert_alpha(),
        pygame.image.load('game/numbers/9-Number-PNG.png').convert_alpha(),

    )

    GAME_SPRITES['messag'] = pygame.image.load('game/message/pygame_logo.gif').convert_alpha()
    GAME_SPRITES['base'] = pygame.image.load('game/base/Flappy-Ground.png').convert_alpha()
    GAME_SPRITES['pipe'] = (
       pygame.transform.rotate(pygame.image.load( PIPE ).convert_alpha(), 180),
        pygame.image.load( PIPE).convert_alpha()
    )
    GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert()
    GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()
    os.getcwd()
    pygame.mixer.pre_init()
    GAME_SOUNDS['FIRST'] = pygame.mixer.Sound('game/sound/birds022.wav')

    while True:

        #r = sr.Recognizer()
        #with sr.Microphone() as source:
            #print('listening...')
            #r.pause_threshold = 1
           # audio = r.listen(source)
          #  print('recognizing...')
         #   query = r.recognize_google(audio)
        #if 'open game' in query:
        welcome()
        game()