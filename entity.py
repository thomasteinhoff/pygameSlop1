import pygame

class Entity:
    def __init__(self, x, y, radius=20):
        self.pos = pygame.Vector2(x, y)
        self.vel = pygame.Vector2(0, 0)
        self.acceleration = 1.5
        self.radius = radius

    def update(self):
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
        direction = (mouse_pos - self.pos)

        if direction.length() > 0:
            direction = direction.normalize()

            if self.vel.length() > 0:
                angle_diff = self.vel.angle_to(direction)
                if abs(angle_diff) > 20:  
                    self.vel -= self.vel.normalize() * self.acceleration

            self.vel += direction * self.acceleration

        self.pos += self.vel

    def draw(self, tela):
        pygame.draw.circle(tela, (255, 255, 255), (int(self.pos.x), int(self.pos.y)), self.radius, 2)
