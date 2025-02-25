from firebase_admin import auth
from firebase_admin import firestore

import controller.initialization
import main
import settings
from controller.badges import generate_badges, generate_missing_badges, generate_team_bb_badges
from controller.tools import parse_yaml
from model.section import Section
from stats import print_stats_section, print_stats_city

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

    reporter_from_soignies = {"win": 0, "loss": 0, "draw": 0}
    reporter_not_soignies = {"win": 0, "loss": 0, "draw": 0}
    for match in db.collection(settings.firestore.matches_collection).stream():
        m = match.to_dict()
        reporter = m["reporter"]
        if not reporter:
            continue
        reporter_section = db.collection(settings.firestore.profiles_collection).document(reporter).get().to_dict()["sectionId"]
        if not reporter_section:
            print(f"Reporter {reporter} has no section")
            continue
        reporter_city = db.collection(settings.firestore.sections_collection).document(reporter_section).get().to_dict()["city"]
        if m["draw"]:
            players = m["player_ids"]
            p0_city = db.collection(settings.firestore.teams_collection).document(players[0]).get().to_dict()["city"]
            p1_city = db.collection(settings.firestore.teams_collection).document(players[1]).get().to_dict()["city"]
            if p0_city == "Soignies" or p1_city == "Soignies":
                if reporter_city == "Soignies":
                    reporter_from_soignies["draw"] += 1
                else:
                    reporter_not_soignies["draw"] += 1
        else:
            winner_city = db.collection(settings.firestore.teams_collection).document(m["winner"]).get().to_dict()["city"]
            loser_city = db.collection(settings.firestore.teams_collection).document(m["loser"]).get().to_dict()["city"]
            if winner_city == "Soignies":
                if reporter_city == "Soignies":
                    reporter_from_soignies["win"] += 1
                else:
                    reporter_not_soignies["win"] += 1
            if loser_city == "Soignies":
                if reporter_city == "Soignies":
                    reporter_from_soignies["loss"] += 1
                else:
                    reporter_not_soignies["loss"] += 1

    print("reporter_from_soignies")
    print(reporter_from_soignies)
    print("reporter_not_soignies")
    print(reporter_not_soignies)
    
    # generate_badges(db, "badges.pdf")
    # generate_missing_badges(missing_badges, "badges_manquants.pdf")
    # generate_team_bb_badges(45, 1, "badges_staff.pdf")
    #print_games(db)
    # controller.initialization.validate_game_collection(db, 17)


if __name__ == '__main__':
    run()
