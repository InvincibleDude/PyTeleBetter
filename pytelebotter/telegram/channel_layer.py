import os
import random

import pyrogram
import regex
from pyrogram.types import InputMediaPhoto

import pytelebotter.orm
from pytelebotter.parser.main import parse_accounts_config
from pytelebotter.utils.logger import logger


async def channel_layer_setup(
    app: pyrogram.Client, user_data: pyrogram.types.User, index: int
):
    # TODO
    logger.info(
        f"Channel layer for {app.phone_number} does not exists. Creating a new one"
    )
    layer_config = parse_accounts_config()["accounts"][index - 1]["channel_layer"]
    # (all|{index}) - chooses a photos that are assigned to all (0) or to specific account ({index})
    # (pfp|clp|ptsw):
    #   pfp - profile picture
    #   clprofile - channel layer profile picture
    #   clpost - channel layer profile post pics
    # ([0-9]) - index of photo (e.g. [0_ptsw_1.jpg, 0_ptsw_2.jpg])
    compiled_regex = regex.compile(
        rf"(all|{index})_(pfp|clprofile|clpost|ptsw)_(\d)(?>.)(png|jpg)"
    )

    channel = None
    try:
        # noinspection PyTypeChecker
        scandir_res: list[os.DirEntry] = list(os.scandir("images"))
        files = [i.name for i in scandir_res if compiled_regex.fullmatch(i.name)]

        logger.info(f"Account {app.phone_number} doesn't exist in DB. Adding it")
        channel = await app.create_channel(
            layer_config["name"], layer_config["description"]
        )

        try:
            await channel.set_photo(
                f"images/{[i for i in files if 'clprofile' in i][-1]}"
            )
        except IndexError:
            raise Exception("no clprofile image")

        media = [InputMediaPhoto(f"images/{i}") for i in files if "clpost" in i]

        try:
            media[0].caption = layer_config["caption"]
        except IndexError:
            raise Exception("no clpost images")

        text_id = f"{layer_config['name'].replace(' ', '_')}{random.randint(0, 10000)}"

        await app.send_media_group(channel.id, media)
        await app.update_chat_username(channel.id, text_id)

        logger.info(f"Saving channel layer for {app.phone_number} into the DB")
        channel_in_db = await pytelebotter.orm.ChannelLayer(
            id=channel.id, owner=user_data.id, text_id=text_id
        )

        await channel_in_db.save()
    except Exception as e:
        if channel is not None:
            await app.delete_channel(channel.id)

        logger.error(f"{e}")
        logger.error(
            "Something went wrong and the newly created channel-layer was deleted"
        )
