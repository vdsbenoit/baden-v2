import itertools
import time
import uuid
from random import randint

from google.cloud import firestore

import settings
from controller.tools import parse_csv
from model import util
from model.game import Game
from model.match import Match
from model.section import Section
from model.team import Team

ALPHABET = [chr(s) for s in range(65, 91)]
TEAMS_COLLECTION    = "teams"
GAMES_COLLECTION    = "games"
MATCHES_COLLECTION  = "matches"
SECTIONS_COLLECTION = "sections"
SETTINGS_COLLECTION = "settings"
SETTINGS_DOCUMENT   = "app"


def get_team_letter(iterator):
    if iterator < 26:
        return ALPHABET[iterator]
    else:
        return "{}{}".format(
            ALPHABET[int(iterator/26) - 1],
            get_team_letter(iterator % 26)
        )


def _shuffle(teams, floor_number):
    """
    Distribute random numbers to a list of Team objects, starting at number floor_number
    :param teams: list of teams to shuffle
    :param floor_number: starting point for the number counter
    :return the list of modified teams
    """
    ceil_number = floor_number + len(teams)
    available_numbers = [i for i in range(floor_number, ceil_number)]
    for team in teams:
        index = randint(0, len(available_numbers) - 1)
        team.number = available_numbers[index]
        available_numbers.pop(index)
    if len(available_numbers) > 0:
        raise Exception("some numbers were not distributed during shuffle: {}".format(available_numbers))
    print("{} teams shuffled from number {} to {}".format(len(teams), floor_number, ceil_number - 1))


def _create_teams(db, categories: dict, nb_games: int):
    """
    Create teams and save them in the DB
    Update matches entries in the DB with the team ids
    """
    all_teams = list()
    letter_iterator = 0

    # Clear DB
    print(f"Clear '{TEAMS_COLLECTION}' collection...")
    util.delete_collection(db.collection(TEAMS_COLLECTION), 200)

    for category_name, sections in categories.items():
        category_teams = list()
        print(f"Create {category_name} teams...")

        section: Section
        for section in sections:
            for i in range(section.nbTeams):
                team_id = "{}{}".format(get_team_letter(letter_iterator), i + 1)
                category_teams.append(Team(team_id, section))
            letter_iterator += 1

        if len(category_teams) % (2 * nb_games) != 0:
            raise Exception("The amount of teams in a category must be a multiple of the double of the amount of games")

        _shuffle(category_teams, len(all_teams) + 1)

        all_teams.extend(category_teams)

    print("FireStore needs to update its indexes. Let's wait a little...")
    time.sleep(60)
    print("Save teams in the DB...")
    batch = db.batch()
    for team in all_teams:
        # get the matches for this team ordered in time
        for match in db.collection(MATCHES_COLLECTION).where("player_numbers", "array_contains", team.number).order_by("time").stream():
            # add the team id in the match entry (only possible after shuffle)
            match.reference.update({"player_ids": firestore.ArrayUnion([team.id])})
            # add the match id to the team attributes
            team.matches.append(match.id)
        assert (
            len(team.matches) == nb_games
        ), f"Incorrect amount of matches for team {team.id}: {len(team.matches)} vs {nb_games})"
        # save the team
        batch.set(db.collection(TEAMS_COLLECTION).document(team.id), team.to_dict())
    batch.commit()


def _create_sections(db, csv_data):
    """
    Process data from a csv holding all the section data
    It creates one document per section in the section collection on firestore
    It also creates a dictionary with one key per category (e.g. louveteaux, lutins etc)
    This dictionary is then used by the _create_teams function
    """
    categories = dict()

    # Clear DB
    print(f"Clear '{SECTIONS_COLLECTION}' collection...")
    util.delete_collection(db.collection(SECTIONS_COLLECTION), 200)

    batch = db.batch()

    # process data from csv file
    for section_data in csv_data:
        # Get an id for the section
        doc_ref = db.collection(SECTIONS_COLLECTION).document()
        section_id = doc_ref.id
        category = section_data[settings.csv.headers.category]

        # create a section object
        section = Section(
            section_id,
            section_data[settings.csv.headers.name],
            section_data[settings.csv.headers.city],
            section_data[settings.csv.headers.unit],
            section_data[settings.csv.headers.category],
            int(section_data[settings.csv.headers.nb_teams]),
            int(section_data[settings.csv.headers.nb_players]),
        )

        # Insert the section object in the categories dict
        if category not in categories.keys():
            categories[category] = list()
        categories[category].append(section)
        # Create a document for the section in the db
        batch.set(doc_ref, section.to_dict())

    # Update app settings with the categories list
    batch.update(db.collection(SETTINGS_COLLECTION).document(SETTINGS_DOCUMENT), {"categories": list(categories.keys())})
    batch.commit()
    return categories


def _create_schedule(db, nb_games: int, nb_circuits: int):
    """
    Generate a new schedule and save it in the DB
    """
    # Clear db
    print(f"Clear '{MATCHES_COLLECTION}' collection...")
    util.delete_collection(db.collection(MATCHES_COLLECTION), 200)
    print(f"Clear '{GAMES_COLLECTION}' collection...")
    util.delete_collection(db.collection(GAMES_COLLECTION), 200)

    for circuit_idx in range(nb_circuits):
        circuit_id = chr(circuit_idx + 65)
        teams = [i for i in range(1 + (nb_games * 2 * circuit_idx), 1 + nb_games * 2 * (circuit_idx + 1))]
        first_game = circuit_idx * nb_games + 1
        last_game = (circuit_idx + 1) * nb_games
        # game_2ways_range is a forth & back range of the game numbers [1, 2, 3, 3, 2, 1]
        game_2ways_range = [i for i in itertools.chain(range(first_game, 1 + last_game), range(last_game, first_game - 1, -1))]

        # Create games
        print(f"Define games for circuit {circuit_id}...")
        games = dict()
        for i in range(1, nb_games + 1):
            game_id = (circuit_idx * nb_games) + i
            games[game_id] = Game(str(game_id), circuit_id)

        # Create matches
        print(f"Define matches for circuit {circuit_id}...")
        for i in range(nb_games):  # iterate over each times in the schedule (same value as nb_games)
            matches = dict()
            time = i + 1
            for j, game_id in enumerate(game_2ways_range):
                team = teams[(j + i * 2) % (2 * nb_games)]
                if game_id in matches:
                    match = matches[game_id]
                else:
                    match = Match(str(uuid.uuid4().fields[-1]), str(game_id), time)
                    matches[game_id] = match
                    games[game_id].matches.append(match.id)
                match.player_numbers.append(team)

            for match in matches.values():
                match_ref = db.collection(MATCHES_COLLECTION).document(match.id)
                match_ref.set(match.to_dict())

        print(f"Save circuit {circuit_id} games in the DB")
        batch = db.batch()
        for game_id, game in games.items():
            batch.set(db.collection(GAMES_COLLECTION).document(str(game_id)), game.to_dict())
        batch.commit()


def validate_game_collection(db, nb_games, nb_circuits):
    """
    Assert the game setup complies with the following constraints:
        - a team cannot play against itself
        - a team cannot play against another team more than once
        - a team cannot play a game more than once
        - a team cannot play two matches at the same time
        - a game cannot have the same hash as another game
        - there is the right amount of matches in the DB
    """
    duel_set_list = list()
    for time in range(1, nb_games + 1):
        print(f"Validate matches collection for time {time}...")
        player_list = list()
        for m in db.collection(MATCHES_COLLECTION).where("time", "==", time).stream():
            players = m.to_dict()["player_ids"]
            players_set = {players[0], players[1]}
            assert (
                players[0] not in player_list
            ), "Team {} plays two games at time {}".format(players[0], time)
            assert (
                players[1] not in player_list
            ), "Team {} plays two games at time {}".format(players[1], time)
            assert (
                players[0] != players[1]
            ), "Player {} plays against itself in game {} at time {}".format(players[0], m.game_number, time)
            assert (
                players_set not in duel_set_list
            ), "Team {} already played against team {}".format(players[0], players[1])
            player_list.append(players[0])
            player_list.append(players[1])
            duel_set_list.append(players_set)
        assert (
            len(player_list) / 2 == nb_games * nb_circuits
        ), "The amount of matches in the DB is incorrect: {} vs {}".format(len(player_list) / 2, nb_games * nb_circuits)

    print("Validate games collection")
    hash_list = list()
    for g in db.collection(GAMES_COLLECTION).stream():
        print(f"Validate game {g.id}...")
        game_hash = g.to_dict()["hash"]
        assert game_hash not in hash_list, "Hash {} is used twice".format(game_hash)
        hash_list.append(game_hash)

        player_list = list()
        for m in db.collection(MATCHES_COLLECTION).where("game_id", "==", g.id).stream():
            players = m.to_dict()["player_ids"]
            assert (
                players[0] not in player_list
            ), "Team {} plays twice the game {}".format(players[0], g.to_dict()["number"])
            player_list.append(players[0])
            assert (
                players[1] not in player_list
            ), "Team {} plays twice the game {}".format(players[1], g.to_dict()["number"])
            player_list.append(players[1])

        assert (
                len(player_list) / 2 == nb_games
        ), "The amount of matches in the DB is incorrect: {} vs {}".format(len(player_list) / 2, nb_games)

    assert (
        len(hash_list) == nb_games * nb_circuits
    ), "The amount of games in the DB is incorrect: {} vs {}".format(len(hash_list), nb_games * nb_circuits)

    print("DB validated with success")


def create_new_db(db, nb_games: int, csv_path: str):
    """
    Generate a new schedule and save it in the DB
    Beware: it erases the previous teams, games & matches collections
    :param db: a Firestore db object
    :param nb_games: amount of games per circuit (amount of matches == amount of teams)
    :param csv_path: path to the csv files with the game data. This file must have headers that matches the 
                     values of the csv.headers settings in settings.yml
    """
    if nb_games % 2 == 0:
        raise Exception("The game amount must be a odd value")
    if nb_games < 1:
        raise Exception("The game amount must higher than 0")
    if nb_games != abs(nb_games):
        raise Exception("The game amount must be an integer")
    total_team_count = 0

    # read data from csv
    csv_data = parse_csv(csv_path)
    # process data from csv
    categories = _create_sections(db, csv_data)
    # check categories & sections data
    for category_name, sections in categories.items():
        cat_team_count = 0
        section: Section
        for section in sections:
            cat_team_count += section.nbTeams
        if cat_team_count % (2 * nb_games) != 0:
            raise Exception(
                "The total amount of teams in a category must be a multiple of the double fo the amount of games.\n"
                "{} has {} teams, which is not a multiple of {}".format(category_name, cat_team_count, 2 * nb_games)
            )
        total_team_count += cat_team_count
    nb_circuits = total_team_count / (2 * nb_games)
    if nb_circuits != abs(nb_circuits):
        raise Exception(f"The circuit amount ({nb_circuits}) must be an integer.")
    nb_circuits = int(nb_circuits)
    if nb_circuits < 1:
        raise Exception(f"The circuit amount ({nb_circuits}) must be greater than 0")
    if nb_circuits > 26:
        raise Exception(f"The circuit amount ({nb_circuits}) must be lower than 26")
    print(f"{nb_circuits} circuits will be created")
    _create_schedule(db, nb_games, nb_circuits)
    _create_teams(db, categories, nb_games)
    validate_game_collection(db, nb_games, nb_circuits)
