# choosing menu for games
import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
import os
import webbrowser

# Get the absolute path of this file to find the other scripts
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Function to run a game script
def run_game(script_name):
    script_path = os.path.join(BASE_DIR, script_name)
    if not os.path.exists(script_path):
        messagebox.showerror("Error", f"{script_name} not found!")
        return
    # Run the script in a new process
    subprocess.Popen([sys.executable, script_path])

# Create main menu window
root = tk.Tk()
root.title("Game Launcher")
root.geometry("800x800")

tk.Label(root, text="Select a Game", font=("Arial", 18)).pack(pady=20)

tk.Button(root, text="2048", width=20, height=2, command=lambda: run_game("2048.py")).pack(pady=10)
tk.Button(root, text="Pig Game", width=20, height=2, command=lambda: run_game("pig.py")).pack(pady=10)
tk.Button(root, text="Quiz Game", width=20, height=2, command=lambda: run_game("homescreenGameMakenPo.py")).pack(pady=10)
tk.Button(root,text="Film",width=20,height=2,command=lambda: webbrowser.open("https://youtu.be/gAEEYzls4Es")).pack(pady=10)
tk.Button(root, text="Quit", width=20, height=2, command=root.quit).pack(pady=10)

root.mainloop()
