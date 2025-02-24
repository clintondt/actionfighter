# import

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

# screen definition

screen_width = 1024
screen_height = 768
screen = pygame.display.set_mode([screen_width, screen_height])

# sprite group definitions

all_sprites_list = pygame.sprite.Group()

# sprite definitions

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

    # sprite updates

    # screen drawing

    screen.fill(BLACK)

    all_sprites_list.draw(screen)

    # screen update

    clock.tick(5)

    pygame.display.flip()

pygame.quit()