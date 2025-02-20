import pyautogui
import time
import tkinter as tk
from PIL import Image
import filecmp
import os
import pytesseract
import difflib
import cv2
import numpy as np  # Ajout de l'importation de NumPy

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Fonction pour obtenir les coordonnées de la souris avec un délai
def get_mouse_coordinates_with_delay():
    root = tk.Tk()
    root.withdraw()  # Masquer la fenêtre principale

    print("Déplacez la souris vers le coin supérieur gauche de la zone à capturer...")
    time.sleep(5)  # Attendre 5 secondes
    x1, y1 = pyautogui.position()
    print(f"Coordonnées du coin supérieur gauche : ({x1}, {y1})")

    print("Déplacez la souris vers le coin inférieur droit de la zone à capturer...")
    time.sleep(5)  # Attendre 5 secondes
    x2, y2 = pyautogui.position()
    print(f"Coordonnées du coin inférieur droit : ({x2}, {y2})")

    return (x1, y1, x2, y2)

# Fonction pour faire une capture d'écran
def capture_screenshot(coords_, filename):
    x1, y1, x2, y2 = coords_
    screenshot = pyautogui.screenshot(region=(x1, y1, x2 - x1, y2 - y1))
    screenshot.save(filename)

# Fonction pour vérifier si deux fichiers sont différents
def files_are_different(file1, file2):
    return not filecmp.cmp(file1, file2, shallow=False)

# Fonction pour convertir une image en texte avec prétraitement
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
        'up': cv2.imread('arrow_up.png', 0),
        'down': cv2.imread('arrow_down.png', 0),
        'left': cv2.imread('arrow_left.png', 0),
        'right': cv2.imread('arrow_right.png', 0)
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

# Obtenir les coordonnées de la souris avec un délai
coords = get_mouse_coordinates_with_delay()

# Nom du fichier de capture d'écran
screenshot_filename = 'screenshot.png'
temp_filename = 'temp_screenshot.png'

# Variable pour stocker le texte précédent
previous_text = ""

# Boucle pour capturer l'écran toutes les 5 secondes
while True:
    capture_screenshot(coords, screenshot_filename)
    
    # Extraire le texte de l'image capturée
    current_text = image_to_text(screenshot_filename)
    
    if not texts_are_similar(previous_text, current_text):
        previous_text = current_text
        print("Nouvelle capture d'écran enregistrée.")
        print("Texte extrait de l'image :")
        print(current_text)
        #Enregistrer le current_text dans label 5
        # Extraire et imprimer la flèche la plus en bas trouvée
        lowest_arrow = extract_lowest_arrow(screenshot_filename)
        if lowest_arrow:
            print("Flèche trouvée la plus en bas :", lowest_arrow)
            #Enregistrer le lowest_arrow a la suite de current_text dans label 5
    else:
        print("Le texte de la capture d'écran est similaire.")
    
    time.sleep(5)
