import pytest
from bot import Keys
import os


@pytest.fixture(scope="module")
def keys():
    print("setting keys!")
    os.environ["YELP_API_KEY"] = "yelp-api-key"
    os.environ["TELEGRAM_API_KEY"] = "telegram-api-key"
    os.environ["DARKSKY_API_KEY"] = "darksky-api-key"


def test_keys(keys):
    assert Keys.get_yelp() == "yelp-api-key"
    assert Keys.get_telegram() == "telegram-api-key"
    assert Keys.get_darksky() == "darksky-api-key"
