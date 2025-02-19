import pyautogui
import time
import tkinter as tk
from PIL import Image
import filecmp
import os
import pytesseract

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
def capture_screenshot(coords, filename):
    x1, y1, x2, y2 = coords
    screenshot = pyautogui.screenshot(region=(x1, y1, x2 - x1, y2 - y1))
    screenshot.save(filename)

# Fonction pour vérifier si deux fichiers sont différents
def files_are_different(file1, file2):
    return not filecmp.cmp(file1, file2, shallow=False)

# Fonction pour convertir une image en texte
def image_to_text(image_path):
    text = pytesseract.image_to_string(Image.open(image_path))
    return text

# Obtenir les coordonnées de la souris avec un délai
coords = get_mouse_coordinates_with_delay()

# Nom du fichier de capture d'écran
screenshot_filename = 'screenshot.png'
temp_filename = 'temp_screenshot.png'

# Boucle pour capturer l'écran toutes les 5 secondes
while True:
    capture_screenshot(coords, temp_filename)
    
    # Vérifier si le fichier temporaire est différent du fichier existant
    if not os.path.exists(screenshot_filename) or files_are_different(screenshot_filename, temp_filename):
        os.replace(temp_filename, screenshot_filename)
        print("Nouvelle capture d'écran enregistrée.")
    else:
        text = image_to_text(temp_filename)
        print("La capture d'écran est identique. Texte extrait de l'image :")
        print(text)
        os.remove(temp_filename)
    
    time.sleep(5)