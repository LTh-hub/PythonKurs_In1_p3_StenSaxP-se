# ssp.py
#   Version 4
#
#   Pythonprogrammering för AI-utveckling
#
#       Inmlämningsuppgift 1    -   22-april-2025
#
#   Projekt 3: Sten-Sax-Påse
#       Skapa en version av spelet sten-sax-påse. Datorn
#       slumpar vilken av sten, sax eller påse den ska välja.
#       Spelaren väljer också sten, sax eller påse. Datorn
#       och spelaren visar sedan upp sina val samtidigt.
#
#       Regler enligt följande:
#           - sten vinner över sax
#           - sax vinner över påse 
#           - påse vinner över sten
#           - oavgjort om båda väljer samma alternativ
#
#   Spelaren spelar tills hen vinner eller förlorar mot datorn.
#
#
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import random
import time
from datetime import datetime
import threading
import os




class StenSaxPåse:
    def __init__(self, root):
        self.root = root
        self.root.title("Sten-Sax-Påse")
        self.root.geometry("500x600")
        self.player_score = 0
        self.computer_score = 0
        self.match_target = 5
        self.choices = ["Sten", "Sax", "Påse"]
        self.game_running = False

        self.create_start_screen()


    def create_start_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.configure(bg="SystemButtonFace")

        tk.Label(self.root, text="Ange namn på spelare").pack(pady=10)
        self.name_entry = tk.Entry(self.root)
        self.name_entry.pack()

        tk.Label(self.root, text="Ange antal vunna 'del-game' för vinst av 'match'?").pack(pady=10)
        self.match_var = tk.StringVar(value="Först till 5")
        ttk.Combobox(self.root, textvariable=self.match_var, values=["Först till 3", "Först till 5", "Först till 10", "Först till 1"]).pack()

        tk.Button(self.root, text="Börja spela", command=self.start_game).pack(pady=20)

        # Horisontell mörkgrå linje
        tk.Frame(self.root, height=2, bd=1, relief=tk.SUNKEN, bg="gray").pack(fill=tk.X, pady=10)

        # Visa regler och information från fil
        try:
            with open("ssp_rules_front.txt", "r", encoding="utf-8") as f:
                rules = f.read()
            tk.Label(self.root, text="Sten-Sax-Påse", font=("Arial", 14, "bold"), anchor="center").pack()
            tk.Label(self.root, text=rules, justify=tk.LEFT).pack(pady=10)
        except FileNotFoundError:
            tk.Label(self.root, text="Filen 'ssp_rules_front.txt' saknas.").pack(pady=10)


    def start_game(self):
        self.player_name = self.name_entry.get()
        self.player_score = 0
        self.computer_score = 0
        self.match_target = int(self.match_var.get().split()[-1])

        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.configure(bg="#e0f7ff")

        self.status_label = tk.Label(self.root, text="Datorn funderar", bg="#e0f7ff")
        self.status_label.pack(pady=10)

        self.icon_label = tk.Label(self.root, text="❔", font=("Arial", 32), bg="#e0f7ff")
        self.icon_label.pack()

        self.computer_choice = None
        self.computer_done = False

        threading.Thread(target=self.simulate_computer_thinking).start()

        self.player_choice_var = tk.StringVar(value="Sten")
        self.radio_frame = tk.Frame(self.root, bg="#e0f7ff")
        self.radio_frame.pack(pady=10)

        for choice in self.choices:
            tk.Radiobutton(self.radio_frame, text=choice, variable=self.player_choice_var, value=choice, bg="#e0f7ff").pack(side=tk.LEFT, padx=10)

        self.button_frame = tk.Frame(self.root, bg="#e0f7ff")
        self.button_frame.pack(pady=10)

        self.reveal_button = tk.Button(self.button_frame, text="Jämför bådas val", state=tk.DISABLED, command=self.reveal_choices)
        self.reveal_button.pack(side=tk.LEFT, padx=10)

        self.play_button = tk.Button(self.button_frame, text="Spela nytt 'del-game'", state=tk.DISABLED, command=self.play_round)
        self.play_button.pack(side=tk.LEFT, padx=10)

        # Första horisontella gul linje
        tk.Frame(self.root, height=2, bd=1, relief=tk.SUNKEN, bg="gold").pack(fill=tk.X, pady=10)

        self.result_label = tk.Label(self.root, text="", bg="#e0f7ff")
        self.result_label.pack()

        self.score_frame = tk.Frame(self.root, bg="#e0f7ff")
        self.score_frame.pack(pady=10)

        self.comp_score_label = tk.Label(self.score_frame, text=f"Computer: {self.computer_score}", bg="#e0f7ff")
        self.comp_score_label.grid(row=0, column=0, padx=50)

        self.player_score_label = tk.Label(self.score_frame, text=f"{self.player_name}: {self.player_score}", bg="#e0f7ff")
        self.player_score_label.grid(row=0, column=1, padx=50)

        self.target_label = tk.Label(self.root, text=f"För att vinna matchen: Först till {self.match_target}", bg="#e0f7ff")
        self.target_label.pack()

        # Andra horisontella gul linje
        tk.Frame(self.root, height=2, bd=1, relief=tk.SUNKEN, bg="gold").pack(fill=tk.X, pady=10)

        # Visa spelregler under
        try:
            with open("ssp_rules_mid.txt", "r", encoding="utf-8") as f:
                mid_rules = f.read()
            tk.Label(self.root, text=mid_rules, justify=tk.LEFT, bg="#e0f7ff").pack(pady=10)
        except FileNotFoundError:
            tk.Label(self.root, text="Filen 'ssp_rules_mid.txt' saknas.", bg="#e0f7ff").pack(pady=10)


    def simulate_computer_thinking(self):
        duration = random.uniform(1, 4)
        start_time = time.time()

        def update_icon():
            if time.time() - start_time < duration:
                symbol = random.choice(["🪨", "✂️", "📄"])
                self.icon_label.config(text=symbol)
                self.root.after(330, update_icon)
            else:
                self.computer_choice = random.choice(self.choices)
                self.status_label.config(text="Datorn har gjort sitt val")
                self.reveal_button.config(state=tk.NORMAL)
                self.computer_done = True

        self.root.after(0, update_icon)


    def reveal_choices(self):
        if not self.computer_done:
            return

        player_choice = self.player_choice_var.get()
        computer_choice = self.computer_choice

        self.icon_label.config(text=self.get_icon(computer_choice))  # Visa datorns val

        result = self.determine_winner(player_choice, computer_choice)
        if result == "Player":
            self.player_score += 1
        elif result == "Computer":
            self.computer_score += 1

        self.result_label.config(text=f"Senaste del-game: {result if result != 'Draw' else 'Oavgjord'}")
        self.comp_score_label.config(text=f"Computer: {self.computer_score}")
        self.player_score_label.config(text=f"{self.player_name}: {self.player_score}")

        if self.player_score >= self.match_target or self.computer_score >= self.match_target:
            self.show_match_result()
        else:
            self.play_button.config(state=tk.NORMAL)


    def get_icon(self, val):
        return {"Sten": "🪨", "Sax": "✂️", "Påse": "📄"}.get(val, "❔")


    def determine_winner(self, player, computer):
        if player == computer:
            return "Draw"
        if (player == "Sten" and computer == "Sax") or \
           (player == "Sax" and computer == "Påse") or \
           (player == "Påse" and computer == "Sten"):
            return "Player"
        else:
            return "Computer"


    def play_round(self):
        self.computer_done = False
        self.reveal_button.config(state=tk.DISABLED)
        self.play_button.config(state=tk.DISABLED)
        self.status_label.config(text="Datorn funderar")
        self.icon_label.config(text="❔")
        self.result_label.config(text="")
        threading.Thread(target=self.simulate_computer_thinking).start()


    def show_match_result(self):
        for widget in self.root.winfo_children():
            if widget.winfo_y() < self.result_label.winfo_y():
                widget.destroy()

        winner = self.player_name if self.player_score > self.computer_score else "Datorn"
        if winner == self.player_name:
            message = f"Grattis {self.player_name}, du vann matchen med {self.player_score} - {self.computer_score}!"
        else:
            message = f"Tyvärr, du förlorade. Datorn vann med {self.computer_score} - {self.player_score}."

        tk.Label(self.root, text=message, bg="#e0f7ff", font=("Arial", 12)).pack(pady=10)

        self.save_button = tk.Button(self.root, text="Spara resultat", command=self.save_result)
        self.save_button.pack(pady=5)

        self.replay_button = tk.Button(self.root, text="Spela en gång till", command=self.create_start_screen)
        self.replay_button.pack(pady=5)

        self.exit_button = tk.Button(self.root, text="Exit", command=self.root.quit)
        self.exit_button.pack(pady=5)


    def save_result(self):
        filename = "ssp_resultat.txt"
        visa_dt = str(datetime.now())
        with open(filename, "a", encoding="utf-8") as file:
            file.write(f"{visa_dt[:19]} >>> {self.player_name} {self.player_score}  -  Computer {self.computer_score}\n")
        messagebox.showinfo("Sparat", f"Resultatet sparades i {filename}")




if __name__ == "__main__":
    root = tk.Tk()
    app = StenSaxPåse(root)
    root.mainloop()






#
# git status (frivilligt)
# git add .
# git commit  -m"TxT messages i rubrikhuvudet på GitHub"
# git push

