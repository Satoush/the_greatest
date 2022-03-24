from Enemy import enemy
import pygame
screen = pygame.display.set_mode((800, 600))

class fast_enemy(enemy):
    def __init__(self,Image_path,X,Y,changeX,changeY):
        enemy.__init__(self,Image_path,X,Y,changeX,changeY)
        self.Image_path = pygame.image.load('The_New_Assets/Enemy/Ghost/ghost_.png')
        self.animation_steps = [5, 5, 5, 5, 5, 5]
        self.current_sprite_sheet = 2
        self.sprite = []

        self.points = 10
        self.velocity = 0.125
        self.health = 1




    def check_if_dead(self):
        if self.damage_taken == self.health:
            return True

    def destroy(self,enemy_object, enemy_array):
        if enemy_object in enemy_array:
                print ('tank destroyed')
                enemy_array.remove(self)
                del self


    # def draw(self):
    #     screen.blit(self.Image_path, (self.X , self.Y))
    #     #pygame.draw.rect(screen, pygame.Color("red"), (self.rect))

#pygame.image.load('Assets/zombie.png')




