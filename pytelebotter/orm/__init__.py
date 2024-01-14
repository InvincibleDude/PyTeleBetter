import os

from tortoise import Tortoise

from pytelebotter.orm.models import *


async def tortoise_init():
    await Tortoise.init(
        config={
            "connections": {
                "default": {
                    "engine": "tortoise.backends.sqlite",
                    "credentials": {"file_path": "db.sqlite3"},
                },
            },
            "apps": {
                "models": {
                    "models": ["pytelebotter.orm.models"],
                    "default_connection": "default",
                }
            },
        }
    )

    if "TESTING_ENV" in os.environ:
        os.remove("db.sqlite3")
    await Tortoise.generate_schemas(safe=True)
