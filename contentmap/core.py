from typing import List, Dict
from datetime import datetime
import sqlite3
from contentmap.vss import ContentMapVSS


class ContentMapCreator:

    def __init__(
            self,
            contents: List[Dict[str, str]],
            database: str = "contentmap.db",
            include_vss: bool = False
    ):
        self.contents = contents
        self.include_vss = include_vss
        self.connection = sqlite3.connect(database)
        self.connection.row_factory = sqlite3.Row

        if self.include_vss:
            import sqlite_vss
            self.connection.enable_load_extension(True)
            sqlite_vss.load(self.connection)
            self.connection.enable_load_extension(False)

        self.cursor = self.connection.cursor()

    def init_db(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS content (url, content)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS config (cat, value)")
        self.connection.commit()

    def add_config(self):
        data = [
            {"Generated with:": "Contentmap lib"},
            {"Date:": datetime.now().strftime("%Y-%m-%d %H:%M:%S")},
            {"Embeddings:": "all-MiniLM-L6-v2"}
        ]
        data = [{"cat": k, "value": v} for row in data for k, v in row.items()]
        self.cursor.executemany("INSERT INTO config VALUES (:cat, :value)", data)
        self.connection.commit()

    def build(self):
        self.init_db()
        self.add_config()
        self.cursor.executemany(
            "INSERT INTO content VALUES (:url, :content)",
            self.contents
        )
        self.connection.commit()

        if self.include_vss:
            self.add_vss()

    def add_vss(self):
        cm_vss = ContentMapVSS(connection=self.connection)
        cm_vss.load()
