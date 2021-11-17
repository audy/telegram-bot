import os
from typing import List

import pytest

from bot import eval_command, potato


class Context:
    """Mock of telegram-bot's context"""

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


def test_eval(context):
    context.args = "var x = { result: 5 + 5 }; x.result".split()
    result = eval_command(context)
    assert result == "10"


def test_eval_does_not_compute(context):
    context.args = ["asdfadfadf"]
    result = eval_command(context)
    assert result == "Does not compute 👾💩🔥"


def test_eval_strings(context):
    context.args = ["‘test’'.repeat(5)"]
    result = eval_command(context)
    assert result == "testtesttesttesttest"
