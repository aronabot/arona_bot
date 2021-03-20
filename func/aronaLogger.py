import json
import sys
from aiologger import Logger
from aiologger.handlers.streams import AsyncStreamHandler
import asyncio
import discord

from discord.ext import commands
import arona

class AronaLogger(commands.Cog):
    def __init__(self, arona: arona.Arona):
        self.arona = arona
        self.channel = self.arona.get_channel(arona.config["discord"]["test"])
        self.level = 0
        self.filter = 0

    async def emit(self, record):
        await self.channel.send(record)


def setup(arona: arona.Arona):
    arona.add_cog(AronaLogger(arona))