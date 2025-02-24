# imports

import pygame
import math
import random
import time

# color definitions

BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

# variable definitions

done = False

clock = pygame.time.Clock()

# general function definitions

def get_image(self, x, y, width, height):
        image = pygame.Surface([width, height]).convert()
        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        image.set_colorkey(BLACK)
        return image

class SpriteSheet(object):
    def __init__(self, file_name):
        self.sprite_sheet = pygame.image.load(file_name).convert()
    def get_image(self, x, y, width, height):
        image = pygame.Surface([width, height]).convert()
        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        image.set_colorkey(BLACK)
        return image

# class definitions

class Player(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width, height])
        player = SpriteSheet("spritesheet.png")
        self.image = player.get_image(0,0,80,100)
        self.rect = self.image.get_rect()
        self.xspeed = 0
        self.yspeed = 0
        self.speed = 4
        self.W = False
        self.A = False
        self.S = False
        self.D = False
    def update(self):

        # vertical movement checks

        if self.W == False and self.S == False:
            self.yspeed = 0
        elif self.W == True and self.S == True:
            self.yspeed = 0
        elif self.W == True and self.S == False:
            self.yspeed = -self.speed
        elif self.W == False and self.S == True:
            self.yspeed = self.speed
        
        # horizontal movement checks

        if self.A == False and self.D == False:
            self.xspeed = 0
        elif self.A == True and self.D == True:
            self.xspeed = 0
        elif self.A == True and self.D == False:
            self.xspeed = -self.speed
        elif self.A == False and self.D == True:
            self.xspeed = self.speed

        # location update

        self.rect.x += self.xspeed
        self.rect.y += self.yspeed

# screen definition

screen_width = 1024
screen_height = 768
screen = pygame.display.set_mode([screen_width, screen_height])

# sprite group definitions

all_sprites_list = pygame.sprite.Group()

# sprite definitions

##player definition

player = Player(BLUE, 100, 100)
all_sprites_list.add(player)
player.rect.x = 472
player.rect.y = 534

# function definitions

# file definitions

pygame.init()

# main code

while not done:
    
    # input code
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                player.W = True
            elif event.key == pygame.K_s:
                player.S = True
            elif event.key == pygame.K_a:
                player.A = True
            elif event.key == pygame.K_d:
                player.D = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                player.W = False
            elif event.key == pygame.K_s:
                player.S = False
            elif event.key == pygame.K_a:
                player.A = False
            elif event.key == pygame.K_d:
                player.D = False

    # sprite updates

    player.update()

    # screen drawing

    screen.fill(BLACK)

    all_sprites_list.draw(screen)

    # screen update

    clock.tick(60)

    pygame.display.flip()

pygame.quit()