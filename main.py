import pygame
import time
from sys import exit
import os
import random

#Setup
os.chdir(os.path.dirname(os.path.abspath(__file__)))
pygame.init()
screen = pygame.display.set_mode((800,400))
logo = pygame.image.load("assets/logo.ico")
pygame.display.set_icon(logo)
pygame.display.set_caption("Jumpy Dude")
clock = pygame.time.Clock()
testcheck = 0
timer_event = pygame.USEREVENT + 1
newhighscorecheck = False
restartcheck = 0
highscore = 0
scoring = False
check = True
first = True
points = 0
game_active = True
speed = 3
gravity = 0

#Loading Assets
font = pygame.font.Font("assets/flappybird.ttf",150)
smaller_font = pygame.font.Font("assets/flappybird.ttf",75)
score_font = pygame.font.Font("assets/flappybird.ttf",75)
logo_font = pygame.font.Font("assets/tamaya-smooth.ttf", 15)
background = pygame.image.load("assets/background.jpg").convert_alpha()
ground = pygame.image.load("assets/ground.png").convert_alpha()
player = pygame.image.load("assets/dude.png").convert_alpha()
pipe1 = pygame.image.load("assets/pipe1.png").convert_alpha()
pipe2 = pygame.image.load("assets/pipe2.png")
gap = pygame.image.load("assets/gap.png")
ground_rec = ground.get_rect(bottomleft = (0,400))
player_rec = player.get_rect(center = (50,200))
pipe1_rec = pipe1.get_rect(midbottom = (800,500))
gap_rec = gap.get_rect(midbottom = pipe1_rec.midtop)
pipe2_rec = pipe2.get_rect(midbottom = gap_rec.midtop)


while True:
    key = pygame.key.get_pressed()
    mouse = pygame.mouse.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
            gravity -= 13

    if game_active and not first:
        
        #Rendering Assets
        score = score_font.render(str(points), False, "Gold")
        score_rec = score.get_rect(center = (400,50))
        screen.blit(background, (0,0))
        screen.blit(pipe1,pipe1_rec)
        screen.blit(pipe2,pipe2_rec)
        screen.blit(ground,ground_rec)
        screen.blit(player,player_rec)
        screen.blit(score,score_rec)

        #Collisions
        if player_rec.colliderect(pipe1_rec) or player_rec.colliderect(pipe2_rec):
            game_active = False

        if player_rec.colliderect(gap_rec) and check:
            check = False
        elif not player_rec.colliderect(gap_rec) and not check:
            points += 1
            check = True

        if not scoring:
            points = 0
            scoring = True

        #Movement
        pipe1_rec.left -= speed
        gap_rec.midbottom = pipe1_rec.midtop
        pipe2_rec.midbottom = gap_rec.midtop

        gravity += 0.5
        player_rec.y += gravity

        if player_rec.bottom >= (400-36):
           player_rec.bottom = (400-36)
           gravity = 0
        if player_rec.top <= 0:
            player_rec.top = 0
            gravity = 0
        if pipe1_rec.right <= 0:
            pipe1_rec.left = 800
            pipe1_rec.bottom = random.randint(375,500)

        newhighscorecheck = False
        restartcheck = 0

    elif first:
        screen.blit(background, (0,0))
        screen.blit(pipe1,pipe1_rec)
        screen.blit(gap,gap_rec)
        screen.blit(pipe2,pipe2_rec)
        screen.blit(ground, ground_rec)
        logo = logo_font.render("JXCK DEVELOPMENT", False, "Cyan")
        logo_rec = logo.get_rect(bottomright = (800,400))
        screen.blit(logo, logo_rec)
        pipe1_rec.x = 550
        gap_rec.midbottom = pipe1_rec.midtop
        pipe2_rec.midbottom = gap_rec.midtop
        title = font.render("jumpy dude", False, (230, 39, 99))
        title_rec = title.get_rect(center = (400,50))
        start = smaller_font.render("press space to play", False, "Orange")
        start_rec = start.get_rect(center = (400,300))
        screen.blit(title,title_rec)
        screen.blit(start,start_rec)
        screen.blit(player,player_rec)
        if key[pygame.K_SPACE]:
            first = False
            game_active = True

    elif not game_active:
        currentscore = score_font.render(str(points), False, (101, 0, 138))
        currentscore_rec = currentscore.get_rect(center = (400,225))
        newhighscore = score_font.render("NEW HIGH SCORE", False, "Green")
        newhighscore_rec = newhighscore.get_rect(center = (400,175))
        highscoretext = score_font.render("high score: "+str(highscore), False, (101, 0, 138))
        highscoretext_rec = highscoretext.get_rect(center = (400,275))
        died = font.render("you died", False, "Red")
        died_rec = died.get_rect(center = (400,50))
        tryagain = smaller_font.render("press space to try again", False, "Orange")
        tryagain_rec = tryagain.get_rect(center = (400,350))
        screen.blit(background, (0,0))
        screen.blit(ground, ground_rec)
        screen.blit(currentscore, currentscore_rec)
        screen.blit(died,died_rec)
        screen.blit(highscoretext, highscoretext_rec)
        if restartcheck < 60:
            restartcheck += 1
        else:
            screen.blit(tryagain,tryagain_rec)
        if highscore < points or newhighscorecheck:
            highscore = points
            newhighscorecheck = True
            screen.blit(newhighscore,newhighscore_rec)
        if key[pygame.K_SPACE] and restartcheck == 60:
            scoring = False
            game_active = True
            pipe1_rec.bottom = random.randint(375,500)
            pipe1_rec.left = 800
            gap_rec.left = 800
            pipe2_rec.left = 800
            gravity = 0

    pygame.display.update()
    clock.tick(60)
