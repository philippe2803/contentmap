"""
Class ContentMapVSS to create vector search dataset from a contentmap
dataset already created.
"""
import sqlite3
from typing import Optional

import sqlite_vss
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)
from langchain_community.vectorstores import SQLiteVSS


class ContentMapVSS:

    def __init__(self,
                 connection: Optional[sqlite3.Connection] = None,
                 db_file: str = "contentmap.db"
                 ):

        self.connection = connection
        if not connection:
            self.connection = SQLiteVSS.create_connection(db_file)

        embedding_function = SentenceTransformerEmbeddings(
            model_name="all-MiniLM-L6-v2"
        )
        self.vss = SQLiteVSS(
            table="content_chunks",
            embedding=embedding_function,
            connection=self.connection
        )

    def load(self):
        # content table must be there
        assert self.table_exists(table_name="content")
        texts, metadatas = self.prepare_texts_and_metadatas()
        self.vss.add_texts(texts=texts, metadatas=metadatas)
        return self.vss

    def table_exists(self, table_name: str) -> bool:
        res = self.connection.execute(f"""
            SELECT name 
            FROM sqlite_master 
            WHERE type='table' AND name='{table_name}';
        """)
        rows = res.fetchall()
        if len(rows) == 1:
            return True
        return False

    def prepare_texts_and_metadatas(self):
        cursor = self.connection.cursor()
        result = cursor.execute("SELECT content, url FROM content")
        rows = result.fetchall()

        # based on Anyscale analysis (https://t.ly/yjgxQ), it looks like the
        # sweet spot is 700 chunk size and 50 chunk overlap
        text_splitter = CharacterTextSplitter(chunk_size=700, chunk_overlap=50)

        texts = []
        metadatas = []
        for row in rows:
            chunks = text_splitter.split_text(row["content"])
            chunk_metadatas = [{"url": row["url"]} for _ in chunks]
            texts += chunks
            metadatas += chunk_metadatas

        return texts, metadatas

    def similarity_search(self, *args, **kwargs):
        return self.vss.similarity_search(*args, **kwargs)