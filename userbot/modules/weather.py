# INFO : ini merupakan copy source code dari repo one4ubot, dan sudah mendapatkan izin dari pemilik.
# INFO : This is a copy of the source code from the One4ubot repo, and has the permission of the owner.
# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot module for getting the weather of a city. """

import json
from datetime import datetime
from urllib.parse import quote

from pytz import country_names as c_n
from pytz import country_timezones as c_tz
from pytz import timezone as tz
from requests import get

from userbot import CMD_HELP
from userbot import OPEN_WEATHER_MAP_APPID as OWM_API
from userbot import WEATHER_DEFCITY, WEATHER_DEFLANG
from userbot.events import register

# ===== CONSTANT =====
if WEATHER_DEFCITY:
    DEFCITY = WEATHER_DEFCITY
else:
    DEFCITY = None

if WEATHER_DEFLANG:
    DEFLANG = WEATHER_DEFLANG
else:
    DEFLANG = "en"
# ====================


async def get_tz(con):
    """ Get time zone of the given country. """
    """ Credits: @aragon12 and @zakaryan2004. """
    for c_code in c_n:
        if con == c_n[c_code]:
            return tz(c_tz[c_code][0])
    try:
        if c_n[con]:
            return tz(c_tz[con][0])
    except KeyError:
        return


@register(outgoing=True, pattern="^.weather(?: |$)(.*)")
async def get_weather(weather):
    """ For .weather command, gets the current weather of a city. """

    if not OWM_API:
        await weather.edit("`Dapatkan API Key dari` https://openweathermap.org/ `dahulu.`")
        return

    APPID = OWM_API

    if not weather.pattern_match.group(1):
        CITY = DEFCITY
        if not CITY:
            await weather.edit(
                "`Harap tentukan kota atau tetapkan sebagai default menggunakan variabel konfigurasi WEATHER_DEFCITY.`"
            )
            return
    else:
        CITY = weather.pattern_match.group(1)

    timezone_countries = {
        timezone: country
        for country, timezones in c_tz.items()
        for timezone in timezones
    }

    if "," in CITY:
        newcity = CITY.split(",")
        if len(newcity[1]) == 2:
            CITY = newcity[0].strip() + "," + newcity[1].strip()
        else:
            country = await get_tz((newcity[1].strip()).title())
            try:
                countrycode = timezone_countries[f"{country}"]
            except KeyError:
                await weather.edit("`Negara tidak valid.`")
                return
            CITY = newcity[0].strip() + "," + countrycode.strip()

    url = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={APPID}"
    request = get(url)
    result = json.loads(request.text)

    if request.status_code != 200:
        await weather.edit(f"`Negara tidak valid.`")
        return

    cityname = result["name"]
    curtemp = result["main"]["temp"]
    humidity = result["main"]["humidity"]
    min_temp = result["main"]["temp_min"]
    max_temp = result["main"]["temp_max"]
    desc = result["weather"][0]
    desc = desc["main"]
    country = result["sys"]["country"]
    sunrise = result["sys"]["sunrise"]
    sunset = result["sys"]["sunset"]
    wind = result["wind"]["speed"]
    winddir = result["wind"]["deg"]

    ctimezone = tz(c_tz[country][0])
    time = datetime.now(ctimezone).strftime("%A, %I:%M %p")
    fullc_n = c_n[f"{country}"]

    dirs = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]

    div = 360 / len(dirs)
    funmath = int((winddir + (div / 2)) / div)
    findir = dirs[funmath % len(dirs)]
    kmph = str(wind * 3.6).split(".")
    mph = str(wind * 2.237).split(".")

    def fahrenheit(f):
        temp = str(((f - 273.15) * 9 / 5 + 32)).split(".")
        return temp[0]

    def celsius(c):
        temp = str((c - 273.15)).split(".")
        return temp[0]

    def sun(unix):
        xx = datetime.fromtimestamp(unix, tz=ctimezone).strftime("%I:%M %p")
        return xx

    await weather.edit(
        f"**Temperature:** `{celsius(curtemp)}°C | {fahrenheit(curtemp)}°F`\n"
        + f"**Min. Temp.:** `{celsius(min_temp)}°C | {fahrenheit(min_temp)}°F`\n"
        + f"**Max. Temp.:** `{celsius(max_temp)}°C | {fahrenheit(max_temp)}°F`\n"
        + f"**Humidity:** `{humidity}%`\n"
        + f"**Wind:** `{kmph[0]} kmh | {mph[0]} mph, {findir}`\n"
        + f"**Sunrise:** `{sun(sunrise)}`\n"
        + f"**Sunset:** `{sun(sunset)}`\n\n"
        + f"**{desc}**\n"
        + f"`{cityname}, {fullc_n}`\n"
        + f"`{time}`"
    )


@register(outgoing=True, pattern="^.wtr(?: |$)(.*)")
async def get_wtr(wtr):
    """ For .wtr command, gets the current weather of a city. """

    if not wtr.pattern_match.group(1):
        CITY = DEFCITY
        if not CITY:
            await wtr.edit(
                "`Please specify a city or set one as default using the WEATHER_DEFCITY config variable.`"
            )
            return
    else:
        CITY = wtr.pattern_match.group(1)

    CITY = quote(CITY.replace(",", ""))
    LANG = DEFLANG.lower()
    URL = f"http://wttr.in/{CITY}?lang={LANG}&format=j1"
    result = get(URL).json()

    try:
        weather = result["current_condition"][0]
        tempC = weather["temp_C"]
        tempF = weather["temp_F"]
        humidity = weather["humidity"]
        windK = weather["windspeedKmph"]
        windM = weather["windspeedMiles"]
        windD = weather["winddir16Point"]
        time = weather["observation_time"]
        mintempC = result["weather"][0]["mintempC"]
        maxtempC = result["weather"][0]["maxtempC"]
        mintempF = result["weather"][0]["mintempF"]
        maxtempF = result["weather"][0]["maxtempF"]
        sunrise = result["weather"][0]["astronomy"][0]["sunrise"]
        sunset = result["weather"][0]["astronomy"][0]["sunset"]
        country = result["nearest_area"][0]["country"][0]["value"]
        region = result["nearest_area"][0]["region"][0]["value"]
        desc = weather[f"lang_{LANG}"][0]["value"]
    except KeyError:
        desc = weather["weatherDesc"][0]["value"]

    text = (
        f"**{desc}**\n\n"
        + f"**Suhu          :** `{tempC}°C | {tempF}°F`\n"
        + f"**Suhu Minimal. :** `{mintempC}°C | {mintempF}°F`\n"
        + f"**Suhu Maksimal :** `{maxtempC}°C | {maxtempF}°F`\n"
        + f"**Kelembaban    :** `{humidity}%`\n"
        + f"**Angin         :** `{windK}Km/h | {windM}Mp/h, {windD}`\n"
        + f"**Matahari terbit   :** `{sunrise}`\n"
        + f"**Matahari terbenam :** `{sunset}`\n"
        + f"**Diperbarui pada   :** `{time}`\n\n"
        + f"`{region}, {country}`"
    )

    await wtr.edit(text)


CMD_HELP.update(
    {
        "weather": ".weather <city> atau .weather <city>, <country name/code>\
    \nPenggunaan: Mendapat cuaca kota.",
        "wtr": ".wtr <city> atau .wtr <city>, <country name/code>\
    \nPenggunaan: Mendapat cuaca kota.",
    }
)
