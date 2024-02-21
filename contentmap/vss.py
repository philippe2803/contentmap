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

    def load(self):
        # content table must be there
        assert self.table_exists(table_name="content")

        embedding_function = SentenceTransformerEmbeddings(
            model_name="all-MiniLM-L6-v2"
        )
        vss = SQLiteVSS(
            table="content_chunks",
            embedding=embedding_function,
            connection=self.connection
        )
        return vss

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
