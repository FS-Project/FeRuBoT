# INFO : ini merupakan copy source code dari repo one4ubot, dan sudah mendapatkan izin dari pemilik.
# INFO : This is a copy of the source code from the One4ubot repo, and has the permission of the owner.
# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
# The entire source code is OSSRPL except 'screencapture' which is MPL
# License: MPL and OSSRPL

import io
from asyncio import sleep
from re import match

from userbot import CMD_HELP
from userbot.events import register
from userbot.utils import chrome, options


@register(pattern="^.ss (.*)", outgoing=True)
async def capture(url):
    """ For .ss command, capture a website's screenshot and send the photo. """
    await url.edit("`Sedang proses...`")
    chrome_options = await options()
    chrome_options.add_argument("--test-type")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.arguments.remove("--window-size=1920x1080")
    driver = await chrome(chrome_options=chrome_options)
    input_str = url.pattern_match.group(1)
    link_match = match(r"\bhttps?://.*\.\S+", input_str)
    if link_match:
        link = link_match.group()
    else:
        return await url.edit("`Saya memerlukan tautan yang valid untuk mengambil tangkapan layar.`")
    driver.get(link)
    height = driver.execute_script(
        "return Math.max(document.body.scrollHeight, document.body.offsetHeight, "
        "document.documentElement.clientHeight, document.documentElement.scrollHeight, "
        "document.documentElement.offsetHeight);"
    )
    width = driver.execute_script(
        "return Math.max(document.body.scrollWidth, document.body.offsetWidth, "
        "document.documentElement.clientWidth, document.documentElement.scrollWidth, "
        "document.documentElement.offsetWidth);"
    )
    driver.set_window_size(width + 125, height + 125)
    wait_for = height / 1000
    await url.edit(
        "`Menghasilkan screenshot page...`"
        f"\n`Tinggi halaman = {height}px`"
        f"\n`Lebar halaman = {width}px`"
        f"\n`Menunggu ({int(wait_for)}s) untuk memuat halaman.`"
    )
    await sleep(int(wait_for))
    im_png = driver.get_screenshot_as_png()
    # saves screenshot of entire page
    driver.quit()
    message_id = url.message.id
    if url.reply_to_msg_id:
        message_id = url.reply_to_msg_id
    with io.BytesIO(im_png) as out_file:
        out_file.name = "screencapture.png"
        await url.edit("`Mengupload screenshot sebagai file..`")
        await url.client.send_file(
            url.chat_id,
            out_file,
            caption=input_str,
            force_document=True,
            reply_to=message_id,
        )
        await url.delete()


CMD_HELP.update(
    {
        "ss": ".ss <url>\
    \nPenggunaan: Mengambil tangkapan layar dari situs web dan mengirimkan tangkapan layar .\
    \nContoh url yang bisa dipakai : `https://www.google.com`"
    }
)
