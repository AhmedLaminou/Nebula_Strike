import tkinter as tk
from tkinter import colorchooser, messagebox
import subprocess
import os

class ConfigMenu:
    def __init__(self, root):
        self.root = root
        self.root.title("Pixel Painter Battle - Menu")
        self.color1 = '#ff5050'
        self.color2 = '#5078ff'
        self.size = tk.IntVar(value=20)
        tk.Label(root, text="Taille de la grille :").pack()
        tk.Scale(root, from_=10, to=40, orient='horizontal', variable=self.size).pack()
        tk.Button(root, text="Couleur Joueur 1", command=self.choose_color1).pack()
        tk.Button(root, text="Couleur Joueur 2", command=self.choose_color2).pack()
        tk.Button(root, text="Jouer", command=self.launch_game).pack(pady=10)
        tk.Button(root, text="Scores", command=self.show_scores).pack()
    def choose_color1(self):
        c = colorchooser.askcolor(title="Couleur Joueur 1")
        if c[1]: self.color1 = c[1]
    def choose_color2(self):
        c = colorchooser.askcolor(title="Couleur Joueur 2")
        if c[1]: self.color2 = c[1]
    def launch_game(self):
        # Pour la démo, lance main.py sans passer les paramètres
        subprocess.Popen(['python', 'main.py'], cwd=os.path.dirname(__file__))
        self.root.destroy()
    def show_scores(self):
        messagebox.showinfo("Scores", "Fonction à implémenter !")

if __name__ == "__main__":
    root = tk.Tk()
    app = ConfigMenu(root)
    root.mainloop()
