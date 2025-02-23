import threading
import time
import pyautogui
import sqlite3

def format_query(query, params):
    for param in params:
        query = query.replace('?', f"'{param}'", 1)
    return query

def execute_sql_query(lowest_arrow, last_match, PosDepartX, PosDepartY):
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()

    if lowest_arrow == 'up':
        query = "SELECT * FROM graal JOIN Graal_indices ON  '|' || Graal.Indices || '|' LIKE '%|' || graal_indices.Cle || '|%' WHERE Graal_indices.nom = ? AND Graal.PosY > ? AND Graal.PosY <= ? AND posx = ? ORDER BY PosX ASC LIMIT 1"
        params = (last_match, int(PosDepartY), int(PosDepartY) - 10, int(PosDepartX))
    elif lowest_arrow == 'down':
        query = "SELECT * FROM graal JOIN Graal_indices ON  '|' || Graal.Indices || '|' LIKE '%|' || graal_indices.Cle || '|%' WHERE Graal_indices.nom = ? AND Graal.PosY >= ? AND Graal.PosY < ? AND posx = ? ORDER BY PosX ASC LIMIT 1"
        params = (last_match, int(PosDepartY) - 10, int(PosDepartY), int(PosDepartX))
    elif lowest_arrow == 'left':
        query = "SELECT * FROM graal JOIN Graal_indices ON  '|' || Graal.Indices || '|' LIKE '%|' || graal_indices.Cle || '|%' WHERE Graal_indices.nom = ? AND Graal.PosX > ? AND Graal.PosX <= ? AND posy = ? ORDER BY PosX ASC LIMIT 1"
        params = (last_match, int(PosDepartX) - 10, int(PosDepartX), int(PosDepartY))
    elif lowest_arrow == 'right':
        query = "SELECT * FROM graal JOIN Graal_indices ON  '|' || Graal.Indices || '|' LIKE '%|' || graal_indices.Cle || '|%' WHERE Graal_indices.nom = ? AND Graal.PosX >= ? AND Graal.PosX < ? AND posy = ? ORDER BY PosX ASC LIMIT 1"
        params = (last_match, int(PosDepartX), int(PosDepartX) + 10, int(PosDepartY))
    else:
        print("Flèche non reconnue")
        return
    
    formatted_query = format_query(query, params)
    print("Query exécutée : " + formatted_query)
    
    cursor.execute(query, params)
    result = cursor.fetchone()
    posX = ''
    posY = ''
    if result:
        posX = result[1]
        posY = result[2]
        print(f"PosX: {posX}, PosY: {posY}")
    else:
        print("Aucun résultat trouvé.")
    
    conn.close()
    return posX,posY

def run_action1(root, label1, label2, check_labels):
    root.withdraw()
    print("Cliquez pour obtenir les coordonnées du coin supérieur gauche...")
    time.sleep(2)
    x, y = pyautogui.position()
    label1.config(text=f"X: {x}")
    label2.config(text=f"Y: {y}")
    root.deiconify()
    check_labels()

def run_action2(root, label3, label4, check_labels):
    root.withdraw()
    print("Cliquez pour obtenir les coordonnées du coin inférieur droit...")
    time.sleep(2)
    x, y = pyautogui.position()
    label3.config(text=f"X: {x}")
    label4.config(text=f"Y: {y}")
    root.deiconify()
    check_labels()

def run_action3():
    print("Action 3 exécutée")

def run_action4():
    global stop_thread
    stop_thread = True
    print("Action 4 exécutée : arrêt du thread de l'action 5")

