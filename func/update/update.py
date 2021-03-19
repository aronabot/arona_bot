from .connect import Connector
import asyncio
import discord
from discord.ext import commands

import arona

class Update(commands.Cog):
    def __init__(self, arona: arona.Arona):
        self.arona = arona

    @commands.is_owner()
    @commands.command(name="update")
    async def _update(self, ctx):
        await ctx.send("업데이트를 진행합니다.")

def setup(arona: arona.Arona):
    arona.add_cog(Update(arona))