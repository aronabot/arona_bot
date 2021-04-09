import asyncio
import discord
from discord.ext import commands

import arona

class ExtensionManager:
    def __init__(self, arona: arona.Arona):
        self.arona = arona

    def _tostring(self, statuses: dict) -> str:
        """
        returns:
            "": if statuses hasn't any status about extensions
        """
        return "\n".join(["{0}:{1}".format(value["status"], "{0}\t{1}".format(ext, value["error"])) for ext, value in statuses.items()])


    async def display_extensions(self, ctx, _):
        result = "\n".join(["{0}".format(ext) for ext in self.arona.extensions_list])
        return await ctx.send("```{0}```".format(result))

        
    async def load_extensions(self, ctx, extensions: list):
        if extensions == []:
            await ctx.send("please enter extensions for load")
            return

        statuses = {k: {"status": "❌", "error": ""} for k in extensions}
        message = await ctx.send("```{0}```".format(self._tostring(statuses)))

        for extension in extensions:
            try:
                self.arona.load_extension(extension)
                self.arona.extensions_list += [extension]
                statuses[extension]["status"] = "✔️"

            except Exception as e:
                statuses[extension]["error"] = type(e).__name__

            await message.edit(content="```{0}```".format(self._tostring(statuses)))
        return


    async def unload_extensions(self, ctx, extensions: list):
        if extensions == []:
            await ctx.send("please enter extensions for unload")
            return

        statuses = {k: {"status": "❌", "error": ""} for k in extensions}
        message = await ctx.send("```{0}```".format(self._tostring(statuses)))

        for extension in extensions:
            try:
                self.arona.load_extension(extension)
                self.arona.extensions_list += [extension]
                statuses[extension]["status"] = "✔️"

            except Exception as e:
                statuses[extension]["error"] = type(e).__name__

            await message.edit(content="```{0}```".format(self._tostring(statuses)))
        return


    async def reload_extensions(self, ctx, extensions: list):
        if extensions == []:
            extensions = self.arona.extensions_list

        statuses = {k: {"status": "❌", "error": ""} for k in extensions}
        message = await ctx.send("```{0}```".format(self._tostring(statuses)))

        for extension in extensions:
            try:
                self.arona.reload_extension(extension)
                statuses[extension]["status"] = "✔️"

            except Exception as e:
                statuses[extension]["error"] = type(e).__name__

            await message.edit(content="```{0}```".format(self._tostring(statuses)))
        return