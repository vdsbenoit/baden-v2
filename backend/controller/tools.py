import csv
import settings


def parse_csv(filename: str):
    with open(filename, mode="r", encoding="utf-8-sig") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=settings.csv.delimiter)
        data = [row for row in reader if row[list(row.keys())[0]]]
    return data


def parse_game_names(filename: str):
    game_names = list()
    with open(filename, mode="r", encoding="utf-8-sig") as game_name_file:
        game_names = game_name_file.read().splitlines()
    return game_names
