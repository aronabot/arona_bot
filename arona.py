import os
import json

import asyncio
import discord
from discord.ext import commands
import logging



class Arona(commands.Bot):
    __slots__ = ["config", "server"]
    extensions_list = ["func.manager", "func.character", "func.termevent", "func.update"]

    def __init__(self):
        intents = discord.Intents(guilds=True, emojis=True, messages=True, 
                                guild_messages=True, reactions=True, 
                                guild_reactions=True)
        super().__init__(intents=intents, command_prefix="!")

        self.updating = False
        
        with open("config.json", encoding="utf-8") as data:
            self.config = json.load(data)
            self.server = self.config["discord"]

    def run(self, bot_token: str):
        super().run(bot_token, reconnect=True)

    async def on_ready(self):
        print("logged in as {0}".format(self.user))
        for ext in self.extensions_list:
            self.load_extension(ext)

    async def on_message(self, message):
        if message.author.bot:
            return
        
        if self.updating and message.content in ["{0}{1}".format(self.command_prefix, c.name) for c in self.commands]:
            return await message.channel.send("현재 업데이트 중입니다. 잠시만 기다려 주세요...")

        return await self.process_commands(message)

    async def on_command_error(self, ctx, error):
        ignore_exception_list = [
            commands.CommandNotFound,
            commands.MissingRequiredArgument,
            commands.errors.NotOwner
        ]

        if any(isinstance(error, i) for i in ignore_exception_list):
            return

        return await ctx.send("Error!```py\n{0}: {1}```".format(type(error), error))

    async def close(self):
        await super().close()

if __name__ == '__main__':
    bot = Arona()
    bot.run(os.environ.get("TOKEN"))