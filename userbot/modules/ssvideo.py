# INFO : ini merupakan copy source code dari repo one4ubot, dan sudah mendapatkan izin dari pemilik.
# INFO : This is a copy of the source code from the One4ubot repo, and has the permission of the owner.
# Copyright (C) 2020 Alfiananda P.A
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#

import asyncio
import os
import time

from telethon.tl.types import DocumentAttributeFilename
from userbot import CMD_HELP, bot
from userbot.events import register
from userbot.utils import progress


@register(outgoing=True, pattern=r"^\.ssvideo(?: |$)(.*)")
async def ssvideo(framecap):
    if not framecap.reply_to_msg_id:
        return await framecap.edit("`balas sebuah vidio!`")
    reply_message = await framecap.get_reply_message()
    if not reply_message.media:
        return await framecap.edit("`balas sebuah vidio!`")
    try:
        frame = int(framecap.pattern_match.group(1))
        if frame > 10:
            return await framecap.edit("`weyy..jangan terlalu banyak`")
    except BaseException:
        return await framecap.edit("`Harap masukkan jumlah frame!`")
    if (reply_message.photo
            or (DocumentAttributeFilename(file_name="AnimatedSticker.tgs")
                in reply_message.media.document.attributes)
            or (DocumentAttributeFilename(file_name="sticker.webp")
                in reply_message.media.document.attributes)
            ):
        return await framecap.edit("`File tidak support!`")
    c_time = time.time()
    await framecap.edit("`Mengunduh media...`")
    ss = await bot.download_media(
        reply_message,
        "anu.mp4",
        progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
            progress(d, t, framecap, c_time, "[DOWNLOAD]")
        ),
    )
    try:
        await framecap.edit("`Prosess...`")
        command = f"vcsi -g {frame}x{frame} {ss} -o ss.png "
        os.system(command)
        await framecap.client.send_file(
            framecap.chat_id,
            "ss.png",
            reply_to=framecap.reply_to_msg_id,
        )
        await framecap.delete()
    except BaseException as e:
        await framecap.edit(f"{e}")
    os.system("rm -rf *.png *.mp4")


CMD_HELP.update(
    {
        "ssvideo": ".ssvideo <grid>\
        \nPenggunaan: Tangkap frame vidio <grid> x <grid>.\
        \n*maksimal grid adalah 10."
    }
)
