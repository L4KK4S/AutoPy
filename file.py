import tkinter as tk
from tkinter import filedialog

file = "."

def file_choice():
    global file
    file = filedialog.askopenfilename()
    if file:
        label.configure(text="Fichier sélectionné : " + file)
        validation_btn.config(state=tk.NORMAL)
    else:
        label.configure(text="Aucun fichier sélectionné.")
        validation_btn.config(state=tk.DISABLED)

def finish():
    root.destroy()

root = tk.Tk()
root.title("Sélection du fichier de l'automate")


file_selection_btn = tk.Button(root, text="Sélectionner un fichier", command=file_choice)
file_selection_btn.pack(pady=20)

label = tk.Label(root, text="")
label.pack()

# Bouton de validation
validation_btn = tk.Button(root, text="Valider et Quitter", command=finish, state=tk.DISABLED)
validation_btn.pack(pady=10)

if __name__ == "__main__":
    root.mainloop()
