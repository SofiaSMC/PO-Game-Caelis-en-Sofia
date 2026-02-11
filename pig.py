import random
import tkinter as tk
from tkinter import messagebox

BIG_FONT = ("Arial", 20)
BUTTON_FONT = ("Arial", 16)

# ----- Game logic -----
def roll():
    return random.randint(1, 6)

class PigGame:
    def __init__(self, root):
        self.root = root
        self.root.title("PIG: Multi-player Game")
        self.root.geometry("550x400")
        self.root.tk.call('tk', 'scaling', 1.5)
        
        self.players = 0
        self.player_scores = []
        self.current_score = 0
        self.current_player = 0
        self.max_score = 150
        
        self.setup_players_screen()
        
    def setup_players_screen(self):
        # Clear window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        tk.Label(self.root, text="Enter number of players (2-4):").pack(pady=10)
        self.player_entry = tk.Entry(self.root)
        self.player_entry.pack(pady=5)
        tk.Button(self.root, text="Start Game", command=self.start_game).pack(pady=10)
    
    def start_game(self):
        try:
            players = int(self.player_entry.get())
            if players < 2 or players > 4:
                raise ValueError
            self.players = players
            self.player_scores = [0 for _ in range(players)]
            self.current_player = 0
            self.current_score = 0
            self.game_screen()
        except ValueError:
            messagebox.showerror("Error", "Please enter a number between 2 and 4.")
    
    def game_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        tk.Label(self.root, text=f"Player {self.current_player + 1}'s turn").pack(pady=5)
        tk.Label(self.root, text=f"Total score: {self.player_scores[self.current_player]}").pack(pady=5)
        self.turn_score_label = tk.Label(self.root, text=f"Current turn score: {self.current_score}")
        self.turn_score_label.pack(pady=5)
        
        tk.Button(self.root, text="Roll", command=self.roll_dice).pack(pady=5)
        tk.Button(self.root, text="Hold", command=self.hold).pack(pady=5)
    
    def roll_dice(self):
        value = roll()
        if value == 1:
            messagebox.showinfo("Rolled 1", "You rolled a 1! Turn over, no points added.")
            self.current_score = 0
            self.next_player()
        else:
            self.current_score += value
            self.turn_score_label.config(text=f"Current turn score: {self.current_score}")
            messagebox.showinfo("Rolled Dice", f"You rolled a {value}!")
    
    def hold(self):
        self.player_scores[self.current_player] += self.current_score
        if self.player_scores[self.current_player] >= self.max_score:
            messagebox.showinfo("Game Over", f"Player {self.current_player + 1} wins with {self.player_scores[self.current_player]} points!")
            self.root.destroy()
        else:
            self.current_score = 0
            self.next_player()
    
    def next_player(self):
        self.current_player = (self.current_player + 1) % self.players
        self.game_screen()

# ----- Run the game -----
root = tk.Tk()
game = PigGame(root)
root.mainloop()
