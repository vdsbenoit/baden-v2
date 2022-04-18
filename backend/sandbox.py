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


def set_leaders(db):
    leaders_config = parse_yaml("data/animateurs.yml")
    batch = db.batch()
    for section_name, section_data in leaders_config.items():
        role = section_data["role"]
        city = section_data["ville"]
        leaders = section_data["animateurs"]
        section_exists = section_data.get("exists", False)

        # todo: check if the section exists
        # Add section to db
        if section_exists:
            print(f"Section marked as existing: {section_name}")
        else:
            doc_ref = db.collection(settings.firestore.sections_collection).document()
            section_id = doc_ref.id
            section = Section(
                section_id,
                section_name,
                city,
                "",
                "Animateurs",
                0,
                0,
            )
            batch.set(doc_ref, section.to_dict())
            print(f"New section created for '{section_name}' with id {doc_ref.id}")
        for leader in leaders:
            user_exists = False
            totem = leader.get("totem", "")
            name = leader.get("name", "")
            email = leader.get("email", None)
            if not email:
                raise(f"email not found for leader {totem}/{name}")
            try:
                user = auth.get_user_by_email(email)
                user_exists = True
                print(f"The user already exists in the DB : {email}")
            except:
                user = auth.create_user(email=email)
            # todo: get doc id
            profile = {
                "email": email,
                "totem": totem,
                "name": name,
                "category": "Animateurs",
                "sectionId": section_id,
                "sectionName": section_name,
                "role": role,
                "uid": user.uid
            }
            if user_exists:
                batch.update(db.collection(settings.firestore.profiles_collection).document(user.uid), profile)
                print(f"Updated: {email} (uid: {user.uid})")
            else:
                batch.set(db.collection(settings.firestore.profiles_collection).document(user.uid), profile)
                print(f"Created: {email} (uid: {user.uid})")
    batch.commit()
    print("Change applied to the DB")


def run():
    main.init_api()
    db = firestore.client()
    # controller.initialization.create_new_db(db, 17, CSV_PATH, GAME_NAMES_PATH)
    # generate_badges(db, "badges.pdf")
    # print_games(db)
    set_leaders(db) # attention: ne détecte pas si une section existe déjà!


if __name__ == '__main__':
    run()
