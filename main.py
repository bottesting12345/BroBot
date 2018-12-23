# python3.6
# coding: utf-8

import os
import sys
import time
import asyncio
import aiohttp
import traceback
import aiohttp

import discord
from discord.ext import commands

prefix = os.getenv('PREFIX')

bot = commands.Bot(command_prefix=prefix)
bot.remove_command('help')

async def start_session():
    bot.session = aiohttp.ClientSession(loop=bot.loop)

extensions = ['cogs.member.fun',
              'cogs.member.info',
              'cogs.member.music',
              'cogs.member.utils',
              'cogs.system.error_handler',
              'cogs.system.logger',
              'cogs.admin.management',
              'cogs.owner']

if __name__ == '__main__':
    for extension in extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print(f'[!]  Failed to load module {extension}.', file=sys.stderr)
            traceback.print_exc()
            print('------------------------')
        else:
            print(f'[!] Module {extension} loaded successfully.')

@bot.event
async def on_connect():
    await bot.change_presence(activity=discord.Game(name='Over Servers:з'), status=discord.Status.online)

@bot.event
async def on_ready():
    print(f'[#] Connection successful!\n[#] Online: {bot.user}')

    async def presence():
        await start_session()
        while not bot.is_closed():
            awaiting = 10

            messages = [f'{len(bot.guilds)} servers!',
                        f'{len(bot.users)} !',
                        f'{len(bot.emojis)} Emoji!',
                        f'{len([x.name for x in bot.commands if not x.hidden])} commands!',
                        f'{prefix}help']
            for msg in messages:
                if os.getenv('ACTIVITY') == 'streaming':
                    await bot.change_presence(activity=discord.Streaming(name=msg, url='https://www.twitch.tv/%none%'))
                    await asyncio.sleep(awaiting)
                elif os.getenv('ACTIVITY') == 'playing':
                    await bot.change_presence(activity=discord.Game(name=msg))
                    await asyncio.sleep(awaiting)
    await bot.loop.create_task(presence())

bot.run(os.getenv('TOKEN'), bot=True, reconnect=True)
