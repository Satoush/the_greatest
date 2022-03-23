import pygame
import random

screen = pygame.display.set_mode((800, 600))


class enemy():
    def __init__(self, X, Y, changeX, changeY, colour):
        self.Hit_box = pygame.image.load('Assets/User_iconnn.png')
        self.Image_path = pygame.image.load('The_New_Assets/Enemy/Goblin/goblin_.png')
        self.sprite = []
        self.X = X
        self.Y = Y
        self.changeX = changeX
        self.changeY = changeY
        self.colour = colour
        self.width = 24
        self.height = 24

        self.cooldown = 100
        self.current_sprite_sheet = 2  # gets the current sprite sheet from the list
        self.step_counter = 0
        self.frame = 0


        self.last_update = pygame.time.get_ticks()
        self.velocity = 0.05
        # self.num_of_enemies = 6
        self.animation_steps = [5,5,5,5,5,5]
        self.points = 5
        self.rect = self.Hit_box.get_rect(center=(self.X, self.Y))
        self.damage_taken = 0
        self.health = 2

    def get_image(self, the_current_frame, scale, colour, stage):
        image = pygame.Surface((self.width, self.height)).convert_alpha()# creates a blank surface
        image.blit(self.Image_path, (0, 0), ((the_current_frame * self.width),(stage * self.height), self.width, self.height)) # third argument specifies what part of the image to display(
        # cuts the rest for the images out)
        image = pygame.transform.scale(image,(self.width * scale, self.height * scale))
        image.set_colorkey(colour) # to make the background transparant

        return image


    def draw_character(self):
        stage = 0
        for animation in self.animation_steps:
            temp_list = []
            for i in range(animation):
                temp_list.append(self.get_image(self.step_counter,  3, self.colour, stage))
                self.step_counter += 1
            stage += 1
            self.step_counter = 0
            self.sprite.append(temp_list)

    def animate_character(self,screen):
        current_time = pygame.time.get_ticks()  # takes the time the code is being executed
        if current_time - self.last_update >= self.cooldown:
            self.frame += 1
            self.last_update = current_time  # resets the cooldown
            if self.frame >= len(self.sprite[self.current_sprite_sheet]) - 1:  # makes sure the list doesnt go out of range
               self.frame = 0

        # show frame image





    # Adding basic movement towards player
    def move_to_player(self, PlayerX, PlayerY):

        if self.X > PlayerX:
            self.changeX = -1 * self.velocity
            flipped_image = pygame.transform.flip(self.sprite[self.current_sprite_sheet][self.frame],True, False)
            flipped_image.set_colorkey(self.colour)
            current_image = flipped_image
        else:
            current_image = self.sprite[self.current_sprite_sheet][self.frame]


        if self.X < PlayerX:
            self.changeX = self.velocity

        else:
            if self.Y == PlayerX:
                self.changeX = 0

        if self.Y > PlayerY:
            self.changeY = -1 * self.velocity

        elif self.Y < PlayerY:
            self.changeY = self.velocity

        else:
            if self.Y == PlayerY:
                self.changeY = 0


        self.rect[0] = self.X
        self.rect[1] = self.Y

        self.X += self.changeX
        self.Y += self.changeY

        self.rect[1] += self.changeY
        self.rect[0] += self.changeX

        screen.blit(current_image, (self.X,self.Y))
        #pygame.draw.rect(screen, "red", (self.rect))
        
    def check_if_dead(self):
        if self.damage_taken == self.health:
            return True


    def destroy(self, enemy_object, enemy_array):
        if enemy_object in enemy_array:
            enemy_array.remove(self)
            del self

    def update(self, PlayerX, PlayerY, screen):
        self.move_to_player(PlayerX, PlayerY)
        self.animate_character(screen)

    @staticmethod
    def updateAllZombies(Enemy_list, PlayerX, PlayerY, screen):
        for e in Enemy_list:
            e.update(PlayerX, PlayerY, screen)


