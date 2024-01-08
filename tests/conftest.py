import pytest
import os


@pytest.fixture(autouse=True)
def remove_created_database_after_test():
    """Fixture to execute asserts before and after a test is run"""
    # Setup logic
    yield   # this is where the testing happens
    # Teardown logic
    os.remove("contentmap.db")

