import csv
import settings


def parse_csv(filename: str):
    with open(filename, mode="r", encoding="utf-8-sig") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=settings.csv.delimiter)
        data = [row for row in reader if row[list(row.keys())[0]]]
    return data
