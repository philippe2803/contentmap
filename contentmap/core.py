from typing import List, Dict, TypedDict
from datetime import datetime
import sqlite3
import importlib.metadata


class ContentMapCreator:

    def __init__(
            self,
            contents: List[Dict[str, str]],
            database: str = "contentmap.db"
    ):
        self.contents = contents
        self.db = sqlite3.connect(database)
        self.db.row_factory = sqlite3.Row
        self.cursor = self.db.cursor()

    def init_db(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS content (url, content)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS config (cat, value)")
        self.db.commit()

    def add_config(self):
        data = [
            {"Version:": "1"},
            {"Generated with:": "Contentmap lib"},
            {"Date:": datetime.now().strftime("%Y-%m-%d %H:%M:%S")},
            {"Embeddings:": "mistral-embed"},
            {"FTSE:": None},
        ]
        data = [{"cat": k, "value": v} for row in data for k, v in row.items()]
        self.cursor.executemany("INSERT INTO config VALUES (:cat, :value)", data)
        self.db.commit()

    def build(self):
        self.init_db()
        self.add_config()
        self.cursor.executemany(
            "INSERT INTO content VALUES (:url, :content)",
            self.contents
        )
        self.db.commit()
