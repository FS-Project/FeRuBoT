# INFO : ini merupakan copy source code dari repo one4ubot, dan sudah mendapatkan izin dari pemilik.
# INFO : This is a copy of the source code from the One4ubot repo, and has the permission of the owner.
# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#

import asyncio
from asyncio import sleep

from userbot import BOTLOG, BOTLOG_CHATID, CMD_HELP
from userbot.events import register


@register(outgoing=True, pattern="^.cspam (.*)")
async def leter_spam(cspammer):
    cspam = str(cspammer.pattern_match.group(1))
    message = cspam.replace(" ", "")
    await cspammer.delete()
    for letter in message:
        await cspammer.respond(letter)
    if BOTLOG:
        await cspammer.client.send_message(
            BOTLOG_CHATID, "#CSPAM\n" "TSpam was executed successfully"
        )


@register(outgoing=True, pattern="^.wspam (.*)")
async def word_spam(wspammer):
    wspam = str(wspammer.pattern_match.group(1))
    message = wspam.split()
    await wspammer.delete()
    for word in message:
        await wspammer.respond(word)
    if BOTLOG:
        await wspammer.client.send_message(
            BOTLOG_CHATID, "#WSPAM\n" "WSpam berhasil dijalankan"
        )


@register(outgoing=True, pattern="^.spam (.*)")
async def spammer(spamm):
    counter = int(spamm.pattern_match.group(1).split(" ", 1)[0])
    spam_message = str(spamm.pattern_match.group(1).split(" ", 1)[1])
    await spamm.delete()
    await asyncio.wait([spamm.respond(spam_message) for i in range(counter)])
    if BOTLOG:
        await spamm.client.send_message(
            BOTLOG_CHATID, "#SPAM\n" "Spam berhasil dijalankan"
        )


@register(outgoing=True, pattern="^.picspam")
async def tiny_pic_spam(pspam):
    message = pspam.text
    text = message.split()
    counter = int(text[1])
    link = str(text[2])
    await pspam.delete()
    for _ in range(1, counter):
        await pspam.client.send_file(pspam.chat_id, link)
    if BOTLOG:
        await pspam.client.send_message(
            BOTLOG_CHATID, "#SPAMGAMBAR\n" "SpamGambar berhasil dijalankan"
        )


@register(outgoing=True, pattern="^.delayspam (.*)")
async def dspammer(dspam):
    spamDelay = float(dspam.pattern_match.group(1).split(" ", 2)[0])
    counter = int(dspam.pattern_match.group(1).split(" ", 2)[1])
    spam_message = str(dspam.pattern_match.group(1).split(" ", 2)[2])
    await dspam.delete()
    for _ in range(1, counter):
        await dspam.respond(spam_message)
        await sleep(spamDelay)
    if BOTLOG:
        await dspam.client.send_message(
            BOTLOG_CHATID, "#DelaySPAM\n" "DelaySpam berhasil dijalankan"
        )


CMD_HELP.update(
    {
        "spam": ".cspam <teks>\
\nPenggunaan: Spam teks huruf demi huruf.\
\n\n.spam <jumlah <teks>\
\nPenggunaan: Membanjiri teks dalam obrolan !!\
\n\n.wspam <teks>\
\nPenggunaan: Spam teks kata demi kata.\
\n\n.picspam <jumlah> <link gambar/gif>\
\nPenggunaan: Seolah-olah teks spam tidak cukup !!\
\n\n.delayspam <delay> <jumlah> <teks>\
\nPenggunaan: .bigspam tetapi dengan penundaan khusus.\
\n\n\nINFO : Resiko Anda tanggung sendiri !!"
    }
)
