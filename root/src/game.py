import pygame
from .config import WIDTH, HEIGHT, FPS, CUBE_SCORE, CUBE_MAX_COUNT, FONT_SIZE
from .entities.entity import Entity
from .entities.cube import CubeManager
from .ui import draw_text, draw_button
from .highscores import HighscoreManager

class Game:
    def _draw_pointer(self, surface, direction, pos):
        # direction: 'top', 'bottom', 'left', 'right'
        # pos: (x, y) center of triangle base on border
        size = 24
        color = (255, 255, 0)
        if direction == 'top':
            points = [
                (pos[0], 8),
                (pos[0] - size//2, 8 + size),
                (pos[0] + size//2, 8 + size)
            ]
        elif direction == 'bottom':
            points = [
                (pos[0], HEIGHT - 8),
                (pos[0] - size//2, HEIGHT - 8 - size),
                (pos[0] + size//2, HEIGHT - 8 - size)
            ]
        elif direction == 'left':
            points = [
                (8, pos[1]),
                (8 + size, pos[1] - size//2),
                (8 + size, pos[1] + size//2)
            ]
        elif direction == 'right':
            points = [
                (WIDTH - 8, pos[1]),
                (WIDTH - 8 - size, pos[1] - size//2),
                (WIDTH - 8 - size, pos[1] + size//2)
            ]
        pygame.draw.polygon(surface, color, points)
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.event.set_grab(True)
        pygame.display.set_caption("Pygame Slop")
        self.clock = pygame.time.Clock()

        self.font = pygame.font.SysFont(None, FONT_SIZE)

        self.entity = self._spawn_entity_offscreen()
        self.cubes = CubeManager(WIDTH, HEIGHT, max_cubes=CUBE_MAX_COUNT)

        self.score = 0
        self.last_time = pygame.time.get_ticks()
        self.running = True
        self.game_over = False
        self.highscores = []

        self.highscore_mgr = HighscoreManager()

        self.state = "start"
        self.start_button = None
        self.highscores = self.highscore_mgr.get_highscores()

    def _spawn_entity_offscreen(self):
        import random
        side = random.choice(["left", "right", "top", "bottom"])
        if side == "left":
            x, y = -50, random.randint(0, HEIGHT)
        elif side == "right":
            x, y = WIDTH + 50, random.randint(0, HEIGHT)
        elif side == "top":
            x, y = random.randint(0, WIDTH), -50
        else:
            x, y = random.randint(0, WIDTH), HEIGHT + 50
        return Entity(x, y)

    def run(self):
        while self.running:
            self._handle_events()
            if self.state == "playing" and not self.game_over:
                self._update()
            self._draw()
            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.state == "start":
                    if self.start_button and self.start_button.collidepoint(event.pos):
                        self.state = "playing"
                        self.score = 0
                        self.last_time = pygame.time.get_ticks()
                        self.entity = self._spawn_entity_offscreen()
                        self.cubes = CubeManager(WIDTH, HEIGHT, max_cubes=CUBE_MAX_COUNT)
                        self.game_over = False
                        pygame.event.set_grab(True)
                elif self.state == "playing":
                    if not self.game_over:
                        killed = self.cubes.handle_click(event.pos)
                        if killed:
                            self.score += killed * CUBE_SCORE
                elif self.state == "game_over" or self.game_over:
                    if hasattr(self, "replay_button") and self.replay_button.collidepoint(event.pos):
                        self.state = "playing"
                        self.score = 0
                        self.last_time = pygame.time.get_ticks()
                        self.entity = self._spawn_entity_offscreen()
                        self.cubes = CubeManager(WIDTH, HEIGHT, max_cubes=CUBE_MAX_COUNT)
                        self.game_over = False
                        pygame.event.set_grab(True)
                    if hasattr(self, "quit_button") and self.quit_button.collidepoint(event.pos):
                        self.running = False

    def _update(self):
        now = pygame.time.get_ticks()
        if now - self.last_time >= 1000:
            self.score += 100
            self.last_time = now

        self.entity.update()
        self.cubes.update()

        if self.entity.pos.distance_to(pygame.mouse.get_pos()) <= self.entity.radius:
            self.game_over = True
            self.state = "game_over"
            self.highscore_mgr.add_if_highscore(self.score)
            self.highscores = self.highscore_mgr.get_highscores()

    def _draw(self):
        self.screen.fill((0, 0, 0))

        if self.state == "start":
            y_offset = 20
            draw_text(self.screen, "High Scores:", (20, y_offset), font=self.font)
            y_offset += 40
            for name, sc in self.highscores:
                text = f"{name}: {sc}"
                draw_text(self.screen, text, (20, y_offset), font=self.font)
                y_offset += 36

            from pygame import Rect
            self.start_button = Rect(WIDTH//2 - 100, HEIGHT//2, 200, 50)
            draw_button(self.screen, self.start_button, "Start", font=self.font)

        elif self.state == "playing":
            self.entity.draw(self.screen)
            self.cubes.draw(self.screen)

            ex, ey = self.entity.pos.x, self.entity.pos.y
            pointer_drawn = False
            if ex < 0:
                y = min(max(ey, 20), HEIGHT - 20)
                self._draw_pointer(self.screen, 'left', (0, y))
                pointer_drawn = True
            if ex > WIDTH:
                y = min(max(ey, 20), HEIGHT - 20)
                self._draw_pointer(self.screen, 'right', (WIDTH, y))
                pointer_drawn = True
            if ey < 0:
                x = min(max(ex, 20), WIDTH - 20)
                self._draw_pointer(self.screen, 'top', (x, 0))
                pointer_drawn = True
            if ey > HEIGHT:
                x = min(max(ex, 20), WIDTH - 20)
                self._draw_pointer(self.screen, 'bottom', (x, HEIGHT))
                pointer_drawn = True

            score_surf = self.font.render(str(self.score), True, (255, 255, 255))
            score_rect = score_surf.get_rect(topright=(WIDTH - 20, 20))
            self.screen.blit(score_surf, score_rect)

            if self.game_over:
                pygame.event.set_grab(False)
                y_offset = 20
                for name, sc in self.highscores:
                    text = f"{name}: {sc}"
                    draw_text(self.screen, text, (20, y_offset), font=self.font)
                    y_offset += 36

                go_surf = self.font.render("GAME OVER", True, (255, 0, 0))
                go_rect = go_surf.get_rect(center=(WIDTH//2, HEIGHT//2 - 50))
                self.screen.blit(go_surf, go_rect)

                # buttons
                from pygame import Rect
                self.replay_button = Rect(WIDTH//2 - 100, HEIGHT//2, 200, 50)
                self.quit_button = Rect(WIDTH//2 - 100, HEIGHT//2 + 70, 200, 50)

                draw_button(self.screen, self.replay_button, "Play Again", font=self.font)
                draw_button(self.screen, self.quit_button, "Exit", font=self.font)

        elif self.state == "game_over":
            pygame.event.set_grab(False)
            y_offset = 20
            for name, sc in self.highscores:
                text = f"{name}: {sc}"
                draw_text(self.screen, text, (20, y_offset), font=self.font)
                y_offset += 36

            go_surf = self.font.render("GAME OVER", True, (255, 0, 0))
            go_rect = go_surf.get_rect(center=(WIDTH//2, HEIGHT//2 - 50))
            self.screen.blit(go_surf, go_rect)

            # buttons
            from pygame import Rect
            self.replay_button = Rect(WIDTH//2 - 100, HEIGHT//2, 200, 50)
            self.quit_button = Rect(WIDTH//2 - 100, HEIGHT//2 + 70, 200, 50)

            draw_button(self.screen, self.replay_button, "Play Again", font=self.font)
            draw_button(self.screen, self.quit_button, "Exit", font=self.font)
