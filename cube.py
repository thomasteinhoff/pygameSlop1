import pygame
import random

class Cube:
    SIZE = 30

    def __init__(self, screen_width, screen_height):
        self.rect = pygame.Rect(
            random.randint(0, screen_width - Cube.SIZE),
            random.randint(0, screen_height - Cube.SIZE),
            Cube.SIZE,
            Cube.SIZE
        )
        self.angle = random.randint(0, 360)
        self.alive = True

        self.original_surf = pygame.Surface((Cube.SIZE, Cube.SIZE), pygame.SRCALPHA)
        pygame.draw.rect(self.original_surf, (255, 255, 255), (0, 0, Cube.SIZE, Cube.SIZE), 2)

    def draw(self, tela):
        rotated_surf = pygame.transform.rotate(self.original_surf, self.angle)
        rotated_rect = rotated_surf.get_rect(center=self.rect.center)
        tela.blit(rotated_surf, rotated_rect)

    def check_click(self, mouse_pos):
        extended_rect = self.rect.inflate(Cube.SIZE, Cube.SIZE)
        if extended_rect.collidepoint(mouse_pos):
            self.alive = False


class CubeManager:
    def __init__(self, screen_width, screen_height):
        self.cubes = []
        self.max_cubes = 5
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.spawn_timer = 0
        self.next_spawn = random.randint(500, 1000)

    def update(self):
        now = pygame.time.get_ticks()

        if len(self.cubes) < self.max_cubes and now - self.spawn_timer > self.next_spawn:
            self.cubes.append(Cube(self.screen_width, self.screen_height))
            self.spawn_timer = now
            self.next_spawn = random.randint(500, 1000)

        self.cubes = [c for c in self.cubes if c.alive]

    def draw(self, tela):
        for cube in self.cubes:
            cube.draw(tela)

    def handle_click(self, mouse_pos):
        for cube in self.cubes:
            cube.check_click(mouse_pos)
