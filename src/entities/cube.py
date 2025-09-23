# src/entities/cube.py
import pygame
import random
from ..config import CUBE_SIZE

class Cube:
    SIZE = CUBE_SIZE

    def __init__(self, screen_width, screen_height):
        
        x = random.randint(0, screen_width - Cube.SIZE)
        y = random.randint(0, screen_height - Cube.SIZE)
        self.rect = pygame.Rect(x, y, Cube.SIZE, Cube.SIZE)
        self.angle = random.randint(0, 360)
        self.alive = True

        self.original_surf = pygame.Surface((Cube.SIZE, Cube.SIZE), pygame.SRCALPHA)
        pygame.draw.rect(self.original_surf, (255, 255, 255), (0, 0, Cube.SIZE, Cube.SIZE), 2)

        self.hitbox = self.rect.inflate(Cube.SIZE, Cube.SIZE)

    def draw(self, surface):
        rotated = pygame.transform.rotate(self.original_surf, self.angle)
        rotated_rect = rotated.get_rect(center=self.rect.center)
        surface.blit(rotated, rotated_rect)

    def check_click(self, mouse_pos):
        """Return True if clicked (and mark dead)."""
        if self.hitbox.collidepoint(mouse_pos):
            self.alive = False
            return True
        return False


class CubeManager:
    def __init__(self, screen_width, screen_height, max_cubes=5):
        self.cubes = []
        self.max_cubes = max_cubes
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.spawn_timer = pygame.time.get_ticks()
        self.next_spawn = random.randint(500, 1000)

    def update(self):
        now = pygame.time.get_ticks()
        
        if len(self.cubes) < self.max_cubes and now - self.spawn_timer > self.next_spawn:
            self.cubes.append(Cube(self.screen_width, self.screen_height))
            self.spawn_timer = now
            self.next_spawn = random.randint(500, 1000)

        self.cubes = [c for c in self.cubes if c.alive]

    def draw(self, surface):
        for c in self.cubes:
            c.draw(surface)

    def handle_click(self, mouse_pos):
        """Return number of cubes killed by this click."""
        killed = 0
        for c in self.cubes:
            if c.check_click(mouse_pos):
                killed += 1
        return killed
