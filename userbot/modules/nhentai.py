# INFO : ini merupakan copy source code dari repo one4ubot, dan sudah mendapatkan izin dari pemilik.
# INFO : This is a copy of the source code from the One4ubot repo, and has the permission of the owner.
# Copyright (C) 2020 KeselekPermen69
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#

from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError

from userbot import CMD_HELP, bot
from userbot.events import register


@register(outgoing=True, pattern="^.nhentai(?: |$)(.*)")
async def _(hentai):
    if hentai.fwd_from:
        return
    link = hentai.pattern_match.group(1)
    if not link:
        return await hentai.edit("`Saya tidak bisa mencari apa-apa`")
    chat = "@nHentaiBot"
    await hentai.edit("```Sedang Proses```")
    async with bot.conversation(chat) as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=424466890)
            )
            msg = await bot.send_message(chat, link)
            response = await response
            """ - jangan spam notif - """
            await bot.send_read_acknowledge(conv.chat_id)
        except YouBlockedUserError:
            await hentai.reply("```Harap buka blokir @nHentaiBot dan coba lagi```")
            return
        if response.text.startswith("**Sorry I couldn't get manga from**"):
            await hentai.edit("```Saya pikir ini bukan tautan yang tepat```")
        else:
            await hentai.delete()
            await bot.send_message(hentai.chat_id, response.message)
            await bot.send_read_acknowledge(hentai.chat_id)
            """ - bersihkan obrolan setelah selesai - """
            await hentai.client.delete_messages(conv.chat_id, [msg.id, response.id])


CMD_HELP.update(
    {
        "nhentai": ".nhentai <link / kode> \
        \nPenggunaan: melihat nhentai di telegraph.\n"
    }
)
