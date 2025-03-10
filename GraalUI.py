import time
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import threading
import difflib
import cv2
import pyautogui
import numpy as np
import pytesseract
import pyperclip
from Actions import run_action1, run_action2, run_action3, run_action4,execute_sql_query
from Graal_parser import verify_lines, target_list
from Utils import capture_screenshot, preprocess_image, image_to_text, texts_are_similar, extract_lowest_arrow

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

stop_thread = False

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

def get_coords_from_labels():
    x1 = int(label1.cget("text").split(": ")[1])
    y1 = int(label2.cget("text").split(": ")[1])
    x2 = int(label3.cget("text").split(": ")[1])
    y2 = int(label4.cget("text").split(": ")[1])
    return (x1, y1, x2, y2)

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

    #while not stop_thread:
    capture_screenshot(coords, screenshot_filename)
    current_text = image_to_text(screenshot_filename)
    
    if not texts_are_similar(previous_text, current_text):
        previous_text = current_text
        print("Nouvelle capture d'écran enregistrée.")
        print("Texte extrait de l'image :")
        print(current_text)
        #label5.config(text=current_text)
        
        lowest_arrow = extract_lowest_arrow(screenshot_filename)
        if lowest_arrow:
            print("Flèche trouvée la plus en bas :", lowest_arrow)
            texte5 = label5.cget("text")  # Récupère le texte actuel du label
            new_text = texte5 + "\nFlèche: "+lowest_arrow  # Ajoute le nouveau texte
            label5.config(text=new_text)
        
        matched_lines,PosDepartX,PosDepartY = verify_lines(current_text, target_list)
        if matched_lines:
            last_match = matched_lines[-1]
            print(f"Dernier indice reconnu : "+last_match[1])
            texte5 = label5.cget("text")  # Récupère le texte actuel du label
            new_text = texte5 + "\nDernier indice : "+last_match[1]  # Ajoute le nouveau texte
            label5.config(text=new_text)
            if PosDepartX and PosDepartY :
                print(f"Position de départ : {PosDepartX} {PosDepartY}")
                destinationX, destinationY = execute_sql_query(lowest_arrow, last_match[1], PosDepartX, PosDepartY)
                if destinationX !='' and destinationY != '' :
                        # Copier le texte dans le presse-papiers
                    travel_command = f"/travel {destinationX},{destinationY}"
                    pyperclip.copy(travel_command)
                    label55.config(text=f"X: {destinationX}")
                    label6.config(text=f"X: {destinationY}")
        else : 
            print(f"Aucun indice reconnu")
    
    img = Image.open(screenshot_filename)
    img = img.resize((550, 310), Image.LANCZOS)
    img_tk = ImageTk.PhotoImage(img)
    image_label.config(image=img_tk)
    image_label.image = img_tk
        
        #time.sleep(5)
def indiceN(IndiceX, IndiceY,DestX, DestY):
    global stop_thread
    coords = get_coords_from_labels()
    screenshot_filename = 'screenshot.png'
    previous_text = ""

    #while not stop_thread:
    capture_screenshot(coords, screenshot_filename)
    current_text = image_to_text(screenshot_filename)
    
    if not texts_are_similar(previous_text, current_text):
        previous_text = current_text
        print("Nouvelle capture d'écran enregistrée.")
        print("Texte extrait de l'image :")
        print(current_text)
        #label5.config(text=current_text)
        
        lowest_arrow = extract_lowest_arrow(screenshot_filename)
        if lowest_arrow:
            print("Flèche trouvée la plus en bas :", lowest_arrow)
            texte5 = label5.cget("text")  # Récupère le texte actuel du label
            new_text = texte5 + "\nFlèche: "+lowest_arrow  # Ajoute le nouveau texte
            label5.config(text=new_text)
        
        matched_lines,IndiceuselessX,IndiceuselessY = verify_lines(current_text, target_list)
        if matched_lines:
            last_match = matched_lines[-1]
            print(f"Dernier indice reconnu : "+last_match[1])
            texte5 = label5.cget("text")  # Récupère le texte actuel du label
            new_text = texte5 + "\nDernier indice : "+last_match[1]  # Ajoute le nouveau texte
            label5.config(text=new_text)
            if IndiceX and IndiceY :
                print(f"Position de départ : {IndiceX} {IndiceY}")
                destinationX, destinationY = execute_sql_query(lowest_arrow, last_match[1], int(IndiceX.cget("text").split(": ")[1]), int(IndiceY.cget("text").split(": ")[1]))
                if destinationX !='' and destinationY != '' :
                        # Copier le texte dans le presse-papiers
                    travel_command = f"/travel {destinationX},{destinationY}"
                    pyperclip.copy(travel_command)
                    DestX.config(text=f"X: {destinationX}")
                    DestY.config(text=f"X: {destinationY}")
        else : 
            print(f"Aucun indice reconnu")
    
    img = Image.open(screenshot_filename)
    img = img.resize((550, 310), Image.LANCZOS)
    img_tk = ImageTk.PhotoImage(img)
    image_label.config(image=img_tk)
    image_label.image = img_tk
        
        #time.sleep(5)

def load_image():
    file_path = filedialog.askopenfilename()
    if file_path:
        img = Image.open(file_path)
        img = img.resize((550, 310), Image.LANCZOS)
        img_tk = ImageTk.PhotoImage(img)
        image_label.config(image=img_tk)
        image_label.image = img_tk

root = tk.Tk()
root.title("Fenêtre avec Image et Champs Libellés")
root.geometry("600x1000")
root.wm_attributes('-alpha', 0.5)

image_label = tk.Label(root, bg='white')
image_label.place(x=25, y=20, width=550, height=350)

labels = ["Label1", "Label2", "Label3", "Label4","Label55", "Label6", "Label7", "Label8","Label9", "Label10","Label11", "Label12", "Label13", "Label14"]
actions = [lambda: run_action1(root, label1, label2, check_labels), 
           lambda: run_action2(root, label3, label4, check_labels), 
           run_action3, run_action4,
           lambda : indiceN(label55,label6,label7,label8),
           lambda : indiceN(label7,label8,label9,label10),
           lambda : indiceN(label9,label10,label11,label12),
           lambda : indiceN(label11,label12,label13,label14)]

global label1, label2, label3, label4, label5
label1 = tk.Label(root, text="Label1", bg='white')
label1.place(x=25, y=390, width=100, height=40)

label2 = tk.Label(root, text="Label2", bg='white')
label2.place(x=135, y=390, width=100, height=40)

label3 = tk.Label(root, text="Label3", bg='white')
label3.place(x=245, y=390, width=100, height=40)

label4 = tk.Label(root, text="Label4", bg='white')
label4.place(x=355, y=390, width=100, height=40)

label55 = tk.Label(root, text="Label55", bg='white')
label55.place(x=25, y=480, width=100, height=40)

label6 = tk.Label(root, text="Label6", bg='white')
label6.place(x=135, y=480, width=100, height=40)

label7 = tk.Label(root, text="Label7", bg='white')
label7.place(x=25, y=530, width=100, height=40)

label8 = tk.Label(root, text="Label8", bg='white')
label8.place(x=135, y=530, width=100, height=40)

label9 = tk.Label(root, text="Label9", bg='white')
label9.place(x=25, y=580, width=100, height=40)

label10 = tk.Label(root, text="Label10", bg='white')
label10.place(x=135, y=580, width=100, height=40)

label11 = tk.Label(root, text="Label11", bg='white')
label11.place(x=25, y=630, width=100, height=40)

label12 = tk.Label(root, text="Label12", bg='white')
label12.place(x=135, y=630, width=100, height=40)

label13 = tk.Label(root, text="label13", bg='white')
label13.place(x=25, y=680, width=100, height=40)

label14 = tk.Label(root, text="label14", bg='white')
label14.place(x=135, y=680, width=100, height=40)

label1.config(text=f"X: {2193}")
label2.config(text=f"Y: {396}")
label3.config(text=f"X: {2554}")
label4.config(text=f"Y: {803}")

for i in range(2, 4):
    button = tk.Button(root, text=f"Action{i+1}", command=actions[i], bg='white')
    button.place(x=25 + i*110, y=430, width=100, height=40)

button1 = tk.Button(root, text="Action1", command=actions[0], bg='white')
button1.place(x=25, y=430, width=100, height=40)

button2 = tk.Button(root, text="Action2", command=actions[1], bg='white')
button2.place(x=135, y=430, width=100, height=40)

button6 = tk.Button(root, text="Indice2", command=actions[4], bg='white')
button6.place(x=245, y=480, width=100, height=40)
button7 = tk.Button(root, text="Indice3", command=actions[5], bg='white')
button7.place(x=245, y=530, width=100, height=40)
button8 = tk.Button(root, text="Indice4", command=actions[6], bg='white')
button8.place(x=245, y=580, width=100, height=40)
button9 = tk.Button(root, text="Indice5", command=actions[7], bg='white')
button9.place(x=245, y=630, width=100, height=40)
button10 = tk.Button(root, text="Indice6", command=actions[1], bg='white')
button10.place(x=245, y=680, width=100, height=40)

label5 = tk.Label(root, text="Label5", bg='white')
label5.place(x=25, y=790, width=550, height=240)

button5 = tk.Button(root, text="Action5", command=run_action5, bg='white')
button5.place(x=475, y=410, width=100, height=40)

root.mainloop()
