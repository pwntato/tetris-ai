import pygame

def empty_square(surface, color, x, y, width, height):
  pygame.draw.rect(surface, color, pygame.Rect(x, y, width, height), 1)

def full_square(surface, color, x, y, width, height):
  pygame.draw.rect(surface, color, pygame.Rect(x, y, width, height))
  