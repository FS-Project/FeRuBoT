# INFO : ini merupakan copy source code dari repo one4ubot, dan sudah mendapatkan izin dari pemilik.
# INFO : This is a copy of the source code from the One4ubot repo, and has the permission of the owner.
# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot module containing userid, chatid and log commands"""

from asyncio import sleep

from userbot import BOTLOG, BOTLOG_CHATID, CMD_HELP, bot
from userbot.events import register
from userbot.modules.admin import get_user_from_event


@register(outgoing=True, pattern="^.userid$")
async def useridgetter(target):
    """ Untuk mengembalikan ID pengguna target, Gunakan .userid . """
    message = await target.get_reply_message()
    if message:
        if not message.forward:
            user_id = message.sender.id
            if message.sender.username:
                name = "@" + message.sender.username
            else:
                name = "**" + message.sender.first_name + "**"
        else:
            user_id = message.forward.sender.id
            if message.forward.sender.username:
                name = "@" + message.forward.sender.username
            else:
                name = "*" + message.forward.sender.first_name + "*"
        await target.edit("**Nama:** {} \n**ID Pengguna:** `{}`".format(name, user_id))


@register(outgoing=True, pattern="^.link(?: |$)(.*)")
async def permalink(mention):
    """ Untuk perintah .link, menghasilkan tautan ke PM pengguna dengan teks kustom. """
    user, custom = await get_user_from_event(mention)
    if not user:
        return
    if custom:
        await mention.edit(f"[{custom}](tg://user?id={user.id})")
    else:
        tag = (
            user.first_name.replace("\u2060", "") if user.first_name else user.username
        )
        await mention.edit(f"[{tag}](tg://user?id={user.id})")


@register(outgoing=True, pattern="^.chatid$")
async def chatidgetter(chat):
    """ Untuk .chatid, kembalikan ID obrolan yang Anda masuki saat itu. """
    await chat.edit("ID Pesan: `" + str(chat.chat_id) + "`")


@register(outgoing=True, pattern=r"^.log(?: |$)([\s\S]*)")
async def log(log_text):
    """ Untuk perintah .log, meneruskan pesan atau argumen perintah ke grup log botp """
    if BOTLOG:
        if log_text.reply_to_msg_id:
            reply_msg = await log_text.get_reply_message()
            await reply_msg.forward_to(BOTLOG_CHATID)
        elif log_text.pattern_match.group(1):
            user = f"#LOG / ID Pesan: {log_text.chat_id}\n\n"
            textx = user + log_text.pattern_match.group(1)
            await bot.send_message(BOTLOG_CHATID, textx)
        else:
            await log_text.edit("`Apa yang harus saya catat?`")
            return
        await log_text.edit("`Berhasil Dicatat`")
    else:
        await log_text.edit("`Fitur ini membutuhkan Logging untuk diaktifkan!`")
    await sleep(2)
    await log_text.delete()


@register(outgoing=True, pattern="^.kickme$")
async def kickme(leave):
    """ Pada dasarnya ini adalah perintah .kickme """
    await leave.edit("Tidak, tidak, tidak, aku pergi")
    await leave.client.kick_participant(leave.chat_id, "me")


@register(outgoing=True, pattern="^.unmutechat$")
async def unmute_chat(unm_e):
    """ Untuk perintah .unmutechat, aktifkan obrolan yang dimute. """
    try:
        from userbot.modules.sql_helper.keep_read_sql import unkread
    except AttributeError:
        await unm_e.edit("`Berjalan di Mode Non-SQL!`")
        return
    unkread(str(unm_e.chat_id))
    await unm_e.edit("```Berhasil mengaktifkan obrolan ini```")
    await sleep(2)
    await unm_e.delete()


@register(outgoing=True, pattern="^.mutechat$")
async def mute_chat(mute_e):
    """ Untuk perintah .mutechat, nonaktifkan obrolan apa pun. """
    try:
        from userbot.modules.sql_helper.keep_read_sql import kread
    except AttributeError:
        await mute_e.edit("`Berjalan di Mode Non-SQL!`")
        return
    await mute_e.edit(str(mute_e.chat_id))
    kread(str(mute_e.chat_id))
    await mute_e.edit("`Shush! Obrolan ini akan dibisukan!`")
    await sleep(2)
    await mute_e.delete()
    if BOTLOG:
        await mute_e.client.send_message(
            BOTLOG_CHATID, str(mute_e.chat_id) + " Sudah dibisukan."
        )


@register(incoming=True, disable_errors=True)
async def keep_read(message):
    """ Logika bisu. """
    try:
        from userbot.modules.sql_helper.keep_read_sql import is_kread
    except AttributeError:
        return
    kread = is_kread()
    if kread:
        for i in kread:
            if i.groupid == str(message.chat_id):
                await message.client.send_read_acknowledge(message.chat_id)


# Regex-Ninja module by @Kandnub
regexNinja = False


@register(outgoing=True, pattern="^s/")
async def sedNinja(event):
    """Untuk modul regex-ninja, perintah hapus otomatis dimulai dengan s/"""
    if regexNinja:
        await sleep(0.5)
        await event.delete()


@register(outgoing=True, pattern="^.regexninja (on|off)$")
async def sedNinjaToggle(event):
    """ Mengaktifkan atau menonaktifkan modul ninja regex. """
    global regexNinja
    if event.pattern_match.group(1) == "on":
        regexNinja = True
        await event.edit("`Berhasil mengaktifkan mode ninja untuk Regexbot.`")
        await sleep(1)
        await event.delete()
    elif event.pattern_match.group(1) == "off":
        regexNinja = False
        await event.edit("`Berhasil menonaktifkan mode ninja untuk Regexbot.`")
        await sleep(1)
        await event.delete()


CMD_HELP.update(
    {
        "chat": ".chatid\
\nPenggunaan: Mengambil ID obrolan saat ini\
\n\n.userid\
\nPenggunaan: Mengambil ID pengguna sebagai balasan, jika ini adalah pesan yang diteruskan, menemukan ID untuk sumbernya.\
\n\n.log\
\nPenggunaan: Meneruskan pesan yang telah Anda balas di grup log bot Anda.\
\n\n.kickme\
\nPenggunaan: Keluar dari grup target.\
\n\n.unmutechat\
\nPenggunaan: Membisukan obrolan yang dibisukan.\
\n\n.mutechat\
\nPenggunaan: Memungkinkan Anda membisukan obrolan apa pun.\
\n\n.link <username/userid> : <optional text> (or) reply to someone's message with .link <optional text>\
\nPenggunaan: Buat tautan permanen ke profil pengguna dengan teks kustom opsional.\
\n\n.regexninja on/off\
\nPenggunaan: Mengaktifkan / menonaktifkan modul ninja regex secara global.\
\nModul Regex Ninja membantu menghapus pesan pemicu bot regex."
    }
)
