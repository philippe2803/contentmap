from contentmap.core import ContentMapCreator
import sqlite3


data = [
    {"url": "https://www.google.com", "content": "this is google home page"},
    {"url": "https://www.google.com/about", "content": "this is google about page"},
]


def test_generator():
    database = ContentMapCreator(data)
    assert isinstance(database.connection, sqlite3.Connection)
    assert isinstance(database.cursor, sqlite3.Cursor)


def test_schema():
    database = ContentMapCreator(data)
    database.build()
    query = database.cursor.execute("SELECT count(1) FROM content")
    assert query.fetchone()[0] == 2


def test_content_creator_vss():
    database = ContentMapCreator(data, include_vss=True)
    database.build()
    query = database.cursor.execute("SELECT count(1) FROM content_chunks")
    assert query.fetchone()[0] == 4


def test_content_creator_vss_check_chunks():
    database = ContentMapCreator(data, include_vss=True)
    database.build()
    query = "SELECT distinct(tbl_name) FROM sqlite_master"
    result = database.cursor.execute(query)
    found_tables = []
    for row in result:
        found_tables.append(row["tbl_name"])
    assert "content" in found_tables
    assert "content_chunks" in found_tables
