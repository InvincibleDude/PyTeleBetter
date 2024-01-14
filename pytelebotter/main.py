import asyncio
import logging

from dotenv import load_dotenv
from pyrogram import idle
from tortoise import run_async

from pytelebotter.orm import tortoise_init
from pytelebotter.parser.main import parse_accounts_config
from pytelebotter.telegram.account import generate_clients, setup_account
from pytelebotter.utils.logger import logger


def main():
    load_dotenv()
    run_async(tortoise_init())

    async def main_internal():
        accounts = parse_accounts_config()

        clients = await generate_clients(accounts)

        for i, j in enumerate(clients):
            await j.start()
            account = accounts["accounts"][i]
            index = i + 1
            await setup_account(j, index, account)

        logger.info(
            f"Done setting up accounts. Now working with {len(clients)} accounts"
        )
        await idle()

        for app in clients:
            await app.stop()

    asyncio.run(main_internal())


if __name__ == "__main__":
    logging.getLogger("pyrogram").setLevel(logging.ERROR)
    logger.info("Setting up accounts")
    main()
