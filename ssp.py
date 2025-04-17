# ssp.py
#
#   Pythonproframmering för AI-utveckling
#
#       Inmlämningsuppgift 1
#
#   Projekt 3: Sten-sax-påse
#       Skapa en version av spelet sten-sax-påse.
#       Datorn slumpar vilken av sten, sax eller påse den ska välja.
#       Spelaren väljer också sten, sax eller påse.
#       Datorn och spelaren visar sedan upp sina val samtidigt.
#
#       Reglerna är enligt följande:
#           - sten vinner över sax
#           - sax vinner över påse 
#           - påse vinner över sten
#           - oavgjort om båda väljer samma alternativ
#
#   Spelaren spelar tills hen vinner eller förlorar mot datorn.
#
#
import tkinter as tk
from tkinter import ttk, messagebox
from random import choice, randint
from datetime import datetime


class SSPGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Sten Sax Påse")
        self.player_name = ""
        self.target_score = 5
        self.player_score = 0
        self.computer_score = 0
        self.choices = ["Sten", "Sax", "Påse"]
        self.computer_choice = ""
        self.result_history = []
        self.game_frame = None
        self.del_game_result_label = None
        self.score_labels = {}
        self.target_text = ""
        self.init_start_screen()


    def init_start_screen(self):
        self.clear_root()
        frame = tk.Frame(self.root)
        frame.pack(padx=10, pady=10)

        tk.Label(frame, text="Ange namn på spelare").pack()
        self.name_entry = tk.Entry(frame)
        self.name_entry.pack()

        tk.Label(frame, text="Antal vunna 'del-game' för vinst av 'match'?").pack(pady=(10, 0))
        self.target_var = tk.StringVar(value="Först till 5")
        dropdown = ttk.Combobox(
            frame, textvariable=self.target_var, values=["Först till 3", "Först till 5", "Först till 10"],
            state="readonly")
        dropdown.pack()

        start_button = tk.Button(frame, text="Börja spela", command=self.start_game)
        start_button.pack(pady=10)


    def start_game(self):
        self.player_name = self.name_entry.get().strip() or "Spelare"
        self.target_score = int(self.target_var.get().split()[-1])
        self.player_score = 0
        self.computer_score = 0
        self.result_history.clear()
        self.target_text = self.target_var.get()
        self.init_game_screen()








if __name__ == "__main__":
    root.mainloop()








# git status (frivilligt)
# git add .
# git commit  -m"Added new code for mongo"
# git push

