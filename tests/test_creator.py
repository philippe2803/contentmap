from contentmap.core import ContentMapCreator
import sqlite3


data = [
    {"url": "https://www.google.com", "content": "this is google home page"},
    {"url": "https://www.google.com/about", "content": "this is google about page"},
]


def test_generator():
    database = ContentMapCreator(data)
    assert isinstance(database.db, sqlite3.Connection)
    assert isinstance(database.cursor, sqlite3.Cursor)


def test_schema():
    database = ContentMapCreator(data)
    database.build()
    query = database.cursor.execute("SELECT count(1) FROM content")
    assert query.fetchone()[0] == 2

