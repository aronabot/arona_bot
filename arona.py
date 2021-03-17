import func

import os
import json
import logging

import asyncio
import discord
from discord.ext import commands

class Arona(commands.Bot):
    __slots__ = ["config", "server"]

    def __init__(self):
        intents = discord.Intents(guilds=True, emojis=True, messages=True, 
                                guild_messages=True, reactions=True, 
                                guild_reactions=True)
        super().__init__(intents=intents, command_prefix="!")

        with open("config.json", encoding="utf-8") as data:
            self.config = json.load(data)
            self.server = self.config["discord"]


    def run(self, bot_token: str):
        super().run(bot_token, reconnect=True)
        #self.load_extension("")

    async def on_ready(self):
        print("logged in as {0}".format(self.user))

    async def on_message(self, message):
        if message.author.bot:
            return
       
    async def on_command_error(self, ctx, error):
        ignore_exception_list = [
            commands.CommandNotFound,
            commands.MissingRequiredArgument
        ]

        if any(isinstance(error, i) for i in ignore_exception_list):
            return

        return await ctx.send("Error!```py\n{0}: {1}```".format(type(error), error))

    async def close(self):
        await super().close()

if __name__ == '__main__':
    bot = Arona()
    bot.run(os.environ.get("TOKEN"))