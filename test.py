import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import pyautogui
import time
import filecmp
import os
import pytesseract
import difflib
import cv2
import numpy as np
import threading

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Variable de contrôle pour arrêter le thread
stop_thread = False

def run_action1():
    root.withdraw()  # Masquer la fenêtre principale pour permettre de cliquer en dehors
    print("Cliquez pour obtenir les coordonnées du coin supérieur gauche...")
    time.sleep(2)  # Attendre un peu pour permettre de cliquer
    x, y = pyautogui.position()
    label1.config(text=f"X: {x}")
    label2.config(text=f"Y: {y}")
    root.deiconify()  # Réafficher la fenêtre principale
    check_labels()

def run_action2():
    root.withdraw()  # Masquer la fenêtre principale pour permettre de cliquer en dehors
    print("Cliquez pour obtenir les coordonnées du coin inférieur droit...")
    time.sleep(2)  # Attendre un peu pour permettre de cliquer
    x, y = pyautogui.position()
    label3.config(text=f"X: {x}")
    label4.config(text=f"Y: {y}")
    root.deiconify()  # Réafficher la fenêtre principale
    check_labels()

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
    global stop_thread
    stop_thread = True
    print("Action 4 exécutée : arrêt du thread de l'action 5")

def run_action5():
    global stop_thread
    stop_thread = False
    thread = threading.Thread(target=capture_loop)
    thread.start()

def capture_loop():
    global stop_thread
    coords = get_coords_from_labels()
    screenshot_filename = 'screenshot.png'
    previous_text = ""

    while not stop_thread:
        capture_screenshot(coords, screenshot_filename)
        current_text = image_to_text(screenshot_filename)
        
        if not texts_are_similar(previous_text, current_text):
            previous_text = current_text
            print("Nouvelle capture d'écran enregistrée.")
            print("Texte extrait de l'image :")
            print(current_text)
            label5.config(text=current_text)  # Enregistrer le current_text dans label5
            
            lowest_arrow = extract_lowest_arrow(screenshot_filename)
            if lowest_arrow:
                print("Flèche trouvée la plus en bas :", lowest_arrow)
                label5.config(text=f"{current_text}\nFlèche: {lowest_arrow}")  # Enregistrer le lowest_arrow à la suite de current_text dans label5
        else:
            print("Le texte de la capture d'écran est similaire.")
        
        time.sleep(5)

def get_coords_from_labels():
    x1 = int(label1.cget("text").split(": ")[1])
    y1 = int(label2.cget("text").split(": ")[1])
    x2 = int(label3.cget("text").split(": ")[1])
    y2 = int(label4.cget("text").split(": ")[1])
    return (x1, y1, x2, y2)

def capture_screenshot(coords_, filename):
    x1, y1, x2, y2 = coords_
    screenshot = pyautogui.screenshot(region=(x1, y1, x2 - x1, y2 - y1))
    screenshot.save(filename)

def preprocess_image(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return Image.fromarray(binary)

def image_to_text(image_path):
    preprocessed_image = preprocess_image(image_path)
    text = pytesseract.image_to_string(preprocessed_image)
    return text

def texts_are_similar(text1, text2):
    similarity_ratio = difflib.SequenceMatcher(None, text1, text2).ratio()
    return similarity_ratio > 0.9  # Ajustez le seuil selon vos besoins

def extract_lowest_arrow(image_path):
    templates = {
        'up': cv2.imread('Arrow/arrow_up.png', 0),
        'down': cv2.imread('Arrow/arrow_down.png', 0),
        'left': cv2.imread('Arrow/arrow_left.png', 0),
        'right': cv2.imread('Arrow/arrow_right.png', 0)
    }
    
    img_rgb = cv2.imread(image_path)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    
    lowest_arrow = None
    lowest_y = -1
    
    for direction, template in templates.items():
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.8
        loc = np.where(res >= threshold)
        for pt in zip(*loc[::-1]):  # Boucle sur les points trouvés
            x, y = pt
            if y > lowest_y:
                lowest_y = y
                lowest_arrow = direction
    
    return lowest_arrow

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
root.geometry("600x1000")
root.wm_attributes('-alpha', 0.5)  # Semi-transparence

# Espace pour l'image
image_label = tk.Label(root, bg='white')
image_label.place(x=25, y=20, width=550, height=350)

# Champs libellés et boutons
labels = ["Label1", "Label2", "Label3", "Label4"]
actions = [run_action1, run_action2, run_action3, run_action4]

# Définir les labels globalement
global label1, label2, label3, label4, label5
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