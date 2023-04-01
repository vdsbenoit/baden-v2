from firebase_admin import auth
from firebase_admin import firestore

import controller.initialization
import main
import settings
from controller.badges import generate_badges, generate_missing_badges, generate_team_bb_badges
from controller.tools import parse_yaml
from model.section import Section

settings.parse()

CSV_PATH = "data/repartition2022.csv"
GAME_NAMES_PATH = "data/game_names2022.yml"


def print_games(db):
    for g in db.collection(settings.firestore.games_collection).order_by("id").stream():
        game_circuit = g.to_dict()["circuit"]
        game_id = g.to_dict()["id"]
        game_name = g.to_dict()["name"]

        print(f"{game_circuit}  {game_id}   {game_name}")


missing_badges = [
    {"teams": ["6A", "6B", "6C"], "colors": ["#2C5F2D", "#FFE77A"], "amount": 1},
    {"teams": ["28A", "28B", "28C", "28D", "28E"], "colors": ["#00203F", "#ADEFD1"], "amount": 1},
    {"teams": ["2A"], "colors": ["#1C1C1B", "#CE4A7E"], "amount": 2},
    {"teams": ["13A"], "colors": ["#89ABE3", "#FCF6F5"], "amount": 1}
]


GAMES_PER_CIRCUIT = 17
MIN_PLAYERS_PER_TEAM = 4
MAX_PLAYERS_PER_TEAM = 10


def run():
    main.init_api()
    db = firestore.client()
    
    sample = [
        {"category": "Baladins & Nutons", "city": "Haine-Saint-Pierre", "unit": "BR006", "name": "Ribambelle Saint-Georges", "players": 20, "leaders": 4},
        {"category": "Baladins & Nutons", "city": "Leernes, Fontaine-l'Evêque", "unit": "9.T.O.", "name": "Baladins de Leernes", "players": 8, "leaders": 3},
        {"category": "Baladins & Nutons", "city": "Enghien", "unit": "BR001", "name": "Baladins Enghien", "players": 37, "leaders": 8},
        {"category": "Baladins & Nutons", "city": "Monceau-sur-Sambre", "unit": "To003", "name": "Ribambelle", "players": 7, "leaders": 3},
        {"category": "Baladins & Nutons", "city": "Braine le comte ", "unit": "BR004 B", "name": "Baladins de B-L-C", "players": 12, "leaders": 4},
        {"category": "Baladins & Nutons", "city": "Neufvilles ", "unit": "BR005 ", "name": "Baladins de Neufvilles ", "players": 16, "leaders": 6},
        {"category": "Baladins & Nutons", "city": "Soignies", "unit": "HC06", "name": "Nutons Lucioles", "players": 32, "leaders": 7},
        {"category": "Baladins & Nutons", "city": "Ecaussinnes ", "unit": "HC 04", "name": "Chaumière d'Ecaussines", "players": 23, "leaders": 7},
        {"category": "Baladins & Nutons", "city": "Braine-le-Comte", "unit": "HC02", "name": "Nutons de B-L-C", "players": 14, "leaders": 5},
        {"category": "Louveteaux", "city": "Casteau", "unit": "HD003", "name": "Meute de Casteau ", "players": 37, "leaders": 10},
        {"category": "Louveteaux", "city": "Enghien", "unit": "BR001", "name": "Meute Seeonee", "players": 31, "leaders": 7},
        {"category": "Louveteaux", "city": "Anderlues", "unit": "6To", "name": "Louveteaux D'Anderlues ", "players": 16, "leaders": 4},
        {"category": "Louveteaux", "city": "Enghien", "unit": "BR001", "name": "Meute Khanhiwhara ", "players": 30, "leaders": 8},
        {"category": "Louveteaux", "city": "Ecaussinnes", "unit": "BR002", "name": "Louveteaux", "players": 55, "leaders": 10},
        {"category": "Louveteaux", "city": "Leernes", "unit": "TO009", "name": "Meute de Leernes", "players": 26, "leaders": 4},
        {"category": "Louveteaux", "city": "Monceau-Sur-Sambre", "unit": "TO003", "name": "Meute de la 3TO", "players": 21, "leaders": 5},
        {"category": "Louveteaux", "city": "Tubize", "unit": "BR 18RP", "name": "Meute Waigunga", "players": 31, "leaders": 8},
        {"category": "Louveteaux", "city": "Soignies", "unit": "BR015 L1", "name": "Meute Waingunga", "players": 36, "leaders": 5},
        {"category": "Louveteaux", "city": "Haine-Saint-Pierre ", "unit": "BR006", "name": "Meute Khanhiwara", "players": 24, "leaders": 7},
        {"category": "Louveteaux", "city": "Braine le Comte", "unit": "BR004", "name": "Meute Micheline Gauthier", "players": 20, "leaders": 9},
        {"category": "Louveteaux", "city": "Soignies", "unit": "BR015 L2", "name": "Meute Ferao", "players": 35, "leaders": 7},
        {"category": "Louveteaux", "city": "Biesme", "unit": "NM023", "name": "Louveteaux de Biesme", "players": 26, "leaders": 9},
        {"category": "Louveteaux", "city": "Hennuyères", "unit": "BR017", "name": "Louveteaux d'Hennuyères ", "players": 34, "leaders": 6},
        {"category": "Louveteaux", "city": "Neufvilles", "unit": "BR005", "name": "Meute petite grenouille", "players": 38, "leaders": 6},
        {"category": "Louveteaux", "city": "La Louvière", "unit": "BR007", "name": "Meute Waingunga", "players": 17, "leaders": 7},
        {"category": "Lutins", "city": "Ecaussinnes", "unit": "4HC", "name": "Lutins Sainte Therèse", "players": 53, "leaders": 9},
        {"category": "Lutins", "city": "Soignies", "unit": "HC06B", "name": "Lutins Ecureuils ", "players": 40, "leaders": 8},
        {"category": "Lutins", "city": "Hyon ", "unit": "12HC", "name": "Lutins ", "players": 42, "leaders": 9},
        {"category": "Lutins", "city": "Saint-Symphorien", "unit": "13HC", "name": "Lutins Soleil levant", "players": 41, "leaders": 8},
        {"category": "Lutins", "city": "Braine-le-Comte ", "unit": "HC2", "name": "Les Lutins de B-L-C ", "players": 35, "leaders": 6},
        {"category": "Lutins", "city": "Ath ", "unit": "4HO ", "name": "Les Lutins d’Ath ", "players": 35, "leaders": 7},
        {"category": "Lutins", "city": "Boussu ", "unit": "JeanXXIII", "name": "Les Lutins de Boussu", "players": 8, "leaders": 4},
        {"category": "Lutins", "city": "Soignies", "unit": "HC06", "name": "Lutins Feux-Follets", "players": 33, "leaders": 8},
    ]
    controller.initialization.create_new_db(db, sample, GAMES_PER_CIRCUIT, MIN_PLAYERS_PER_TEAM, MAX_PLAYERS_PER_TEAM)
    # generate_badges(db, "badges.pdf")
    # generate_missing_badges(missing_badges, "badges_manquants.pdf")
    # generate_team_bb_badges(45, 1, "badges_staff.pdf")
    #print_games(db)
    # controller.initialization.validate_game_collection(db, 17)


if __name__ == '__main__':
    run()
