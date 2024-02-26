import pytest
import os
import os.path as op
import logging


@pytest.fixture(autouse=True)
def remove_created_database_after_test():
    """Fixture to execute asserts before and after a test is run"""
    # Setup logic
    yield   # this is where the testing happens
    # Teardown logic

    contentmap_db_path = op.join(op.dirname(__file__), "contentmap.db")
    if op.exists(contentmap_db_path):
        logging.info('Destroying mock sqlite content instance')
        os.remove(contentmap_db_path)

