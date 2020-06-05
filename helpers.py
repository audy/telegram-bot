import random


def humanized_list(items):
    """convert a list of items into something that could go into an English sentence"""
    if len(items) == 1:
        return items[0]
    else:
        return ", ".join(items[:1]) + f" & {items[-1]}"


def get_movement_action() -> str:
    return random.choice(
        [
            "take a trip to",
            "head on over to",
            "walk on down to",
            "make a quick jaunt to",
            "find yourself in",
            "ride the bus to",
            "have a nice bike ride over to",
        ]
    )
