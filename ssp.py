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


    def init_game_screen(self):
        self.clear_root()
        self.root.configure(bg="#e6f2ff")
        self.computer_thinking_label = tk.Label(self.root, text="Datorn funderar", bg="#e6f2ff", font=("Arial", 12))
        self.computer_thinking_label.pack(pady=5)

        self.computer_animation_label = tk.Label(self.root, text="", font=("Arial", 18), bg="#e6f2ff")
        self.computer_animation_label.pack()

        self.choice_var = tk.StringVar(value="")
        choice_frame = tk.Frame(self.root, bg="#e6f2ff")
        choice_frame.pack(pady=10)
        for choice in self.choices:
            tk.Radiobutton(choice_frame, text=choice, variable=self.choice_var, value=choice, bg="#e6f2ff").pack(side="left", padx=5)

        self.play_button = tk.Button(self.root, text="Spela ett 'del-game'", state="disabled", command=self.play_round)
        self.play_button.pack(pady=10)

        separator = tk.Frame(self.root, bg="darkgoldenrod", height=2)
        separator.pack(fill="x", pady=5)

        self.del_game_result_label = tk.Label(self.root, text="", bg="#e6f2ff", font=("Arial", 12))
        self.del_game_result_label.pack()

        score_frame = tk.Frame(self.root, bg="#e6f2ff")
        score_frame.pack()

        tk.Label(score_frame, text="Computer", bg="#e6f2ff", font=("Arial", 10, "bold")).grid(row=0, column=0)
        tk.Label(score_frame, text=self.player_name, bg="#e6f2ff", font=("Arial", 10, "bold")).grid(row=0, column=1)
        self.score_labels["Computer"] = tk.Label(score_frame, text="0", bg="#e6f2ff")
        self.score_labels["Computer"].grid(row=1, column=0)
        self.score_labels["Player"] = tk.Label(score_frame, text="0", bg="#e6f2ff")
        self.score_labels["Player"].grid(row=1, column=1)

        tk.Label(self.root, text=f"För att vinna matchen: {self.target_text}", bg="#e6f2ff").pack(pady=(5, 10))

        self.root.after(100, self.start_computer_thinking)


    def start_computer_thinking(self):
        duration = randint(200, 4000)
        end_time = self.root.after(duration, self.finish_computer_thinking)
        self.animate_computer_choice()


    def animate_computer_choice(self):
        symbol = choice(self.choices)
        self.computer_animation_label.config(text=symbol)
        self.animation = self.root.after(200, self.animate_computer_choice)


    def finish_computer_thinking(self):
        if hasattr(self, 'animation'):
            self.root.after_cancel(self.animation)
        self.computer_choice = choice(self.choices)
        self.computer_thinking_label.config(text="Datorn har gjort sitt val")
        self.computer_animation_label.config(text=self.computer_choice)
        self.play_button.config(state="normal")


    def play_round(self):
        player_choice = self.choice_var.get()
        if not player_choice:
            messagebox.showwarning("Välj något", "Du måste välja sten, sax eller påse!")
            return

        winner = self.determine_winner(player_choice, self.computer_choice)
        if winner == "Player":
            self.player_score += 1
            result = self.player_name
        elif winner == "Computer":
            self.computer_score += 1
            result = "Computer"
        else:
            result = "oavgjord"

        self.result_history.append((self.computer_choice, player_choice, result))
        self.del_game_result_label.config(text=f"Vinnare: {result}")
        self.score_labels["Computer"].config(text=str(self.computer_score))
        self.score_labels["Player"].config(text=str(self.player_score))

        if self.player_score >= self.target_score or self.computer_score >= self.target_score:
            self.show_result_screen()
        else:
            self.play_button.config(state="disabled")
            self.computer_thinking_label.config(text="Datorn funderar")
            self.root.after(100, self.start_computer_thinking)


    def determine_winner(self, player, computer):
        if player == computer:
            return "Draw"
        wins = {
            "Sten": "Sax",
            "Sax": "Påse",
            "Påse": "Sten"
        }
        return "Player" if wins[player] == computer else "Computer"


    def show_result_screen(self):
        self.clear_top()
        msg = ""
        winner = self.player_name if self.player_score > self.computer_score else "Computer"
        if winner == self.player_name:
            msg = f"Grattis {self.player_name}! Du vann matchen med {self.player_score} vunna 'del-game'."
        else:
            msg = f"Tyvärr {self.player_name}, datorn vann med {self.computer_score} vunna 'del-game'."

        tk.Label(self.root, text=msg, bg="#e6f2ff", font=("Arial", 12, "bold")).pack(pady=10)

        btn_frame = tk.Frame(self.root, bg="#e6f2ff")
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Spara resultat", command=self.save_result).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Spela en gång till", command=self.init_start_screen).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Exit", command=self.root.quit).pack(side="left", padx=5)


    def save_result(self):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        filename = "ssp_resultat.txt"
        with open(filename, "a", encoding="utf-8") as f:
            f.write("=== STEN-SAX-PÅSE MATCH ===\n")
            f.write(f"Tid: {now}\n")
            f.write(f"Spelare: {self.player_name}\n")
            f.write(f"Match till: {self.target_text}\n")
            for i, (comp, play, res) in enumerate(self.result_history, 1):
                f.write(f"{i}. Dator: {comp} | {self.player_name}: {play} => Vinnare: {res}\n")
            f.write(f"Slutresultat - {self.player_name}: {self.player_score}, Computer: {self.computer_score}\n\n")
        messagebox.showinfo("Resultat sparat", "Matchresultatet har sparats i ssp_resultat.txt")


    def clear_root(self):
        for widget in self.root.winfo_children():
            widget.destroy()


    def clear_top(self):
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Label) or isinstance(widget, tk.Button) or isinstance(widget, tk.Frame):
                widget.destroy()







if __name__ == "__main__":
    root = tk.Tk()
    app = SSPGame(root)
    root.mainloop()








# git status (frivilligt)
# git add .
# git commit  -m"Added new code for mongo"
# git push

