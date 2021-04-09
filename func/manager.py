import asyncio
from discord.ext import commands

from Func.Manage.ExtensionManager import ExtensionManager

import arona

class Manager(commands.Cog):
    def __init__(self, arona: arona.Arona):
        self.arona = arona
        self.extension_manager = ExtensionManager(arona)


    @commands.is_owner()
    @commands.command(name="e", hidden=True)
    async def _call_extension_manager(self, ctx, *, oper):
        """
        manager about extensions
        """
        switch = {  
            "display": self.extension_manager.display_extensions,
            "load": self.extension_manager.load_extensions, 
            "reload": self.extension_manager.reload_extensions, 
            "unload": self.extension_manager.unload_extensions
        }

        oper = oper.split(" ")
        operator, operands = oper[0], oper[1:]

        await switch[operator](ctx, operands)

    @commands.is_owner()
    @commands.command(name="u", hidden=True)
    async def _call_update_manager(self, ctx, * oper):
        """
        manager about update
        """
        switch = {

        }
        operator, operands = oper[0], oper[1:]
        operands = "\n".join(operands)

        await switch[operator](ctx, operands)

def setup(arona: arona.Arona):
    arona.add_cog(Manager(arona))
