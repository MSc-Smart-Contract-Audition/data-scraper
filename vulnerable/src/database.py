import csv
import os
import sys

"""
Register a custom dialect for the CSV module
"""
common_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../common"))
if common_path not in sys.path:
    sys.path.append(common_path)
from csv_dialect import get_dialect

FIELDNAMES = [
    "name",
    "severity",
    "description",
    "recommendation",
    "impact",
    "function",
]


class Database:
    def __init__(self, name):
        file_exists = os.path.isfile(f"../db-vulnerable/{name}-db.csv")
        self.file = open(f"../db-vulnerable/{name}-db.csv", "a")

        self.writer = csv.DictWriter(
            self.file,
            fieldnames=FIELDNAMES,
            dialect=get_dialect(),
        )

        if not file_exists:
            self.writer.writeheader()

    def escape(self, data):
        for key in data:
            data[key] = data[key].replace("\n", "\\n").replace("\r", "")
        return data

    def record(self, data, escaped=False):
        if not escaped:
            data = self.escape(data)
        self.writer.writerow(data)

    def close(self):
        self.file.close()
