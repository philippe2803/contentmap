import os.path as op
import shutil


def build_fixture_db():
    fixture_db = op.join(op.dirname(__file__), 'fixture.db')
    dest = op.join(op.dirname(__file__), 'contentmap.db')
    shutil.copy(fixture_db, dest)
    return dest
