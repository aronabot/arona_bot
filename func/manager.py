import asyncio
import discord
from discord.ext import commands
import arona

class Manager(commands.Cog):
    def __init__(self, arona : arona.Arona):
        self.arona = arona
        pass

    @commands.command(name="load")
    async def _load_extention(self, ctx, *, extensions):
        extensions = extensions.split(" ")

        try:
            for ext in extensions:
                self.arona.load_extension(ext)
                self.arona.extensions_list += [ext]

        except Exception as e:
            print(e)

    @commands.command(name="unload")
    async def _unload_extention(self, ctx, *, extensions):
        extensions = extensions.split(" ")

        try:
            for ext in extensions:
                self.arona.unload_extension(ext)
                self.arona.extensions_list.remove(ext)
        except Exception as e:
            print(e)

    @commands.command(name="reload")
    async def _reload_extention(self, ctx):
        try:
            for ext in [x for x in self.arona.extensions_list if x != "func.manager"]:
                self.arona.load_extension(ext)
        except Exception as e:
            print(e)

def setup(arona : arona.Arona):
    arona.add_cog(Manager(arona))