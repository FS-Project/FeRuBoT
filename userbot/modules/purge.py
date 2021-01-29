# INFO : ini merupakan copy source code dari repo one4ubot, dan sudah mendapatkan izin dari pemilik.
# INFO : This is a copy of the source code from the One4ubot repo, and has the permission of the owner.
# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot module for purging unneeded messages(usually spam or ot). """

from asyncio import sleep

from telethon.errors import rpcbaseerrors

from userbot import BOTLOG, BOTLOG_CHATID, CMD_HELP
from userbot.events import register


@register(outgoing=True, pattern="^.purge$")
async def fastpurger(purg):
    """ For .purge command, purge all messages starting from the reply. """
    chat = await purg.get_input_chat()
    msgs = []
    itermsg = purg.client.iter_messages(chat, min_id=purg.reply_to_msg_id)
    count = 0

    if purg.reply_to_msg_id is not None:
        async for msg in itermsg:
            msgs.append(msg)
            count = count + 1
            msgs.append(purg.reply_to_msg_id)
            if len(msgs) == 100:
                await purg.client.delete_messages(chat, msgs)
                msgs = []
    else:
        await purg.edit("`Saya perlu pesan untuk mulai membersihkan.`")
        return

    if msgs:
        await purg.client.delete_messages(chat, msgs)
    done = await purg.client.send_message(
        purg.chat_id,
        f"`Pembersihan cepat selesai!`\
        \nMembersihkan {str(count)} pesan",
    )

    if BOTLOG:
        await purg.client.send_message(
            BOTLOG_CHATID, "Pembersihan " + str(count) + " pesan berhasil diselesaikan."
        )
    await sleep(2)
    await done.delete()


@register(outgoing=True, pattern="^.purgeme")
async def purgeme(delme):
    """ For .purgeme, delete x count of your latest message."""
    message = delme.text
    count = int(message[9:])
    i = 1

    async for message in delme.client.iter_messages(delme.chat_id, from_user="me"):
        if i > count + 1:
            break
        i = i + 1
        await message.delete()

    smsg = await delme.client.send_message(
        delme.chat_id,
        "`Pembersihan selesai!` Purged " + str(count) + " pesan.",
    )
    if BOTLOG:
        await delme.client.send_message(
            BOTLOG_CHATID, "Pembersihan " + str(count) + " pesan berhasil diselesaikan."
        )
    await sleep(2)
    i = 1
    await smsg.delete()


@register(outgoing=True, pattern="^.del$")
async def delete_it(delme):
    """ For .del command, delete the replied message. """
    msg_src = await delme.get_reply_message()
    if delme.reply_to_msg_id:
        try:
            await msg_src.delete()
            await delme.delete()
            if BOTLOG:
                await delme.client.send_message(
                    BOTLOG_CHATID, "Penghapusan pesan berhasil"
                )
        except rpcbaseerrors.BadRequestError:
            if BOTLOG:
                await delme.client.send_message(
                    BOTLOG_CHATID, "Ya, saya tidak bisa menghapus pesan"
                )


@register(outgoing=True, pattern="^.edit")
async def editer(edit):
    """ For .editme command, edit your last message. """
    message = edit.text
    chat = await edit.get_input_chat()
    self_id = await edit.client.get_peer_id("me")
    string = str(message[6:])
    i = 1
    async for message in edit.client.iter_messages(chat, self_id):
        if i == 2:
            await message.edit(string)
            await edit.delete()
            break
        i = i + 1
    if BOTLOG:
        await edit.client.send_message(
            BOTLOG_CHATID, "Edit query berhasil dijalankan"
        )


@register(outgoing=True, pattern="^.sd")
async def selfdestruct(destroy):
    """ For .sd command, make seflf-destructable messages. """
    message = destroy.text
    counter = int(message[4:6])
    text = str(destroy.text[6:])
    await destroy.delete()
    smsg = await destroy.client.send_message(destroy.chat_id, text)
    await sleep(counter)
    await smsg.delete()
    if BOTLOG:
        await destroy.client.send_message(BOTLOG_CHATID, "sd query done successfully")


CMD_HELP.update(
    {
        "purge": ".purge\
        \nPenggunaan: Membersihkan semua pesan mulai dari balasan."
    }
)

CMD_HELP.update(
    {
        "purgeme": ".purgeme <x>\
        \nPenggunaan: Menghapus sejumlah x pesan terbaru Anda."
    }
)

CMD_HELP.update(
    {
        "del": ".del\
\nPenggunaan: Menghapus pesan yang Anda balas."
    }
)

CMD_HELP.update(
    {
        "edit": ".edit <newmessage>\
\nPenggunaan: Ganti pesan terakhir Anda dengan <newmessage>."
    }
)

CMD_HELP.update(
    {
        "sd": ".sd <x> <message>\
\nPenggunaan: Membuat pesan yang merusak diri sendiri dalam x detik.\
\nPertahankan detik di bawah 100 karena bot Anda akan tertidur."
    }
)
