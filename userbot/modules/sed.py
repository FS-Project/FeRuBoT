# INFO : ini merupakan copy source code dari repo one4ubot, dan sudah mendapatkan izin dari pemilik.
# INFO : This is a copy of the source code from the One4ubot repo, and has the permission of the owner.
# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
# The entire source code is OSSRPL except 'sed' which is GPLv3
# License: GPLv3 and OSSRPL
""" Userbot command for sed. """

import re
from sre_constants import error as sre_err

from userbot import CMD_HELP
from userbot.events import register

DELIMITERS = ("/", ":", "|", "_")


async def separate_sed(sed_string):
    """ Separate sed arguments. """

    if len(sed_string) < 2:
        return

    if (
        len(sed_string) >= 2
        and sed_string[2] in DELIMITERS
        and sed_string.count(sed_string[2]) >= 2
    ):
        delim = sed_string[2]
        start = counter = 3
        while counter < len(sed_string):
            if sed_string[counter] == "\\":
                counter += 1

            elif sed_string[counter] == delim:
                replace = sed_string[start:counter]
                counter += 1
                start = counter
                break

            counter += 1

        else:
            return None

        while counter < len(sed_string):
            if (
                sed_string[counter] == "\\"
                and counter + 1 < len(sed_string)
                and sed_string[counter + 1] == delim
            ):
                sed_string = sed_string[:counter] + sed_string[counter + 1 :]

            elif sed_string[counter] == delim:
                replace_with = sed_string[start:counter]
                counter += 1
                break

            counter += 1
        else:
            return replace, sed_string[start:], ""

        flags = ""
        if counter < len(sed_string):
            flags = sed_string[counter:]
        return replace, replace_with, flags.lower()
    return None


@register(outgoing=True, pattern="^.s")
async def sed(command):
    """ For sed command, use sed on Telegram. """
    sed_result = await separate_sed(command.text)
    textx = await command.get_reply_message()
    if sed_result:
        if textx:
            to_fix = textx.text
        else:
            await command.edit(
                "`Master, Saya tidak punya otak. Yah, kurasa juga tidak.`"
            )
            return

        repl, repl_with, flags = sed_result

        if not repl:
            await command.edit(
                "`Master, Saya tidak punya otak. Yah, kurasa juga tidak.`"
            )
            return

        try:
            check = re.match(repl, to_fix, flags=re.IGNORECASE)
            if check and check.group(0).lower() == to_fix.lower():
                await command.edit("`Boi!, itu jawaban. Jangan gunakan sed`")
                return

            if "i" in flags and "g" in flags:
                text = re.sub(repl, repl_with, to_fix, flags=re.I).strip()
            elif "i" in flags:
                text = re.sub(repl, repl_with, to_fix, count=1, flags=re.I).strip()
            elif "g" in flags:
                text = re.sub(repl, repl_with, to_fix).strip()
            else:
                text = re.sub(repl, repl_with, to_fix, count=1).strip()
        except sre_err:
            await command.edit("B O I! [Pelajari Regex](https://regexone.com)")
            return
        if text:
            await command.edit(f"Apakah yang kamu maksud? \n\n{text}")


CMD_HELP.update(
    {
        "sed": ".s<delimiter><old word(s)><delimiter><new word(s)>\
    \nPenggunaan: Mengganti satu kata atau kata-kata.\
    \nmenggunakan sed Delimiters: `/, :, |, _`"
    }
)
