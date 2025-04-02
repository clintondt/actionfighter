import pygame
import math
import random
import time
from collections import deque

map_graph = {

    # 1 to x
    
    "1m": ["1ml", "1mr", "1m2lr"],
    "1r": ["1rm", "1r2lr"],
    "1l": ["1lm", "1l2lr"],
    "1ml": ["1l"],
    "1mr": ["1r"],
    "1lm": ["1m", "1mr"],
    "1rm": ["1m", "1ml"],
    "1m2lr": ["2lr"],
    "1l2lr": ["2lr"],
    "1r2lr": ["2lr"],


    # 2 to x

    "2lr": ["2lr1l", "2lr1r", "2lr1m"],
    "2lr1l": ["1l"],
    "2lr1r": ["1r"],
    "2lr1m": ["1m"],

}

road_images = {

    "1m": "sprites/roads/1m.png",
    "1l": "sprites/roads/1l.png", 
    "1r": "sprites/roads/1r.png",
    "1ml": "sprites/roads/1ml.png",
    "1mr": "sprites/roads/1mr.png",
    "1lm": "sprites/roads/1lm.png",
    "1rm": "sprites/roads/1rm.png",
    "2lr": "sprites/roads/2lr.png",
    "1m2lr": "sprites/roads/1m2lr.png",
    "2lr1m": "sprites/roads/2lr1m.png",
    "2lr1l": "sprites/roads/2lr1l.png",
    "2lr1r": "sprites/roads/2lr1r.png",
    "1l2lr": "sprites/roads/1l2lr.png",
    "1r2lr": "sprites/roads/1r2lr.png",
}

__all__ = ['road_images']