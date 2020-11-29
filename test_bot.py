import pytest
from bot import potato
from typing import List
import os


class Context:
    """ Mock of telegram-bot's context """

    args: List[str] = []


@pytest.fixture
def context():
    return Context()


def test_potato(context):
    context.args = ["crab"]
    assert "crab" in potato(context)


def test_potato_no_args(context):
    result = potato(context)
    assert "potato" in result or "tomato" in result
