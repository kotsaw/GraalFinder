import json
import sqlite3

# Charger le fichier JSON
with open(r'C:\Users\hjeanjacques\Desktop\Untitled-1.json', 'r', encoding='windows-1252') as file:
    data = json.load(file)
with open(r'C:\Users\hjeanjacques\Desktop\Untitled-2.json', 'r', encoding='windows-1252') as file:
    data_clues = json.load(file)

# Connexion à la base de données SQLite (ou création si elle n'existe pas)
conn = sqlite3.connect('example.db')
cursor = conn.cursor()

# Créer une table (si elle n'existe pas déjà)
cursor.execute('''
CREATE TABLE IF NOT EXISTS Graal (
    id INTEGER PRIMARY KEY,
    PosX TEXT,
    PosY TEXT,
    Indices TEXT
)
''')
# Créer une table (si elle n'existe pas déjà)
cursor.execute('''
CREATE TABLE IF NOT EXISTS Graal_indices (
    id INTEGER PRIMARY KEY,
    Cle INTEGER,
    nom TEXT
)
''')
cursor.execute('''
DELETE FROM Graal_indices
''')
cursor.execute('''
DELETE FROM Graal
''')

indice = 0
# Insérer des données dans la table
for item in data:
    indice +=1
    clues_str = '|'.join(item['clues'])
    cursor.execute('''
    INSERT INTO Graal (PosX, PosY, Indices) VALUES (?, ?, ?)
    ''', (item['x'], item['y'],clues_str))
    print(indice)
    
# Insérer des données dans la table
indice = 0
for item in data_clues:
    indice +=1
    cursor.execute('''
    INSERT INTO Graal_indices (cle, nom) VALUES (?, ?)
    ''', (item['clueid'], item['hintfr']))
    print(indice)
# Sauvegarder (commit) les changements et fermer la connexion
conn.commit()
conn.close()