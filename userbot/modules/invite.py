# INFO : ini merupakan copy source code dari repo one4ubot, dan sudah mendapatkan izin dari pemilik.
# INFO : This is a copy of the source code from the One4ubot repo, and has the permission of the owner.
# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
# Port From UniBorg to UserBot by @afdulfauzan

from asyncio import sleep

from telethon import functions

from userbot import CMD_HELP
from userbot.events import register


@register(outgoing=True, pattern="^.invite(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    to_add_users = event.pattern_match.group(1)
    if event.is_private:
        await event.edit("`.invite` pengguna ke obrolan, bukan ke Pesan Pribadi")
    else:
        if not event.is_channel and event.is_group:
            # https://lonamiwebs.github.io/Telethon/methods/messages/add_chat_user.html
            for user_id in to_add_users.split(" "):
                try:
                    await event.client(
                        functions.messages.AddChatUserRequest(
                            chat_id=event.chat_id, user_id=user_id, fwd_limit=1000000
                        )
                    )
                except Exception as e:
                    await event.edit(str(e))
                    return
            await event.edit("`Berhasil Diundang`")
            await sleep(2)
            await event.delete()
        else:
            # https://lonamiwebs.github.io/Telethon/methods/channels/invite_to_channel.html
            for user_id in to_add_users.split(" "):
                try:
                    await event.client(
                        functions.channels.InviteToChannelRequest(
                            channel=event.chat_id, users=[user_id]
                        )
                    )
                except Exception as e:
                    await event.edit(str(e))
                    return
            await event.edit("`Berhasil Diundang`")
            await sleep(2)
            await event.delete()


CMD_HELP.update(
    {
        "invite": ".invite <username> \
        \nUPenggunaan: Undang beberapa pengguna atau bot jika Anda mau."
    }
)
