#!/usr/bin/env python3.7
"""
A simple reminder bot for Discord servers

!reminder help
!reminder cancel <num>
!reminder <when> <msg>

Example for <when>:
    10s   - 10 seconds
    5m    - 5  minutes
    5m10s - 5  minutes and 10 seconds
    1h    - 1  hour
    1d    - 1  day
"""
import discord
import asyncio
import time
import re

# Define your bot_token in secret.py
from secret import bot_token

class Reminder:
    def __init__(self, id_, when, author, channel, message):
        self.id_ = id_
        self.when = when
        self.author = author
        self.channel = channel
        self.message = message

class ReminderManager:
    def __init__(self):
        self.reminders = []
        self.counter = 0
        self.task = None

    def start(self):
        loop = asyncio.get_running_loop()
        loop.create_task(self.run())

    async def run(self):
        while True:
            now = time.time()
            for i in range(len(self.reminders)):
                r = self.reminders[0]
                if r.when > now: break
                await r.channel.send(f'<@{r.author.id}>, your reminder:\n> {r.message!s}')
                self.reminders.pop(0)
            await asyncio.sleep(1)

    async def on_message(self, message):
        async def usage():
            await message.channel.send(f'Try !reminder help')

        m = message.content.split()
        if len(m) < 2:
            await usage()
            return

        if m[1] == 'help':
            help_text  = 'Command Examples:\n'
            help_text += '```\n'
            help_text += '- !reminder 1d file an issue about xyz\n'
            help_text += '- !reminder 6h restart the server\n'
            help_text += '- !reminder 5m update the wiki\n'
            help_text += '- !reminder cancel 5\n'
            help_text += '```\n'
            await message.channel.send(help_text)
            return

        elif m[1] == 'cancel':
            index = None
            try:
                requested = int(m[2])
                for i, r in enumerate(self.reminders):
                    if r.id_ == requested:
                        index = i
            except:
                await usage()
                return

            if index is None:
                await r.channel.send(f'Reminder {r_id} not found') 
                return

            r = self.reminders[index]
            can_remove = r.channel.permissions_for(message.author).manage_messages
            if (r.author == message.author) or can_remove:
                self.reminders.pop(index)
                await r.channel.send(f'Reminder {r.id_} cancelled')
            else:
                await r.channel.send(f'Permission denied')

        else:
            m = re.match(r'^!reminder\s+(?P<ts>(\d+[smhd])+)\s+(?P<msg>.+)', message.content)
            if m is None:
                await usage()
                return
            ts = m.group('ts')
            msg = m.group('msg')
            when = time.time()
            for val, unit in re.findall('(\d+)([dhms])', ts):
                units = {'s': 1, 'm': 60, 'h':60*60, 'd': 24*60*60}
                when += units[unit]*int(val)

            r = Reminder(self.counter, when, message.author, message.channel, msg)
            self.reminders.append(r)
            self.reminders.sort(key=lambda r: r.when)
            self.counter += 1
            await message.channel.send(f'Reminder {r.id_} created')
            return r

client = discord.Client()
rm = ReminderManager()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    rm.start()

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!reminder'):
        await rm.on_message(message)

client.run(bot_token)
