import os

import pyrogram.filters
import pyrogram.types
import tortoise.exceptions
from pyrogram import Client
from pyrogram.handlers import MessageHandler

import pytelebotter.orm
import pytelebotter.utils.types
from pytelebotter.randomizer.main import parse_and_randomize
from pytelebotter.telegram.channel_layer import channel_layer_setup
from pytelebotter.utils.logger import logger


async def generate_clients(
    accounts: pytelebotter.utils.types.AccountsConfig,
) -> list[Client]:
    logger.info("Logging into accounts")
    api_id = int(os.getenv("PYROGRAM_API_ID"))
    api_hash = os.getenv("PYROGRAM_API_HASH")

    clients = []
    for i in accounts["accounts"]:
        phone_number = str(i["number"])
        client = Client(
            f"account{phone_number}",
            api_id,
            api_hash,
            workdir="sessions/",
            phone_number=phone_number,
        )

        clients.append(client)
    return clients


async def setup_account(
    app: Client, index: int, config: pytelebotter.utils.types.Account
):
    list_of_channels = config["assigned_to"]
    text = config["reply_template"]["text"]
    logger.info(f"Setting up account {app.phone_number}")
    account = await app.get_me()

    if config.get("account_name", False):
        await app.update_profile(first_name=config["account_name"], last_name="")

    if config.get("account_description", False):
        await app.update_profile(
            bio=config["account_description"],
        )

    if not bool(config["channel_layer"]):
        logger.info(f"Skipping channel layer setup for account {app.phone_number}")
    elif not await pytelebotter.orm.ChannelLayer.exists(owner=account.id):
        await channel_layer_setup(app, account, index)

    try:
        channel_layer = await pytelebotter.orm.ChannelLayer.get(owner=account.id)
    except tortoise.exceptions.DoesNotExist:
        pass

    write_to: list[pytelebotter.utils.types.ChannelDictItem] = []
    for i in list_of_channels:
        chat = await app.get_chat(i)
        if list_of_channels and await pytelebotter.orm.ChannelLayer.exists(
            owner=account.id
        ):
            if send_as_chats := await app.get_send_as_chats(chat.linked_chat.id):
                send_as_chats = list(
                    filter(
                        lambda channel: channel["id"] == channel_layer.id, send_as_chats
                    )
                )[0]

            await app.set_send_as_chat(
                chat_id=chat.linked_chat.id, send_as_chat_id=send_as_chats["id"]
            )

        write_to.append(
            pytelebotter.utils.types.ChannelDictItem(
                channel=chat.id, linked_chat=chat.linked_chat.id
            )
        )

    app.add_handler(
        MessageHandler(
            Handler(text).auto_reply_peg,
            pyrogram.filters.chat([i["channel"] for i in write_to])
            & ~pyrogram.filters.create(lambda _, __, m: m.edit_date),
        )
    )


class Handler:
    def __init__(self, text):
        self.text = text

    async def auto_reply_peg(self, client: Client, message: pyrogram.types.Message):
        logger.info(
            f"Got a message from {message.chat.title} at account {client.phone_number}"
        )
        message_discussion = await client.get_discussion_message(
            message.chat.id, message.id
        )
        await message_discussion.reply(parse_and_randomize(self.text))
        logger.info(
            f"Sent a message to {message.chat.title} as account {client.phone_number}"
        )

    async def auto_reply_py(self, client: Client, message: pyrogram.types.Message):
        message_discussion = await client.get_discussion_message(
            message.chat.id, message.id
        )
        await message_discussion.reply(eval(f"f'{self.text}'"))
