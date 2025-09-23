import sqlite3
from datetime import datetime
import tkinter as tk
from tkinter import simpledialog
import sys
from pathlib import Path
from .config import DB_FILE

class HighscoreManager:
    def __init__(self, db_file: Path = DB_FILE):
        self.db_file = str(db_file)
        self._ensure_table()

    def _conn(self):
        return sqlite3.connect(self.db_file)

    def _ensure_table(self):
        conn = self._conn()
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
        conn.close()

    def add_if_highscore(self, score: int):
        if score <= 0:
            return False
        conn = self._conn()
        c = conn.cursor()
        c.execute('SELECT MAX(score) FROM highscores')
        row = c.fetchone()
        max_score = row[0] if row and row[0] is not None else 0

        if score >= max_score:
            name = self._ask_name()
            date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            c.execute('INSERT INTO highscores (name, score, date) VALUES (?, ?, ?)', (name, score, date))
            conn.commit()
            conn.close()
            return True

        conn.close()
        return False

    def get_highscores(self, limit=10):
        conn = self._conn()
        c = conn.cursor()
        c.execute('SELECT name, score FROM highscores ORDER BY score DESC LIMIT ?', (limit,))
        rows = c.fetchall()
        conn.close()
        return rows

    def _ask_name(self):
        root = tk.Tk()
        root.withdraw()
        name = None
        while not name or name.strip() == "":
            name = simpledialog.askstring("New Highscore!", "Type your name:")
            if name is None:
                root.destroy()
                sys.exit()
            name = name.strip()
        root.destroy()
        return name
