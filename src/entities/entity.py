# src/entities/entity.py
import pygame
from pygame.math import Vector2
from ..config import ENTITY_ACCEL, ENTITY_RADIUS

class Entity:
    def __init__(self, x, y, radius=ENTITY_RADIUS):
        self.pos = Vector2(x, y)
        self.vel = Vector2(0, 0)
        self.acceleration = ENTITY_ACCEL
        self.radius = radius

    def update(self):
        mouse_pos = Vector2(pygame.mouse.get_pos())
        direction = mouse_pos - self.pos
        if direction.length_squared() == 0:
            return

        direction = direction.normalize()

        self.vel += direction * self.acceleration

        if self.vel.length() > 0:
            angle_diff = self.vel.angle_to(direction)
            if abs(angle_diff) > 90:
                self.vel *= 0.8

        self.pos += self.vel

    def draw(self, surface):
        pygame.draw.circle(surface, (255, 255, 255), (int(self.pos.x), int(self.pos.y)), self.radius, 2)
