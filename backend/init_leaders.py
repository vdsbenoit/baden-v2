import datetime

from firebase_admin import auth
from firebase_admin import firestore

import main
import settings
from controller.tools import parse_yaml
from model.section import Section

settings.parse()


def set_leaders(db, config_file):
    leaders_config = parse_yaml(config_file)
    batch = db.batch()
    for section_name, section_data in leaders_config.items():
        role = section_data["role"]
        city = section_data["ville"]
        leaders = section_data["animateurs"]
        section_exists = section_data.get("exists", False)

        # todo: check if the section exists
        # Add section to db
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
            profile = {
                "email": email,
                "totem": totem,
                "name": name,
                "category": "Animateurs",
                "sectionId": section_id,
                "sectionName": section_name,
                "role": role,
                "uid": user.uid,
                "creationDate": datetime.datetime.now(tz=datetime.timezone.utc)
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
    # attention: ne détecte pas si une section existe déjà!
    # ce script recrée les sections à chaque fois
    # set_leaders(db, "data/animateurs.yml")
    set_leaders(db, "data/animateurs.yml")


if __name__ == '__main__':
    run()
