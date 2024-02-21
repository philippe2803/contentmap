from contentmap.vss import ContentMapVSS
import os.path as op
from tests.utils import build_fixture_db


class TestContentMapVSS:

    def test_assertion_content_exists(self):
        fixture_db = op.join(op.dirname(__file__), "fixture.db")
        vss_content = ContentMapVSS(db_file=fixture_db)
        assert vss_content.table_exists(table_name="content") is True

    def test_assertion_content_not_exists(self):
        vss_content = ContentMapVSS(db_file=":memory:")
        assert vss_content.table_exists(table_name="content") is False


class TestVssTablesCreation:

    db = build_fixture_db()

    def test_vss_instance(self):
        cm_vss = ContentMapVSS(db_file=self.db)
        cm_vss.load()
        assert cm_vss.table_exists("content_chunks")
