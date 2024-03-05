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

    def test_vss_instance(self):
        db = build_fixture_db()
        cm_vss = ContentMapVSS(db_file=db)
        cm_vss.load()
        assert cm_vss.table_exists("content_chunks")

    def test_prepare_texts_and_metadatas(self):
        db = build_fixture_db()
        cm_vss = ContentMapVSS(db_file=db)
        texts, metadatas = cm_vss.prepare_texts_and_metadatas()
        assert len(texts) == len(metadatas) >= 1

    def test_chunk_table(self):
        db = build_fixture_db()
        cm_vss = ContentMapVSS(db_file=db)
        cm_vss.load()
        assert cm_vss.table_exists("content_chunks")
        cursor = cm_vss.connection.cursor()
        res = cursor.execute("SELECT * FROM content_chunks")
        rows = res.fetchall()
        assert len(rows) >= 15

    def test_similarity_search(self):
        db = build_fixture_db()
        cm_vss = ContentMapVSS(db_file=db)
        cm_vss.load()
        data = cm_vss.similarity_search(query="who is Mistral ai company?", k=2)
        assert len(data) == 2
        urls = [doc["url"] for doc in data]
        for url in urls:
            assert url == "https://philippeoger.com/pages/ai-scene-in-europe-last-week/"
