# INFO : ini merupakan copy source code dari repo one4ubot, dan sudah mendapatkan izin dari pemilik.
# INFO : This is a copy of the source code from the One4ubot repo, and has the permission of the owner.
# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
# Port From UniBorg to UserBot by keselekpermen69

import io
import re

import userbot.modules.sql_helper.blacklist_sql as sql
from userbot import CMD_HELP
from userbot.events import register


@register(incoming=True, disable_edited=True, disable_errors=True)
async def on_new_message(event):
    # TODO: exempt admins from locks
    name = event.raw_text
    snips = sql.get_chat_blacklist(event.chat_id)
    for snip in snips:
        pattern = r"( |^|[^\w])" + re.escape(snip) + r"( |$|[^\w])"
        if re.search(pattern, name, flags=re.IGNORECASE):
            try:
                await event.delete()
            except Exception:
                await event.reply("Saya tidak memiliki izin HAPUS dalam obrolan ini")
                sql.rm_from_blacklist(event.chat_id, snip.lower())
            break


@register(outgoing=True, pattern="^.addbl(?: |$)(.*)")
async def on_add_black_list(addbl):
    text = addbl.pattern_match.group(1)
    to_blacklist = list(
        set(trigger.strip() for trigger in text.split("\n") if trigger.strip())
    )
    for trigger in to_blacklist:
        sql.add_to_blacklist(addbl.chat_id, trigger.lower())
    await addbl.edit(
        "Ditambahkan {} triggers ke daftar hitam di obrolan saat ini".format(
            len(to_blacklist)
        )
    )


@register(outgoing=True, pattern="^.listbl(?: |$)(.*)")
async def on_view_blacklist(listbl):
    all_blacklisted = sql.get_chat_blacklist(listbl.chat_id)
    OUT_STR = "Daftar Hitam di Obrolan Saat Ini:\n"
    if len(all_blacklisted) > 0:
        for trigger in all_blacklisted:
            OUT_STR += f"`{trigger}`\n"
    else:
        OUT_STR = "Tidak Ada Daftar Hitam. Mulai Menyimpan menggunakan `.addbl`"
    if len(OUT_STR) > 4096:
        with io.BytesIO(str.encode(OUT_STR)) as out_file:
            out_file.name = "blacklist.text"
            await listbl.client.send_file(
                listbl.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption="Daftar Hitam di Obrolan Saat Ini",
                reply_to=listbl,
            )
            await listbl.delete()
    else:
        await listbl.edit(OUT_STR)


@register(outgoing=True, pattern="^.rmbl(?: |$)(.*)")
async def on_delete_blacklist(rmbl):
    text = rmbl.pattern_match.group(1)
    to_unblacklist = list(
        set(trigger.strip() for trigger in text.split("\n") if trigger.strip())
    )
    successful = 0
    for trigger in to_unblacklist:
        if sql.rm_from_blacklist(rmbl.chat_id, trigger.lower()):
            successful += 1
    await rmbl.edit(f"Menghapus {successful} / {len(to_unblacklist)} dari daftar hitam")


CMD_HELP.update(
    {
        "daftarhitam": ".listbl\
    \nPenggunaan: Mencantumkan semua daftar hitam bot pengguna aktif dalam obrolan.\
    \n\n.addbl <kata kunci>\
    \nPenggunaan: Menyimpan pesan ke 'kata kunci daftar hitam'.\
    \nBot akan menghapus pesan setiap kali 'kata kunci daftar hitam' disebutkan.\
    \n\n.rmbl <kata kunci>\
    \nPenggunaan: Menghentikan daftar hitam tertentu.\
	\n btw you need permissions **Delete Messages** of admin."
    }
)
