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


def run():
    main.init_api()
    db = firestore.client()
    #controller.initialization.create_new_db(db, 17, CSV_PATH, GAME_NAMES_PATH)
    # generate_badges(db, "badges.pdf")
    # generate_missing_badges(missing_badges, "badges_manquants.pdf")
    # generate_team_bb_badges(45, 1, "badges_staff.pdf")
    #print_games(db)
    controller.initialization.validate_game_collection(db, 17, 4)


if __name__ == '__main__':
    run()
