from typing import List, Dict, TypedDict
import sqlite3


class ContentMapCreator:

    def __init__(self, contents: List[Dict[str, str]]):
        self.contents = contents
        self.db = sqlite3.connect("contentmap.db")
        self.db.row_factory = sqlite3.Row
        self.cursor = self.db.cursor()

    def build(self):
        self.cursor.execute("CREATE TABLE contentmap (url, content)")
        self.cursor.executemany(
            "INSERT INTO contentmap VALUES (:url, :content)",
            self.contents
        )
