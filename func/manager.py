import asyncio
import discord
from discord.ext import commands
from .util import *

import arona

class Manager(commands.Cog):
    def __init__(self, arona: arona.Arona):
        self.arona = arona
        pass
    
    def _tostring(self, status: dict) -> str:
        result = ""

        for ext, s in status.items():
            result += "{0}:{1}\n".format(s, ext)

        return result

    @commands.is_owner()
    @commands.command(name="show", hidden=True)
    async def _show_extension(self, ctx):
        result = "```\n"
        for ext in self.arona.extensions_list:
            result += "{0}\n".format(ext)
        result += "```"
        
        return await ctx.send(result)

    @commands.is_owner()
    @commands.command(name="load", hidden=True)
    async def _load_extension(self, ctx, *, extensions):
        extensions = extensions.split(" ")
        status = { k : "❌" for k in extensions }

        status_string = self._tostring(status)
        message = await sendmsg(ctx, status_string)
        
        if message is None:
            return

        for ext in extensions:
            try:
                self.arona.load_extension(ext)
                self.arona.extensions_list += [ext]
                status[ext] = "✔️"

            except Exception as e:
                status["{0} : {1}".format(ext, type(e).__name__)] = status.pop(ext)

            status_string = self._tostring(status)
            await message.edit(content="```{0}```".format(status_string))

    @commands.is_owner()
    @commands.command(name="unload", hidden=True)
    async def _unload_extension(self, ctx, *, extensions):
        extensions = extensions.split(" ")
        status = { k : "❌" for k in extensions }

        status_string = self._tostring(status)
        message = await sendmsg(ctx, status_string)
        
        if message is None:
            return

        for ext in extensions:
            try:
                self.arona.unload_extension(ext)
                self.arona.extensions_list.remove(ext)
                status[ext] = "✔️"

            except Exception as e:
                status["{0} : {1}".format(ext, type(e).__name__)] = status.pop(ext)

            status_string = self._tostring(status)
            await message.edit(content="```{0}```".format(status_string))

    @commands.is_owner()
    @commands.command(name="reload", hidden=True)
    async def _reload_extension(self, ctx):
        extensions = self.arona.extensions_list
        status = { k : "❌" for k in extensions }

        status_string = self._tostring(status)
        message = await sendmsg(ctx, status_string)
        
        if message is None:
            return

        for ext in extensions:
            try:
                self.arona.reload_extension(ext)
                status[ext] = "✔️"

            except Exception as e:
                status["{0} : {1}".format(ext, type(e).__name__)] = status.pop(ext)

            status_string = self._tostring(status)
            await message.edit(content="```{0}```".format(status_string))


def setup(arona : arona.Arona):
    arona.add_cog(Manager(arona))