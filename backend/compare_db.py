import os

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

import settings
settings.parse()


def init_db():
    cred = credentials.Certificate("cred.json")
    prod_app = firebase_admin.initialize_app(cred, {
        'projectId': "badenbattle-a0dec"
    }, "prod_db")
    return firestore.client(prod_app)


def init_dev_db():
    cred = credentials.Certificate("cred-dev.json")
    dev_app = firebase_admin.initialize_app(cred, {
        'projectId': "mailmerge-59e91",
    }, "dev_db")
    return firestore.client(dev_app)


def run():
    db_1 = init_db()
    db_2 = init_dev_db()
    differences = list()
    for db_1_team in db_1.collection(settings.firestore.teams_collection).order_by("id").stream():
        db_1_team_id = db_1_team.to_dict()["id"]
        db_1_team_category = db_1_team.to_dict()["category"]
        db_1_team_city = db_1_team.to_dict()["city"]
        db_1_team_nbPlayers = db_1_team.to_dict()["id"]
        db_1_team_sectionName = db_1_team.to_dict()["sectionName"]
        db_1_team_sectionId = db_1_team.to_dict()["sectionId"]
        db_2_team = db_2.collection(settings.firestore.teams_collection).document(db_1_team_id).get()
        db_2_team_category = db_2_team.to_dict()["category"]
        db_2_team_city = db_2_team.to_dict()["city"]
        db_2_team_nbPlayers = db_2_team.to_dict()["id"]
        db_2_team_sectionName = db_2_team.to_dict()["sectionName"]
        db_2_team_sectionId = db_2_team.to_dict()["sectionId"]
        if db_1_team_sectionName != db_2_team_sectionName:
            differences.append(f"Team {db_1_team_id} db_1 sectionName is '{db_1_team_sectionName}' vs db_2 '{db_2_team_sectionName}'")
        if db_1_team_category != db_2_team_category:
            differences.append(f"Team {db_1_team_id} db_1 category is '{db_1_team_category}' vs db_2 '{db_2_team_category}'")
        if db_1_team_city != db_2_team_city:
            differences.append(f"Team {db_1_team_id} db_1 city is '{db_1_team_city}' vs db_2 '{db_2_team_city}'")
        if db_1_team_nbPlayers != db_2_team_nbPlayers:
            differences.append(f"Team {db_1_team_id} db_1 nbPlayers is '{db_1_team_nbPlayers}' vs db_2 '{db_2_team_nbPlayers}'")
        print(f"Team {db_1_team_id} processed")
    if len(differences) > 0:
        for difference in differences:
            print(difference)
    else:
        print("No differences found")


if __name__ == '__main__':
    run()
