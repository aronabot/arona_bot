from .connect import Connector
import asyncio
import discord
from discord.ext import commands

import arona

class Update(commands.Cog):
    def __init__(self, arona: arona.Arona):
        self.arona = arona
        self.connector = Connector(arona.config["mirror"], arona.config["term"])

    async def _get_rawdata(self):
        rawdata = await self.connector.download()
        return rawdata

    async def _parsing_rawdata(self):
        pass

def setup(arona: arona.Arona):
    arona.add_cog(Update(arona))