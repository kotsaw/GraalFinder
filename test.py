import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

def run_action1():
    root.bind("<Button-1>", get_mouse_position_action1)

def get_mouse_position_action1(event):
    x, y = event.x, event.y
    label1.config(text=f"X: {x}")
    label2.config(text=f"Y: {y}")
    check_labels()
    root.unbind("<Button-1>")  # Désactiver le binding après le clic

def run_action2():
    root.bind("<Button-1>", get_mouse_position_action2)

def get_mouse_position_action2(event):
    x, y = event.x, event.y
    label3.config(text=f"X: {x}")
    label4.config(text=f"Y: {y}")
    check_labels()
    root.unbind("<Button-1>")  # Désactiver le binding après le clic

def check_labels():
    x1 = int(label1.cget("text").split(": ")[1])
    y1 = int(label2.cget("text").split(": ")[1])
    x2 = int(label3.cget("text").split(": ")[1])
    y2 = int(label4.cget("text").split(": ")[1])
    
    if x2 < x1 or y2 < y1:
        label1.config(bg='red')
        label2.config(bg='red')
        label3.config(bg='red')
        label4.config(bg='red')
    else:
        label1.config(bg='white')
        label2.config(bg='white')
        label3.config(bg='white')
        label4.config(bg='white')

def run_action3():
    print("Action 3 exécutée")

def run_action4():
    print("Action 4 exécutée")

def run_action5():
    print("Action 5 exécutée")

def load_image():
    file_path = filedialog.askopenfilename()
    if file_path:
        img = Image.open(file_path)
        img = img.resize((550, 310), Image.LANCZOS)  # Ajustez la taille de l'image
        img_tk = ImageTk.PhotoImage(img)
        image_label.config(image=img_tk)
        image_label.image = img_tk

root = tk.Tk()
root.title("Fenêtre avec Image et Champs Libellés")
root.geometry("600x600")
root.wm_attributes('-alpha', 0.8)  # Semi-transparence

# Espace pour l'image
image_label = tk.Label(root, bg='white')
image_label.place(x=25, y=20, width=550, height=350)

# Champs libellés et boutons
labels = ["Label1", "Label2", "Label3", "Label4"]
actions = [run_action1, run_action2, run_action3, run_action4]

# Définir les labels globalement
global label1, label2, label3, label4
label1 = tk.Label(root, text="Label1", bg='white')
label1.place(x=25, y=390, width=100, height=40)

label2 = tk.Label(root, text="Label2", bg='white')
label2.place(x=135, y=390, width=100, height=40)

label3 = tk.Label(root, text="Label3", bg='white')
label3.place(x=245, y=390, width=100, height=40)

label4 = tk.Label(root, text="Label4", bg='white')
label4.place(x=355, y=390, width=100, height=40)

for i in range(2, 4):
    button = tk.Button(root, text=f"Action{i+1}", command=actions[i], bg='white')
    button.place(x=25 + i*110, y=430, width=100, height=40)

# Ajouter les boutons Action1 et Action2
button1 = tk.Button(root, text="Action1", command=run_action1, bg='white')
button1.place(x=25, y=430, width=100, height=40)

button2 = tk.Button(root, text="Action2", command=run_action2, bg='white')
button2.place(x=135, y=430, width=100, height=40)

# Champ libellé supplémentaire et bouton
label5 = tk.Label(root, text="Label5", bg='white')
label5.place(x=25, y=490, width=550, height=40)

button5 = tk.Button(root, text="Action5", command=run_action5, bg='white')
button5.place(x=475, y=410, width=100, height=40)  # Ajustement de la position

root.mainloop()