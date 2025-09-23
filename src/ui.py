# src/ui.py
import pygame
from .config import FONT_SIZE

pygame.font.init()
_default_font = pygame.font.SysFont(None, FONT_SIZE)

def draw_text(surface, text, pos, color=(255,255,255), font=None):
    font = font or _default_font
    surf = font.render(str(text), True, color)
    rect = surf.get_rect(topleft=pos)
    surface.blit(surf, rect)
    return rect

def draw_button(surface, rect, text, font=None, color=(255,255,255)):
    pygame.draw.rect(surface, color, rect, 2)
    font = font or _default_font
    text_surf = font.render(text, True, color)
    surface.blit(text_surf, text_surf.get_rect(center=rect.center))
