# INFO : ini merupakan copy source code dari repo one4ubot, dan sudah mendapatkan izin dari pemilik.
# INFO : This is a copy of the source code from the One4ubot repo, and has the permission of the owner.
# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
# You can find misc modules, which dont fit in anything xD
""" Userbot module for other small commands. """

import io
import sys
from os import execl
from random import randint
from time import sleep

from userbot import BOTLOG, BOTLOG_CHATID, CMD_HELP, bot
from userbot.events import register
from userbot.utils import time_formatter


@register(outgoing=True, pattern="^.random")
async def randomise(items):
    """ For .random command, get a random item from the list of items. """
    itemo = (items.text[8:]).split()
    if len(itemo) < 2:
        await items.edit(
            "`2 item atau lebih diperlukan! Periksa .help random untuk info lebih lanjut.`"
        )
        return
    index = randint(1, len(itemo) - 1)
    await items.edit(
        "**Query: **\n`" + items.text[8:] + "`\n**Output: **\n`" + itemo[index] + "`"
    )


@register(outgoing=True, pattern="^.sleep ([0-9]+)$")
async def sleepybot(time):
    """ For .sleep command, let the userbot snooze for a few second. """
    counter = int(time.pattern_match.group(1))
    await time.edit("`Saya merajuk dan tertidur...`")
    if BOTLOG:
        str_counter = time_formatter(counter)
        await time.client.send_message(
            BOTLOG_CHATID,
            f"Anda sudah membuat bot untuk tidur💤 {str_counter}.",
        )
    sleep(counter)
    await time.edit("`Oke, saya sudah bangun sekarang.`")


@register(outgoing=True, pattern="^.shutdown$")
async def killbot(shut):
    """For .shutdown command, shut the bot down."""
    await shut.edit("`Selamat tinggal *Suara shutdown Windows XP*....`")
    if BOTLOG:
        await shut.client.send_message(BOTLOG_CHATID, "#SHUTDOWN \n" "Bot sudah meninggal, hidupkan lagi ")
    await bot.disconnect()


@register(outgoing=True, pattern="^.restart$")
async def killdabot(reboot):
    await reboot.edit("`*saya akan kembali sebentar lagi*`")
    if BOTLOG:
        await reboot.client.send_message(BOTLOG_CHATID, "#RESTART \n" "Bot di nyalakan ulang")
    await bot.disconnect()
    # Spin a new instance of bot
    execl(sys.executable, sys.executable, *sys.argv)
    # Shut the existing one down
    exit()


# Copyright (c) Gegham Zakaryan | 2019
@register(outgoing=True, pattern="^.repeat (.*)")
async def repeat(rep):
    cnt, txt = rep.pattern_match.group(1).split(" ", 1)
    replyCount = int(cnt)
    toBeRepeated = txt

    replyText = toBeRepeated + "\n"

    for i in range(0, replyCount - 1):
        replyText += toBeRepeated + "\n"

    await rep.edit(replyText)


@register(outgoing=True, pattern="^.repo$")
async def repo_is_here(wannasee):
    """ For .repo command, just returns the repo URL. """
    await wannasee.edit(
        "[🔗Sentuh ini](https://github.com/FS-Project/FeRuBoT) untuk membuka repo FeRuBoT."
    )


@register(outgoing=True, pattern="^.raw$")
async def raw(rawtext):
    the_real_message = None
    reply_to_id = None
    if rawtext.reply_to_msg_id:
        previous_message = await rawtext.get_reply_message()
        the_real_message = previous_message.stringify()
        reply_to_id = rawtext.reply_to_msg_id
    else:
        the_real_message = rawtext.stringify()
        reply_to_id = rawtext.message.id
    with io.BytesIO(str.encode(the_real_message)) as out_file:
        out_file.name = "raw_message_data.txt"
        await rawtext.edit("`Periksa log userbot untuk data pesan yang didekodekan!!`")
        await rawtext.client.send_file(
            BOTLOG_CHATID,
            out_file,
            force_document=True,
            allow_cache=False,
            reply_to=reply_to_id,
            caption="`Berikut data pesan yang diterjemahkan!!`",
        )


CMD_HELP.update(
    {
        "random": ".random <item1> <item2> ... <itemN>\
\nPenggunaan: Dapatkan item acak dari daftar item."
    }
)

CMD_HELP.update(
    {
        "sleep": ".sleep <seconds>\
\nPenggunaan: Userbot juga lelah. Biarkan punyamu tertidur selama beberapa detik💤."
    }
)

CMD_HELP.update(
    {
        "shutdown": ".shutdown\
\nPenggunaan: Terkadang Anda perlu mematikan bot Anda. Terkadang Anda hanya berharap\
mendengar suara shutdown Windows XP ... tetapi Anda tidak melakukannya."
    }
)

CMD_HELP.update(
    {
        "repo": ".repo\
\nPenggunaan: Jika Anda penasaran dengan apa yang membuat userbot bekerja, inilah yang Anda butuhkan."
    }
)

CMD_HELP.update(
    {
        "readme": ".readme\
\nPenggunaan: Berikan tautan untuk menyiapkan bot pengguna dan modulnya."
    }
)

CMD_HELP.update(
    {
        "repeat": ".repeat <no.> <text>\
\nPenggunaan: Mengulangi teks beberapa kali. Jangan bingung ini dengan spam."
    }
)

CMD_HELP.update(
    {
        "restart": ".restart\
\nPenggunaan: Mulai ulang bot!!"
    }
)

CMD_HELP.update(
    {
        "raw": ".raw\
\nPenggunaan: Dapatkan data rinci yang diformat seperti JSON tentang pesan yang dibalas."
    }
)
