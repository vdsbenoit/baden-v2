# -*-coding:UTF-8 -*
import os
import tempfile

from docx import Document as Document_compose
from docxcompose.composer import Composer
from docxtpl import DocxTemplate
from firebase_admin import firestore

import main
import settings

settings.parse()

TEAM_ROADMAP_TEMPLATES = {
    "A": os.path.join("data/team_roadmap_templateA.docx"),
    "B": os.path.join("data/team_roadmap_templateB.docx"),
    "C": os.path.join("data/team_roadmap_templateC.docx"),
    "D": os.path.join("data/team_roadmap_templateD.docx"),
}
GAME_ROADMAP_TEMPLATE = os.path.join("data/game_roadmap_template.docx")


def _combine_docx(target_file, files):
    master = Document_compose(files[0])
    composer = Composer(master)
    for i in range(1, len(files)):
        doc_temp = Document_compose(files[i])
        composer.append(doc_temp)
    composer.save(target_file)


def generate_team_roadmaps(db, target_file):
    files_to_merge = list()
    with tempfile.TemporaryDirectory() as tmpdir:
        teams = db.collection(settings.firestore.teams_collection).order_by("id").stream()
        for t in teams:
            team = t.to_dict()
            print(f"Generating roadmap for {team['sectionName']} - {team['id']}...")

            context = dict(
                section=team["sectionName"],
                city=team["city"],
                teamId=str(team["id"]),
            )
            matches = db.collection(settings.firestore.matches_collection).where("player_ids", "array_contains", team["id"]).order_by("time").stream()
            for i, m in enumerate(matches, 1):
                match = m.to_dict()
                game_id = match["game_id"]
                game_ref = db.collection(settings.firestore.games_collection).document(str(game_id))
                g = game_ref.get()
                if not g.exists:
                    raise f"Game not found : {game_id}"
                game = g.to_dict()
                context["game{}".format(i)] = game["name"]
                context["gId{}".format(i)] = game["id"]
            # do it only once
            circuit = game["circuit"]
            context["circuit".format(i)] = circuit

            tpl = DocxTemplate(TEAM_ROADMAP_TEMPLATES[circuit])
            tpl.render(context)
            team_file = os.path.join(tmpdir, "team{}.docx".format(team["id"]))
            tpl.save(team_file)
            files_to_merge.append(team_file)

        print("Merging all team roadmaps...")
        _combine_docx(target_file, files_to_merge)


def generate_game_roadmaps(db, target_file):
    files_to_merge = list()
    with tempfile.TemporaryDirectory() as tmpdir:
        games = db.collection(settings.firestore.games_collection).order_by("id").stream()
        for g in games:
            game = g.to_dict()
            tpl = DocxTemplate(GAME_ROADMAP_TEMPLATE)
            print(f"Generating roadmap for {game['id']} - {game['name']}...")

            context = dict(
                gameName=game["name"],
                gId=str(game["id"]),
                circuit=game["circuit"],
            )
            matches = db.collection(settings.firestore.matches_collection).where("game_id", "==", int(game["id"])).order_by("time").stream()
            for i, m in enumerate(matches, 1):
                match = m.to_dict()
                context["players{}".format(i)] = "{} - {}".format(match["player_ids"][0], match["player_ids"][1])

            tpl.render(context)
            game_file = os.path.join(tmpdir, "game{}.docx".format(game["id"]))
            tpl.save(game_file)
            files_to_merge.append(game_file)

        print("Merging all game roadmaps...")
        _combine_docx(target_file, files_to_merge)


TARGET_TEAMS_ROADMAPS = "teams2022.docx"
TARGET_GAMES_ROADMAPS = "games2022.docx"


def run():
    main.init_api()
    db = firestore.client()
    # todo: dynamically get the schedule times here
    generate_team_roadmaps(db, TARGET_TEAMS_ROADMAPS)
    generate_game_roadmaps(db, TARGET_GAMES_ROADMAPS)
    print("Done!")


if __name__ == '__main__':
    run()
