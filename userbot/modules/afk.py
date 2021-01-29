# INFO : ini merupakan copy source code dari repo one4ubot, dan sudah mendapatkan izin dari pemilik.
# INFO : This is a copy of the source code from the One4ubot repo, and has the permission of the owner.
# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot module which contains afk-related commands """

import time
from datetime import datetime
from random import choice, randint

from telethon.events import StopPropagation

from userbot import (
    AFKREASON,
    COUNT_MSG,
    CMD_HELP,
    ISAFK,
    BOTLOG,
    BOTLOG_CHATID,
    USERS,
    PM_AUTO_BAN)  # pylint: disable=unused-imports

from userbot.events import register

# ========================= CONSTANTS ============================
AFKSTR = [
    "Gua sibuk sekarang. Tolong bicara di dalam hati dan ketika saya kembali Anda bisa memberi saya itu!",
    "Saya pergi sekarang. Jika Anda butuh sesuatu, tinggalkan pesan setelah bunyi beep:\n`beeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeep`!",
    "Anda merindukan saya, lain kali bidik lebih baik.",
    "Saya akan kembali dalam beberapa menit dan jika tidak...,\ntunggu lebih lama.",
    "Saya tidak di sini sekarang, jadi saya mungkin di tempat lain. ",
    "Mawar itu merah, \nBiola itu biru, \nTinggalkan aku pesan, \nDan aku akan menghubungi kamu kembali.",
    "Terkadang hal terbaik dalam hidup layak untuk ditunggu… \nAku akan segera kembali.",
    "Aku akan segera kembali, \ntapi jika aku tidak segera kembali, \nAku akan kembali nanti.",
    "Jika kamu belum mengetahuinya, \nAku tidak di sini.",
    "Halo, selamat datang di pesan tandang saya, bagaimana saya bisa mengabaikan Anda hari ini?",
    "Saya berada di 7 lautan dan 7 negara, \n7 perairan dan 7 benua, \n7 gunung dan 7 bukit, \n7 dataran dan 7 gundukan, \n7 kolam dan 7 danau, \n7 mata air dan 7 padang rumput, \n7 kota dan 7 lingkungan, \n7 blok dan 7 rumah ... \n\nDi mana bahkan pesan Anda tidak bisa sampai ke saya! ",
    "Saya sedang tidak menggunakan keyboard saat ini, tetapi jika Anda akan berteriak cukup keras di layar, saya mungkin akan mendengar Anda.",
    "Saya pergi ke sana \n ---->",
    "Aku pergi ke sini \n <----",
    "Silakan tinggalkan pesan dan buat saya merasa lebih penting daripada sebelumnya.",
    "Saya tidak di sini jadi berhentilah menulis kepada saya, \nAnda juga tidak akan menemukan diri Anda dengan layar yang penuh dengan pesan Anda sendiri.",
    "Jika aku ada di sini, \nAku akan memberitahumu di mana aku berada. \n\nTapi aku tidak, \njadi tanya aku kapan aku kembali ...",
    "Aku pergi! \nAku tidak tahu kapan aku akan kembali! \nSemoga beberapa menit dari sekarang!",
    "Saya tidak ada saat ini jadi tolong tinggalkan nama, nomor, dan alamat Anda dan saya akan menguntit Anda nanti.",
    "Maaf, saya tidak di sini sekarang. \nJangan ragu untuk berbicara dengan userbot saya selama Anda suka. \nSaya akan menghubungi Anda lagi nanti.",
    "Saya yakin Anda mengharapkan pesan tandang!",
    "Hidup ini sangat singkat, begitu banyak hal yang harus dilakukan ... \nSaya akan melakukan salah satunya ..",
    "Aku tidak di sini sekarang ... \ntapi jika aku ... \n\nbukankah itu keren?",
]

global USER_AFK  # pylint:disable=E0602
global afk_time  # pylint:disable=E0602
global afk_start
global afk_end
USER_AFK = {}
afk_time = None
afk_start = {}

# =================================================================


@register(outgoing=True, pattern="^.afk(?: |$)(.*)", disable_errors=True)
async def set_afk(afk_e):
    """ Untuk memungkinkan Anda memberi tahu orang-orang bahwa Anda afk saat mereka mengirimi Anda pesan, gunakan perintah .afk,  """
    afk_e.text
    string = afk_e.pattern_match.group(1)
    global ISAFK
    global AFKREASON
    global USER_AFK  # pylint:disable=E0602
    global afk_time  # pylint:disable=E0602
    global afk_start
    global afk_end
    global reason
    USER_AFK = {}
    afk_time = None
    afk_end = {}
    start_1 = datetime.now()
    afk_start = start_1.replace(microsecond=0)
    if string:
        AFKREASON = string
        await afk_e.edit(
            f"Gua AFK Bro!\
        \nAlasan: `{string}`"
        )
    else:
        await afk_e.edit("Gua AFK Bro!")
    if BOTLOG:
        await afk_e.client.send_message(BOTLOG_CHATID, "#AFK\nKamu Telah AFK!")
    ISAFK = True
    afk_time = datetime.now()  # pylint:disable=E0602
    raise StopPropagation


@register(outgoing=True)
async def type_afk_is_not_true(notafk):
    """ This sets your status as not afk automatically when you write something while being afk """
    global ISAFK
    global COUNT_MSG
    global USERS
    global AFKREASON
    global USER_AFK  # pylint:disable=E0602
    global afk_time  # pylint:disable=E0602
    global afk_start
    global afk_end
    back_alive = datetime.now()
    afk_end = back_alive.replace(microsecond=0)
    if ISAFK:
        ISAFK = False
        msg = await notafk.respond("I'm no longer AFK.")
        time.sleep(3)
        await msg.delete()
        if BOTLOG:
            await notafk.client.send_message(
                BOTLOG_CHATID,
                "Kamu Mendapatkan Pesan "
                + str(COUNT_MSG)
                + " Pesan Dari  "
                + str(len(USERS))
                + " Pesan Saat Kamu AFK",
            )
            for i in USERS:
                if str(i).isnumeric():
                    name = await notafk.client.get_entity(i)
                    name0 = str(name.first_name)
                    await notafk.client.send_message(
                        BOTLOG_CHATID,
                        "[" + name0 + "](tg://user?id=" + str(i) + ")" +
                        " Mengirim Kamu " + "`" + str(USERS[i]) + " Pesan`",
                    )
                else:  # anon admin
                    await notafk.client.send_message(
                        BOTLOG_CHATID,
                        "Admin anonim di `" + i + "` mengirim kamu " + "`" +
                        str(USERS[i]) + " pesan`",
                    )
        COUNT_MSG = 0
        USERS = {}
        AFKREASON = None


@register(incoming=True, disable_edited=True)
async def mention_afk(mention):
    """ This function takes care of notifying the people who mention you that you are AFK."""
    global COUNT_MSG
    global USERS
    global ISAFK
    global USER_AFK  # pylint:disable=E0602
    global afk_time  # pylint:disable=E0602
    global afk_start
    global afk_end
    back_alivee = datetime.now()
    afk_end = back_alivee.replace(microsecond=0)
    afk_since = "Beberapa saat yang lalu...."
    if ISAFK and mention.message.mentioned:
            now = datetime.now()
            datime_since_afk = now - afk_time  # pylint:disable=E0602
            time = float(datime_since_afk.seconds)
            days = time // (24 * 3600)
            time = time % (24 * 3600)
            hours = time // 3600
            time %= 3600
            minutes = time // 60
            time %= 60
            seconds = time
            if days == 1:
                afk_since = "Kemarin"
            elif days > 1:
                if days > 6:
                    date = now + datetime.timedelta(
                        days=-days, hours=-hours, minutes=-minutes
                    )
                    afk_since = date.strftime("%A, %Y %B %m, %H:%I")
                else:
                    wday = now + datetime.timedelta(days=-days)
                    afk_since = wday.strftime("%A")
            elif hours > 1:
                afk_since = f"`{int(hours)}jam{int(minutes)}` lalu"
            elif minutes > 0:
                afk_since = f"`{int(minutes)}menit{int(seconds)}` lalu"
            else:
                afk_since = f"`{int(seconds)}detik` lalu"
            
            is_bot = False
            if (sender := await mention.get_sender()):
                is_bot = sender.bot
                if is_bot: return  # ignore bot

            chat_obj = await mention.client.get_entity(mention.chat_id)
            chat_title = chat_obj.title

            if mention.sender_id not in USERS or chat_title not in USERS:
                if AFKREASON:
                    await mention.reply(
                        f"Saya AFK sejak {afk_since}.\
                        \nAlasan: `{AFKREASON}`"
                    )
                else:
                    await mention.reply(str(choice(AFKSTR)))
                if mention.sender_id is not None:
                    USERS.update({mention.sender_id: 1})
                else:
                    USERS.update({chat_title: 1})
            else:
                if USERS[mention.sender_id] % randint(2, 4) == 0:
                    if AFKREASON:
                        await mention.reply(
                            f"Saya masih AFK sejak {afk_since}.\
                            \nAlasan: `{AFKREASON}`"
                        )
                    else:
                        await mention.reply(str(choice(AFKSTR)))
                    if mention.sender_id is not None:
                        USERS[mention.sender_id] += 1
                    else:
                        USERS[chat_title] += 1
                COUNT_MSG += 1


@register(incoming=True, disable_errors=True)
async def afk_on_pm(sender):
    """ Function which informs people that you are AFK in PM """
    global ISAFK
    global USERS
    global COUNT_MSG
    global COUNT_MSG
    global USERS
    global ISAFK
    global USER_AFK  # pylint:disable=E0602
    global afk_time  # pylint:disable=E0602
    global afk_start
    global afk_end
    back_alivee = datetime.now()
    afk_end = back_alivee.replace(microsecond=0)
    afk_since = "Beberapa saat yang lalu"
    if (
        sender.is_private
        and sender.sender_id != 777000
        and not (await sender.get_sender()).bot
    ):
        if PM_AUTO_BAN:
            try:
                from userbot.modules.sql_helper.pm_permit_sql import is_approved

                apprv = is_approved(sender.sender_id)
            except AttributeError:
                apprv = True
        else:
            apprv = True
        if apprv and ISAFK:
            now = datetime.now()
            datime_since_afk = now - afk_time  # pylint:disable=E0602
            time = float(datime_since_afk.seconds)
            days = time // (24 * 3600)
            time = time % (24 * 3600)
            hours = time // 3600
            time %= 3600
            minutes = time // 60
            time %= 60
            seconds = time
            if days == 1:
                afk_since = "Kemarin"
            elif days > 1:
                if days > 6:
                    date = now + datetime.timedelta(
                        days=-days, hours=-hours, minutes=-minutes
                    )
                    afk_since = date.strftime("%A, %Y %B %m, %H:%I")
                else:
                    wday = now + datetime.timedelta(days=-days)
                    afk_since = wday.strftime("%A")
            elif hours > 1:
                afk_since = f"`{int(hours)}jam{int(minutes)}` lalu"
            elif minutes > 0:
                afk_since = f"`{int(minutes)}menit{int(seconds)}` lalu"
            else:
                afk_since = f"`{int(seconds)}detik` lalu"
            if sender.sender_id not in USERS:
                if AFKREASON:
                    await sender.reply(
                        f"Saya AFK Sejak {afk_since}.\
                        \nAlasan: `{AFKREASON}`"
                    )
                else:
                    await sender.reply(str(choice(AFKSTR)))
                USERS.update({sender.sender_id: 1})
                COUNT_MSG = COUNT_MSG + 1
            elif apprv and sender.sender_id in USERS:
                if USERS[sender.sender_id] % randint(2, 4) == 0:
                    if AFKREASON:
                        await sender.reply(
                            f"Saya masih AFK sejak {afk_since}.\
                            \nAlasan: `{AFKREASON}`"
                        )
                    else:
                        await sender.reply(str(choice(AFKSTR)))
                    USERS[sender.sender_id] = USERS[sender.sender_id] + 1
                    COUNT_MSG = COUNT_MSG + 1
                else:
                    USERS[sender.sender_id] = USERS[sender.sender_id] + 1
                    COUNT_MSG = COUNT_MSG + 1


CMD_HELP.update(
    {
        "afk": ".afk [Alasan Optional]\
\nDigunakan: Menetapkan Anda sebagai afk.\nBalasan untuk siapa saja yang tag / PM \
Anda memberi tahu mereka bahwa Anda AFK (alasan).\n\nUntuk Mematikan AFK Anda hanya mengetik kembali apa pun, di mana pun.\
"
    }
)
