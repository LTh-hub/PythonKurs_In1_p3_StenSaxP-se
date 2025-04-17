# ssp.py
#   Version 2
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
import random
import time
import threading
from datetime import datetime


class StenSaxPase:
    def __init__(self, root):
        self.root = root
        self.root.title("Sten-Sax-Påse")
        self.root.geometry("600x400")
        self.spelare_namn = ""
        self.match_grans = 5
        self.choices = ["Sten", "Sax", "Påse"]
        self.spelare_val = tk.StringVar(value="Sten")
        self.computer_score = 0
        self.player_score = 0
        self.antal_for_match = tk.StringVar(value="Först till 5")
        self.resultat_text = ""
        self.computer_choice = ""
        self.fundering_pa = False
        self.create_start_view()


    def create_start_view(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        ttk.Label(self.root, text="Ange namn på spelare:").pack(pady=10)
        self.name_entry = ttk.Entry(self.root)
        self.name_entry.pack(pady=5)

        ttk.Label(self.root, text="Antal vunna 'del-game' för vinst av 'match'?").pack(pady=10)
        self.dropdown = ttk.Combobox(self.root, 
                                     values=["Först till 3", "Först till 5", "Först till 10"], 
                                     textvariable=self.antal_for_match)
        self.dropdown.current(1)
        self.dropdown.pack(pady=5)

        start_button = ttk.Button(self.root, text="Börja spela", command=self.start_game)
        start_button.pack(pady=20)


    def start_game(self):
        self.spelare_namn = self.name_entry.get() or "Spelare"
        self.match_grans = int(self.antal_for_match.get().split()[-1])
        self.computer_score = 0
        self.player_score = 0
        self.spelare_val.set("Sten")
        self.resultat_text = ""
        self.build_game_view()
        threading.Thread(target=self.computer_thinking_phase).start()


    def build_game_view(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.configure(bg="#e6f2ff")

        self.status_label = ttk.Label(self.root, text="Datorn funderar")
        self.status_label.pack(pady=10)

        self.card_label = ttk.Label(self.root, text="❓", font=("Helvetica", 32))
        self.card_label.pack()

        self.radio_frame = ttk.Frame(self.root)
        self.radio_frame.pack(pady=10)

        for val in self.choices:
            ttk.Radiobutton(self.radio_frame, text=val, variable=self.spelare_val, value=val).pack(side=tk.LEFT, padx=5)

        self.button_frame = ttk.Frame(self.root)
        self.button_frame.pack(pady=10)

        self.visa_button = ttk.Button(self.button_frame, text="Visa ditt val", command=self.reveal_choice, state=tk.DISABLED)
        self.visa_button.pack(side=tk.LEFT, padx=5)

        self.spela_button = ttk.Button(self.button_frame, text="Spela ett 'del-game'", command=self.new_round, state=tk.DISABLED)
        self.spela_button.pack(side=tk.LEFT, padx=5)

        self.separator = tk.Frame(self.root, height=2, bg="darkgoldenrod", bd=1, relief=tk.SUNKEN)
        self.separator.pack(fill=tk.X, padx=5, pady=10)

        self.result_label = ttk.Label(self.root, text="")
        self.result_label.pack()

        self.score_frame = ttk.Frame(self.root)
        self.score_frame.pack(pady=10)

        self.computer_score_label = ttk.Label(self.score_frame, text="Computer: 0")
        self.computer_score_label.pack(side=tk.LEFT, padx=20)

        self.player_score_label = ttk.Label(self.score_frame, text=f"{self.spelare_namn}: 0")
        self.player_score_label.pack(side=tk.RIGHT, padx=20)

        self.vinst_info = ttk.Label(self.root, text=f"För att vinna matchen: Först till {self.match_grans}")
        self.vinst_info.pack()


    def computer_thinking_phase(self):
        self.fundering_pa = True
        tid = random.uniform(1, 4)
        slut_tid = time.time() + tid
        while time.time() < slut_tid:
            symbol = random.choice(["🪨", "✂️", "📄"])
            self.card_label.config(text=symbol)
            time.sleep(1/3)
        self.computer_choice = random.choice(self.choices)
        self.status_label.config(text="Datorn har gjort sitt val")
        self.visa_button.config(state=tk.NORMAL)
        self.fundering_pa = False


    def reveal_choice(self):
        resultat = self.jamfor_val(self.computer_choice, self.spelare_val.get())
        if resultat == "spelare":
            self.player_score += 1
            self.resultat_text = f"{self.spelare_namn} vann!"
        elif resultat == "dator":
            self.computer_score += 1
            self.resultat_text = "Computer vann!"
        else:
            self.resultat_text = "Det blev oavgjort!"

        self.computer_score_label.config(text=f"Computer: {self.computer_score}")
        self.player_score_label.config(text=f"{self.spelare_namn}: {self.player_score}")
        self.result_label.config(text=self.resultat_text)

        self.visa_button.config(state=tk.DISABLED)
        if self.computer_score >= self.match_grans or self.player_score >= self.match_grans:
            self.show_end_screen()
        else:
            self.spela_button.config(state=tk.NORMAL)


    def new_round(self):
        self.spelare_val.set("Sten")
        self.result_label.config(text="")
        self.status_label.config(text="Datorn funderar")
        self.spela_button.config(state=tk.DISABLED)
        threading.Thread(target=self.computer_thinking_phase).start()


    def jamfor_val(self, dator, spelare):
        if dator == spelare:
            return "oavgjort"
        elif (dator == "Sten" and spelare == "Sax") or \
             (dator == "Sax" and spelare == "Påse") or \
             (dator == "Påse" and spelare == "Sten"):
            return "dator"
        else:
            return "spelare"


    def show_end_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.configure(bg="#e6f2ff")

        if self.player_score > self.computer_score:
            text = f"Grattis {self.spelare_namn}! Du vann matchen med {self.player_score} vunna del-game."
        else:
            text = f"Tyvärr {self.spelare_namn}, datorn vann matchen med {self.computer_score} vunna del-game."

        ttk.Label(self.root, text=text, wraplength=500).pack(pady=20)

        knapp_frame = ttk.Frame(self.root)
        knapp_frame.pack(pady=20)

        ttk.Button(knapp_frame, text="Spara resultat", command=self.spara_resultat).pack(side=tk.LEFT, padx=5)
        ttk.Button(knapp_frame, text="Spela en gång till", command=self.create_start_view).pack(side=tk.LEFT, padx=5)
        ttk.Button(knapp_frame, text="Exit", command=self.root.destroy).pack(side=tk.LEFT, padx=5)


    def spara_resultat(self):
        with open("ssp_resultat.txt", "a") as fil:
            fil.write(f"{datetime.now()} - {self.spelare_namn} {self.player_score}:{self.computer_score}\n")




if __name__ == "__main__":
    root = tk.Tk()
    app = StenSaxPase(root)
    root.mainloop()






#
# git status (frivilligt)
# git add .
# git commit  -m"TxT messages i rubrikhuvudet på GitHub"
# git push

