from firebase_admin import auth
from firebase_admin import firestore

import controller.initialization
import main
import settings
from controller.badges import generate_badges
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


def run():
    main.init_api()
    db = firestore.client()
    # controller.initialization.create_new_db(db, 17, CSV_PATH, GAME_NAMES_PATH)
    # generate_badges(db, "badges.pdf")
    # print_games(db)


if __name__ == '__main__':
    run()
