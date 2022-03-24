'''
you will need to install:
pygame
math
random
'''
import time

import pygame
import random
from character_class_v2 import Character
from Enemy import enemy
from Fast_Enemy import fast_enemy
from Button import button
from Tank_Enemy import tank_enemy
from Save import Save
import glob
import pickle
import datetime

# Intialize pygame
pygame.init()
mx, my = pygame.mouse.get_pos()
font = pygame.font.SysFont("font/Pixeltype.ttf",75)
WHITE = (255, 255, 255)
BLACK = (0,0,0)
screen = pygame.display.set_mode((800, 600))

########################################################################################
# Players data
playerX = 400
playerY = 300
rounds = 0
kills = 0
damage_taken = 0
last_update = pygame.time.get_ticks()
cooldown = 300 # how fast the animation is
step_counter = 0


# Enemies data
Enemy_list = []
changeX  = 0
changeY = 0
velocity = 0.01
fast_velocity = 0.05
num_of_enemies = 6



# Player object
character = Character(playerX, playerY, mx, my,BLACK)
character.draw_character()
# ----------------------------------------------------------------------------------------------------------------------


def draw_text(text, font, colour, x, y):
    image = font.render(text, True, colour)
    screen.blit(image, (x, y))

def draw_panel():
    pygame.draw.rect(screen, BLACK, (0,0, 800, 40))
    draw_text('Score:' + str(character.score), font, WHITE, 0, 0)

def spawn(num_of_enemies):
    count = 0
    while count < num_of_enemies:
        EnemyX = random.randint(0, 725) # this
        EnemyY = random.randint(30, 600)
        Enemy_pick = random.randint(0,2)
        if EnemyX <= (character.X + 128) and EnemyX >= (character.X - 128):
            if EnemyY <= (character.Y + 128) and EnemyY >= (character.Y - 128):
                pass
        else:
            if Enemy_pick == 0:
                zombie = enemy(EnemyX, EnemyY,changeX,changeY, BLACK)
                zombie.draw_character()
                Enemy_list.append(zombie)
                count += 1
            elif Enemy_pick == 1:
                zombie_fast = fast_enemy(EnemyX, EnemyY, changeX, changeY, BLACK)
                zombie_fast.draw_character()
                Enemy_list.append(zombie_fast)
                count += 1
            else:
                tough_zombie = tank_enemy(EnemyX, EnemyY, changeX, changeY, BLACK)
                tough_zombie.draw_character()
                Enemy_list.append(tough_zombie)
                count += 1

# loads users scores
def retrieve_character_data():
    previous_characters = []
    for file in glob.glob("*.sav"):
        print(file)
        with open(str(file), "rb") as f:
            previous_characters.append(pickle.load(f))
    return previous_characters


# saves users scores
def save_and_finish(character):
    with open("file.conf") as f:
        for line in f.readlines():
            if 'last_save' in line:
                filenumber = line[12:]
    filename = filenumber + ".sav"
    save_object = Save(character.score,datetime.datetime.now())
    # The idea was to make it look like in the old arcades, with just scores and dates

    with open(filename, "wb") as f:
        pickle.dump(save_object, f)
    with open("file.conf", "w") as f:
        f.write(f"last_save = {str(int(filenumber)+1)}")

    print(filenumber)




# -------- Main Program Loop -----------

def main_menu():

    while True:
        mx,my = pygame.mouse.get_pos()
        screen.fill(BLACK)

        Play_Button = button(400,275,WHITE,font,'PLAY')
        Exit_Button = button(400, 450, WHITE, font, 'EXIT')
        Score_Button = button(400, 350, WHITE, font, 'HIGHSCORE')

        for b in [Play_Button, Exit_Button, Score_Button]:
            b.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if Play_Button.pressed(mx,my):
                    character.current_sprite_sheet = 0
                    game(rounds, kills,num_of_enemies, damage_taken)
                if Exit_Button.pressed(mx,my):
                    pygame.quit()
                    exit()
                if Score_Button.pressed(mx,my):
                    previous_characters = retrieve_character_data()
                    show_high_scores(previous_characters)

        pygame.display.update()

# Screen which displays users previous scores
def show_high_scores(previous_characters):
    while True:
        mx,my = pygame.mouse.get_pos()
        screen.fill(BLACK)
        Exit_Button = button(400, 275, WHITE, font, 'EXIT')
        Back_Button = button(400, 200, WHITE, font, 'BACK')
        buttons = [Exit_Button, Back_Button]
        # enumerate gets both index i of a list, and the list item itself
        for i, character in enumerate(previous_characters):
            buttons.append(button(400, 350 + i*75, WHITE, font, "Score: "+str(character.score) +
            "  Date: " +str(character.date.date())))

        for b in buttons:
            b.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if Exit_Button.pressed(mx,my):
                    pygame.quit()
                    exit()
                if Back_Button.pressed(mx, my):
                    main_menu()

        pygame.display.update()


def game(rounds,kills,num_of_enemies, damage_taken ):
    running = True
    game_over = False
    while running:

        # Background colour
        screen.fill(WHITE)
        if game_over == False:

            for bullet in character.bullets:
                bullet.draw(screen)
                bullet.move()
                for e in Enemy_list:
                   if bullet.has_collided(e.rect):
                       bullet.destroy(bullet, character.bullets)
                       e.damage_taken += 1
                       if e.check_if_dead():
                           character.score += e.points
                           e.destroy(e,Enemy_list)
                           spawn(1)
                           kills +=1
                           #print (character.score)

            # Rounds
            if kills == num_of_enemies:
                kills = 0
                num = 0
                rounds += 1
                num_of_enemies += 1
                spawn(num+1)

            for e in Enemy_list:
                if character.has_collided(e.rect) == True:
                    character.current_sprite_sheet = 4
                    character.frame = 0
                    e.destroy(e, Enemy_list)
                    e.velocity = 0
                    running = False
                    # this is when the game stops
                    save_and_finish(character)
                    spawn(1)



        # Adding the exit button
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w or event.key == pygame.K_s\
                        or event.key == pygame.K_a or event.key == pygame.K_d:
                    character.current_sprite_sheet = 1
                    character.frame = 0
            else:
                if event.type == pygame.KEYUP:
                    character.current_sprite_sheet = 0
                    character.frame = 0

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    character.frame = 0
                    character.current_sprite_sheet = 2
                    character.fire()

        draw_panel()
        enemy.updateAllZombies(Enemy_list, character.X, character.Y, screen)
        character.update(screen,BLACK)
        pygame.display.update()



spawn(num_of_enemies)


# Calling main program
main_menu()
#game(rounds,kills,num_of_enemies)