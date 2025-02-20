import difflib

def verify_lines(text, target_list):
    lines = text.strip().split('\n')
    
    # Extraire les coordonnées de départ de la première ligne
    dechet ,POSdepart = lines[0].strip().split('[')
    posX, posY = POSdepart.strip('[]').split(',')
    print(f"Coordonnées de départ : {POSdepart}, posX : {posX}, posY : {posY}")
    
    
    # Ignorer la deuxième et la dernière ligne
    lines_to_check = lines[2:-1]

    # Vérifier l'existence des lignes X dans la liste donnée
    matched_lines = []
    for line in lines_to_check:
        # Utiliser difflib pour la correspondance souple
        for target in target_list:
            ratio = difflib.SequenceMatcher(None, line, target).ratio()
            if ratio > 0.8:  # Ajustez le seuil de similarité selon vos besoins
                matched_lines.append((line, target, ratio))
                break

    return matched_lines

# Exemple de chaîne et liste cible
example_text = """ETAPE : 1/4 Départ [-48,19]
ile d'Otomai (Plaines herbeuses)
@ Étoile verte en papier
2
2

4 essais restants

encoursVALIDER"""

target_list = [
    'Étoile verte en papier',
    'Étoile rouge en papier',
    'Étoile jaune peinte',
    'Étoile en papier plié',
    'Épée prise dans la glace',
    'Épouvantail à pipe',
    'Éolienne à quatre pales',
    'Échelle cassée',
    'Tube rempli de tofus',
    'Trou mielleux',
    'Tricycle',
    'Trace de main en sang',
    'Torii cassé',
    'Tombe inondée de sang',
    'Tombe inondée',
    'Tombe gravée d''un bouclier',
    'Tissu à carreaux noué',
    'Théière à rayures',
    'Tambour à rayures',
    'Tambour papatte',
    'Talisman en papier',
    'Sève qui s''écoule',
    'Symbole de quête peint',
    'Sucre d''orge',
    'Stèle chacha',
    'Statue wabbit',
    'Statue sidoa',
    'Statue koalak',
    'Squelette d''Ouginak pendu',
    'Soupe de bananagrumes',
    'Slip à petit coeur',
    'Serrure dorée',
    'Sapin couché',
    'Rune nimbos',
    'Ruban bleu noué',
    'Rouage pris dans la glace',
    'Rose noire',
    'Rose des vents dorée',
    'Rocher à sédimentation verticale',
    'Rocher taillé en arètes de poisson',
    'Rocher percé',
    'Rocher dé',
    'Rocher crâne',
    'Rocher Dofus',
    'Queue d''Osamodas',
    'Poupée koalak',
    'Poisson grillé embroché',
    'Pioche plantée',
    'Phorreur sournois / baveux / chafouin / fourbe',
    'Peluche de likrone',
    'Peinture de Dofus',
    'Panneau nonosse',
    'Palmifleur vert fleuri',
    'Palmifleur jaune fleuri',
    'Palmifleur bleu fleuri',
    'Palmier à pois',
    'Palmier à feuilles déchirées',
    'Palmier à feuilles carrées',
    'Palmier surchargé de noix de coco',
    'Palmier peint à rayures',
    'Palmier peint d''un chacha',
    'Paire de lunettes',
    'Os dans la lave',
    'Ornement flocon',
    'Oeuf dans un trou',
    'Oeil de shushu peint',
    'Obélisque enfoui',
    'Niche dans une caisse',
    'Moufles rouges',
    'Moufles jaunes',
    'Minouki',
    'Menottes',
    'Marionnette',
    'Logo Ankama peint',
    'Lapino origami',
    'Lanterne au crâne luminescent',
    'Langue dans un trou',
    'Lampion bleu',
    'Lampadaire fungus',
    'Kama peint',
    'Kaliptus à fleurs jaunes',
    'Kaliptus grignoté',
    'Kaliptus coupé',
    'Hache brisée',
    'Grelot',
    'Gravure de wukin',
    'Gravure de wabbit',
    'Gravure de tofu',
    'Gravure de symbole égal',
    'Gravure de symbole de quête',
    'Gravure de spirale',
    'Gravure de soleil',
    'Gravure de rose des vents',
    'Gravure de point',
    'Gravure de papatte',
    'Gravure de lune',
    'Gravure de logo Ankama',
    'Gravure de flèche',
    'Gravure de fleur',
    'Gravure de fantôme',
    'Gravure de dragodinde',
    'Gravure de crâne',
    'Gravure de croix',
    'Gravure de coeur',
    'Gravure de clef',
    'Gravure de chacha',
    'Gravure de boule de poche',
    'Gravure de bouftou',
    'Gravure de Kama',
    'Gravure de Gelax',
    'Gravure de Firefoux',
    'Gravure de Dofus',
    'Gravure d''étoile',
    'Gravure d''oeil',
    'Gravure d''arakne',
    'Gravure d''aile',
    'Gravure d''Epée',
    'Grand coquillage cassé',
    'Girouette dragodinde',
    'Framboisier',
    'Flèche dans une pomme',
    'Fleurs smiley',
    'Fleur de nénuphar bleue',
    'Filon de cristaux multicolores',
    'Fer à cheval',
    'Dé en glace',
    'Dolmen',
    'Dofus en bois',
    'Dessin koalak',
    'Dessin dragodinde',
    'Dessin de croix dans un cercle',
    'Dessin au pipi dans la neige',
    'Crâne de renne',
    'Crâne de likrone dans la glace',
    'Crâne de likrone',
    'Crâne de cristal',
    'Crâne de Roublard',
    'Crâne de Crâ',
    'Crâne dans un trou',
    'Crâ cramé',
    'Croix en pierre brisée',
    'Corne de likrone',
    'Corail flûtiste',
    'Corail avec des dents',
    'Coquillage à pois',
    'Coeur dans un nénuphar',
    'Cocotte origami',
    'Clef dorée',
    'Chaussette à pois',
    'Chapeau dé',
    'Champignon rayé',
    'Cerf-volant shinkansen',
    'Ceinture cloutée',
    'Casque à cornes',
    'Carapace de tortue',
    'Canne à kebab',
    'Canard en plastique',
    'Cairn',
    'Cadran solaire',
    'Cactus à fleur bleue',
    'Cactus sans épines',
    'Buisson poupée sadida',
    'Bouton de couture',
    'Boule dorée de marin',
    'Bougie dans un trou',
    'Bonhomme de neige fondu',
    'Bonbon bleu',
    'Bombe coeur',
    'Blé noir et blanc',
    'Barque coulée',
    'Bannière brâkmarienne déchirée',
    'Bannière bontarienne déchirée',
    'Ballons en forme de coeur',
    'Balançoire macabre',
    'Arche naturelle',
    'Arbre à épines',
    'Arbre à trous',
    'Arbre à moitié coupé',
    'Arbre glacé',
    'Arbre ensanglanté',
    'Arbre arc-en-ciel',
    'Anneau d''or',
    'Ancre dorée',
    'Aiguille à coudre',
    'Affiche de carte au trésor'
]

# Appel de la fonction
matched_lines = verify_lines(example_text, target_list)

print("Lignes correspondantes trouvées :")
for line, target, ratio in matched_lines:
    print(f"'{line}' correspond à '{target}' avec un ratio de similarité de {ratio:.2f}")
