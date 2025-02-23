import cv2
import difflib
import pyautogui
import numpy as np
from PIL import Image
import pytesseract

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
    return similarity_ratio > 0.9

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
        for pt in zip(*loc[::-1]):
            x, y = pt
            if y > lowest_y:
                lowest_y = y
                lowest_arrow = direction
    
    return lowest_arrow