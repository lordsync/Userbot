# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.b (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot module which contains afk-related commands """

import time
import random

from telethon.events import StopPropagation

from userbot import (AFKREASON, COUNT_MSG, CMD_HELP, ISAFK, BOTLOG, BOTLOG_CHATID,
                     USERS)
from userbot.events import register


@register(incoming=True, disable_edited=True)
async def mention_afk(mention):
    """ This function takes care of notifying the people who mention you that you are AFK."""
    global COUNT_MSG
    global USERS
    global ISAFK
    if mention.message.mentioned and not (await mention.get_sender()).bot:
        if ISAFK:
            if mention.sender_id not in USERS:
                await mention.reply(
                    f"Sorry! My boss is AFK due to `{AFKREASON}`."
                    "\nWould ping him to look into the message soon 😉."
                )
                USERS.update({mention.sender_id: 1})
                COUNT_MSG = COUNT_MSG + 1
            elif mention.sender_id in USERS:
                if USERS[mention.sender_id] % 5 == 0:
                    await mention.reply(
                        "Sorry! But my boss is still not here."
                        "\nTry to ping him a little later. I am sorry 😖."
                        f"\nHe told me he was busy with `{AFKREASON}`."
                    )
                    USERS[mention.sender_id] = USERS[mention.sender_id] + 1
                    COUNT_MSG = COUNT_MSG + 1
                else:
                    USERS[mention.sender_id] = USERS[mention.sender_id] + 1
                    COUNT_MSG = COUNT_MSG + 1


@register(incoming=True, disable_edited=True)
async def afk_on_pm(sender):
    """ Function which informs people that you are AFK in PM """
    global ISAFK
    global USERS
    global COUNT_MSG
    if sender.is_private and not (await sender.get_sender()).bot:
        if ISAFK:
            if sender.sender_id not in USERS:
                await sender.reply(
                    f"Sorry! My boss is AFK due to `{AFKREASON}`."
                    "\nI'll ping him to look into the message soon 😉."
                )
                USERS.update({sender.sender_id: 1})
                COUNT_MSG = COUNT_MSG + 1
            elif sender.sender_id in USERS:
                if USERS[sender.sender_id] % 5 == 0:
                    await sender.reply(
                        "Sorry! But my boss is still not here."
                        "\nTry to ping him a little later. I am sorry 😖."
                        f"\nHe told me he was busy with `{AFKREASON}`."
                    )
                    USERS[sender.sender_id] = USERS[sender.sender_id] + 1
                    COUNT_MSG = COUNT_MSG + 1
                else:
                    USERS[sender.sender_id] = USERS[sender.sender_id] + 1
                    COUNT_MSG = COUNT_MSG + 1


@register(outgoing=True, pattern="^.afk")
async def set_afk(afk_e):
    """ For .afk command, allows you to inform people that you are afk when they message you """
    if not afk_e.text[0].isalpha() and afk_e.text[0] not in ("/", "#", "@", "!"):
        message = afk_e.text
        string = str(message[5:])
        global ISAFK
        global AFKREASON

        AFKSTR = [
        "AFK AF!",
        "Out of my mind. Back in five!",
        "I'll be back in a couple of minutes... If not, read this status again!",
        "I'll be back in a couple of hours. I didn't say starting from when.",
        "If I'm not back in half an hour... please wait a little longer.",
        "I'm away; please talk in a bag and when I come back you'll just give me the bag!",
        "Away. If you need anything, leave a message after the beep: beeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeep!",
        "Away over 7 seas and 7 countries, 7 waters and 7 continents, 7 mountains and 7 hills, 7 plains and 7 mounds, 7 pools and 7 lakes, 7 springs and 7 meadows, 7 cities and 7 neighborhoods, 7 blocks and 7 houses... Where not even your messages can reach me!",
        "I'm away from the keyboard at the moment, but if you'll scream loud enough at your screen, I might just hear you.",
        "I am away! I don't know when I'll be back! Hopefully 10 minutes from NOW!",
        ]

        await afk_e.edit(str(random.choice(AFKSTR)))
        if string != "":
            AFKREASON = string
        if BOTLOG:
            await afk_e.client.send_message(BOTLOG_CHATID, "You went AFK!")
        ISAFK = True
        raise StopPropagation


@register(outgoing=True)
async def type_afk_is_not_true(notafk):
    """ This sets your status as not afk automatically when you write something while being afk """
    global ISAFK
    global COUNT_MSG
    global USERS
    global AFKREASON
    if ISAFK:
        ISAFK = False
        await notafk.respond("I'm no longer AFK.")
        afk_info = await notafk.respond(
            "`You recieved " +
            str(COUNT_MSG) +
            " messages while you were away. Check log for more details.`" +
            " `This auto-generated message shall be self destructed in 2 seconds.`"
        )
        time.sleep(2)
        await afk_info.delete()
        if BOTLOG:
            await notafk.client.send_message(
                BOTLOG_CHATID,
                "You've recieved " +
                str(COUNT_MSG) +
                " messages from " +
                str(len(USERS)) +
                " chats while you were away",
            )
            for i in USERS:
                name = await notafk.client.get_entity(i)
                name0 = str(name.first_name)
                await notafk.client.send_message(
                    BOTLOG_CHATID,
                    "[" +
                    name0 +
                    "](tg://user?id=" +
                    str(i) +
                    ")" +
                    " sent you " +
                    "`" +
                    str(USERS[i]) +
                    " messages`",
                )
        COUNT_MSG = 0
        USERS = {}
        AFKREASON = "No Reason"

CMD_HELP.update({
    "afk": ".afk <reason>(reason is optional)\
\nUsage: Sets you as afk. Responds to anyone who tags/PM's \
you telling that you are afk. Switches off AFK when you type back anything.\
"
})