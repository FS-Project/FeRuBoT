# INFO : ini merupakan copy source code dari repo one4ubot, dan sudah mendapatkan izin dari pemilik.
# INFO : This is a copy of the source code from the One4ubot repo, and has the permission of the owner.
# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#

import os

import lyricsgenius
from pylast import User

from userbot import CMD_HELP, GENIUS, LASTFM_USERNAME, lastfm
from userbot.events import register

if GENIUS is not None:
    genius = lyricsgenius.Genius(GENIUS)


@register(outgoing=True, pattern="^.lyrics (?:(now)|(.*) - (.*))")
async def lyrics(lyric):
    await lyric.edit("`Mendapatkan informasi...`")
    if GENIUS is None:
        await lyric.edit("`Berikan token akses jenius ke Heroku ConfigVars...`")
        return False
    if lyric.pattern_match.group(1) == "now":
        playing = User(LASTFM_USERNAME, lastfm).get_now_playing()
        if playing is None:
            await lyric.edit("`Tidak ada informasi scrobbling lastfm terkini...`")
            return False
        artist = playing.get_artist()
        song = playing.get_title()
    else:
        artist = lyric.pattern_match.group(2)
        song = lyric.pattern_match.group(3)
    await lyric.edit(f"`Mencari lirik {artist} - {song}...`")
    songs = genius.search_song(song, artist)
    if songs is None:
        await lyric.edit(f"`Lagu`  **{artist} - {song}**  `tidak ditemukan...`")
        return False
    if len(songs.lyrics) > 4096:
        await lyric.edit("`Lirik terlalu besar, lihat file untuk melihatnya.`")
        with open("lyrics.txt", "w+") as f:
            f.write(f"Hasil pencarian: \n{artist} - {song}\n\n{songs.lyrics}")
        await lyric.client.send_file(
            lyric.chat_id,
            "lyrics.txt",
            reply_to=lyric.id,
        )
        os.remove("lyrics.txt")
        return True
    else:
        await lyric.edit(
            f"**Hasil pencarian**:\n`{artist}` - `{song}`" f"\n\n```{songs.lyrics}```"
        )
        return True


CMD_HELP.update(
    {
        "lyrics": ".lyrics **<nama artis> - <nama lagu>**"
        "\nPenggunaan: Dapatkan lirik yang cocok dengan artis dan lagu."
        "\n\n.lyrics now"
        "\nPenggunaan: Dapatkan lirik artis dan lagu dari scrobbling lastfm saat ini."
    }
)
