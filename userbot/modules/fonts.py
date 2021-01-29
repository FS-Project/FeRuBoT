# INFO : ini merupakan copy source code dari repo one4ubot, dan sudah mendapatkan izin dari pemilik.
# INFO : This is a copy of the source code from the One4ubot repo, and has the permission of the owner.
# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
# This module is maked by Project TESLA

from userbot import CMD_HELP
from userbot.events import register

normiefont = [
    "a",
    "b",
    "c",
    "d",
    "e",
    "f",
    "g",
    "h",
    "i",
    "j",
    "k",
    "l",
    "m",
    "n",
    "o",
    "p",
    "q",
    "r",
    "s",
    "t",
    "u",
    "v",
    "w",
    "x",
    "y",
    "z",
]
weebyfont = [
    "卂",
    "乃",
    "匚",
    "刀",
    "乇",
    "下",
    "厶",
    "卄",
    "工",
    "丁",
    "长",
    "乚",
    "从",
    "𠘨",
    "口",
    "尸",
    "㔿",
    "尺",
    "丂",
    "丅",
    "凵",
    "リ",
    "山",
    "乂",
    "丫",
    "乙",
]
circlyfont = [
    "🅐",
    "🅑",
    "🅒",
    "🅓",
    "🅔",
    "🅕",
    "🅖",
    "🅗",
    "🅘",
    "🅙",
    "🅚",
    "🅛",
    "🅜",
    "🅝",
    "🅞",
    "🅟",
    "🅠",
    "🅡",
    "🅢",
    "🅣",
    "🅤",
    "🅥",
    "🅦",
    "🅧",
    "🅨",
    "🅩",
]
oldengfont = [
    "𝔄",
    "𝔅",
    "ℭ",
    "𝔇",
    "𝔈",
    "𝔉",
    "𝔊",
    "ℌ",
    "ℑ",
    "𝔍",
    "𝔎",
    "𝔏",
    "𝔐",
    "𝔑",
    "𝔒",
    "𝔓",
    "𝔔",
    "ℜ",
    "𝔖",
    "𝔗",
    "𝔘",
    "𝔙",
    "𝔚",
    "𝔛",
    "𝔜",
    "ℨ",
]


@register(outgoing=True, pattern="^.weebify(?: |$)(.*)")
async def weebify(event):

    args = event.pattern_match.group(1)
    if not args:
        get = await event.get_reply_message()
        args = get.text
    if not args:
        await event.edit("`Apaaa, Saya Seharusnya merubah teksmu`")
        return
    string = "  ".join(args).lower()
    for normiecharacter in string:
        if normiecharacter in normiefont:
            weebycharacter = weebyfont[normiefont.index(normiecharacter)]
            string = string.replace(normiecharacter, weebycharacter)
    await event.edit(string)


@register(outgoing=True, pattern="^.circlify(?: |$)(.*)")
async def circly(event):

    args = event.pattern_match.group(1)
    if not args:
        get = await event.get_reply_message()
        args = get.text
    if not args:
        await event.edit("`Apaaa, Saya Seharusnya me lingkari teksmu`")
        return
    string = "  ".join(args).lower()
    for normiecharacter in string:
        if normiecharacter in normiefont:
            circlycharacter = circlyfont[normiefont.index(normiecharacter)]
            string = string.replace(normiecharacter, circlycharacter)
    await event.edit(string)


@register(outgoing=True, pattern="^.oldeng(?: |$)(.*)")
async def oldy(event):

    args = event.pattern_match.group(1)
    if not args:
        get = await event.get_reply_message()
        args = get.text
    if not args:
        await event.edit("`Apaaa, Saya Seharusnya Bekerja dengan teks saja`")
        return
    string = "  ".join(args).lower()
    for normiecharacter in string:
        if normiecharacter in normiefont:
            oldycharacter = oldengfont[normiefont.index(normiecharacter)]
            string = string.replace(normiecharacter, oldycharacter)
    await event.edit(string)


CMD_HELP.update(
    {
        "fonts": ".weebify :- weebifys your text \
\n.circlify :- melingkari teks \
\n.oldeng :- font inggris tua"
    }
)
