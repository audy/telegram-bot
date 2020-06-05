# Telegram Bot
[![test](https://github.com/audy/telegram-bot/workflows/tests/badge.svg)](https://github.com/audy/telegram-bot/actions)
[![deploy](https://github.com/audy/telegram-bot/workflows/deploy/badge.svg)](https://github.com/audy/telegram-bot/actions)

I'm a bot! on Telegram!
[Contributors](https://github.com/audy/telegram-bot/graphs/contributors)

## Adding New Commands

To add a command, edit `bot.py` and add a function that returns a string:

```python
import random

@bot.responds_to("hello")
def hello():
    """ returns a greeting """
    return random.sample(["Hola", "Hallo", "Hello", "Salut"])
```

That's it!

## Deployment

This repository will automatically deploy to production if you push/merge to
the `master` branch. To fix/modify the bot, [submit a pull
request](https://github.com/audy/telegram-bot/pull/new/master).

## Testing

`pytest -vv`
