import os

import dotenv
import pytest
from dotenv import load_dotenv
import sys
import os

# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture(autouse=True)
def envs():
    dotenv.load_dotenv()


@pytest.fixture()
def app_url():
    return os.getenv("APP_URL")
