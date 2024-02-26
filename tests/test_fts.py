import sqlite3


def test_fts_extension_enabled():

    con = sqlite3.connect(':memory:')
    cur = con.cursor()
    cur.execute('pragma compile_options;')
    available_pragmas = cur.fetchall()
    con.close()

    assert ('ENABLE_FTS5',) in available_pragmas
