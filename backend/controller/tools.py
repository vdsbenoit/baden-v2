import csv
import settings


def parse_csv(filename: str):
    with open(filename, mode="r", encoding="utf-8-sig") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=settings.csv.delimiter)
        data = [row for row in reader]
    return data
