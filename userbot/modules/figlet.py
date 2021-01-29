# INFO : ini merupakan copy source code dari repo one4ubot, dan sudah mendapatkan izin dari pemilik.
# INFO : This is a copy of the source code from the One4ubot repo, and has the permission of the owner.
# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
# Port to UserBot by @MoveAngel

import pyfiglet

from userbot import CMD_HELP
from userbot.events import register


@register(outgoing=True, pattern=r"^\.figlet(?: |$)(.*)")
async def figlet(fg):
    if fg.fwd_from:
        return
    CMD_FIG = {
        "slant": "slant",
        "3D": "3-d",
        "5line": "5lineoblique",
        "alpha": "alphabet",
        "banner": "banner3-D",
        "doh": "doh",
        "iso": "isometric1",
        "letter": "letters",
        "allig": "alligator",
        "dotm": "dotmatrix",
        "bubble": "bubble",
        "bulb": "bulbhead",
        "digi": "digital",
    }
    input_str = fg.pattern_match.group(1)
    if "." in input_str:
        text, cmd = input_str.split(".", maxsplit=1)
    elif input_str is not None:
        cmd = None
        text = input_str
    else:
        await fg.edit("`Harap tambahkan beberapa teks ke figlet`")
        return
    if cmd is not None:
        try:
            font = CMD_FIG[cmd]
        except KeyError:
            await fg.edit("`Font yang dipilih tidak valid.`")
            return
        result = pyfiglet.figlet_format(text, font=font)
    else:
        result = pyfiglet.figlet_format(text)
    await fg.respond("‌‌‎`{}`".format(result))
    await fg.delete()


CMD_HELP.update(
    {
        "figlet": ".figlet"
        "\nPenggunaan: Mengubah teks ke beberapa gaya."
        "\n\nExample: `.figlet <Gaya Teks>`"
        "\nDAFTAR GAYA: `slant`, `3D`, `5line`, `alpha`, `banner`, `doh`, `iso`, `letter`, `allig`, `dotm`, `bubble`, `bulb`, `digi`"
    }
)
