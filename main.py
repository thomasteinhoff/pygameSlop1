import pygame, sqlite3, random, sys
from entity import Entity
from cube import CubeManager
from datetime import datetime
import tkinter as tk
from tkinter import simpledialog

WIDTH, HEIGHT = 800, 600
DB_FILE = "hscore.sql"

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.event.set_grab(True) 
pygame.display.set_caption("Pygame Slop")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)


def check_highscore(current_score):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS highscores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            score INTEGER NOT NULL,
            date TEXT NOT NULL
        )
    ''')
    conn.commit()

    c.execute('SELECT MAX(score) FROM highscores')
    row = c.fetchone()
    max_score = row[0] if row[0] is not None else 0

    if current_score > 0 and current_score >= max_score:
        name = get_player_name()
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        c.execute('INSERT INTO highscores (name, score, date) VALUES (?, ?, ?)',
                  (name, current_score, date))
        conn.commit()

    conn.close()

def get_player_name():
    root = tk.Tk()
    root.withdraw()
    name = None
    while not name or name.strip() == "":
        name = simpledialog.askstring("Novo Highscore!", "Digite seu nome:")
        if name is None:
            sys.exit()
        name = name.strip()
    root.destroy()
    return name

def get_highscores(limit=10):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT name, score FROM highscores ORDER BY score DESC LIMIT ?', (limit,))
    rows = c.fetchall()
    conn.close()
    return rows


def spawn_entity_offscreen():
    side = random.choice(["left", "right", "top", "bottom"])
    if side == "left":
        x = -50
        y = random.randint(0, HEIGHT)
    elif side == "right":
        x = WIDTH + 50
        y = random.randint(0, HEIGHT)
    elif side == "top":
        x = random.randint(0, WIDTH)
        y = -50
    else:  # bottom
        x = random.randint(0, WIDTH)
        y = HEIGHT + 50
    return Entity(x, y)

def game_loop():
    entity = spawn_entity_offscreen()
    cubes = CubeManager(WIDTH, HEIGHT)

    score = 0
    last_time = pygame.time.get_ticks()
    running = True
    game_over = False
    highscores = []

    while running:
        now = pygame.time.get_ticks()
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if not game_over:
                    cubes.handle_click(event.pos)
                    dead_count = len([c for c in cubes.cubes if not c.alive])
                    score += dead_count * 350
                else:
                    if replay_button.collidepoint(event.pos):
                        game_loop()
                        return
                    if quit_button.collidepoint(event.pos):
                        running = False

        if not game_over:
            if now - last_time >= 1000:
                score += 100
                last_time = now

            entity.update()
            cubes.update()

            if entity.pos.distance_to(mouse_pos) <= entity.radius:
                game_over = True
                check_highscore(score)
                highscores = get_highscores()

        screen.fill((0, 0, 0))
        entity.draw(screen)
        cubes.draw(screen)

        score_surf = font.render(str(score), True, (255, 255, 255))
        score_rect = score_surf.get_rect(topright=(WIDTH - 20, 20))
        screen.blit(score_surf, score_rect)

        if game_over:
            y_offset = 20
            for hs_name, hs_score in highscores:
                hs_text = f"{hs_name}: {hs_score}"
                hs_surf = font.render(hs_text, True, (255, 255, 255))
                screen.blit(hs_surf, (20, y_offset))
                y_offset += 36

            go_surf = font.render("GAME OVER", True, (255, 0, 0))
            go_rect = go_surf.get_rect(center=(WIDTH//2, HEIGHT//2 - 50))
            screen.blit(go_surf, go_rect)

            replay_button = pygame.Rect(WIDTH//2 - 100, HEIGHT//2, 200, 50)
            quit_button = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 + 70, 200, 50)

            pygame.draw.rect(screen, (255, 255, 255), replay_button, 2)
            pygame.draw.rect(screen, (255, 255, 255), quit_button, 2)

            replay_text = font.render("Play Again", True, (255, 255, 255))
            quit_text = font.render("Exit", True, (255, 255, 255))

            screen.blit(replay_text, replay_text.get_rect(center=replay_button.center))
            screen.blit(quit_text, quit_text.get_rect(center=quit_button.center))

        pygame.display.flip()
        clock.tick(60)

game_loop()
pygame.quit()
