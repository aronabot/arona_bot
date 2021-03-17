import asyncio
import discord
from discord.ext import commands
import arona

class Manager(commands.Cog):
    def __init__(self, arona : arona.Arona):
        self.arona = arona
        pass
    
    @commands.command(name="show")
    async def _show_extension(self, ctx):
        result = "```"
        for ext in self.arona.extensions_list:
            result += "{0}\n".format(ext)
        result += "```"
        
        return await ctx.send(result)

    @commands.command(name="load")
    async def _load_extension(self, ctx, *, extensions):
        extensions = extensions.split(" ")
        sucess_list = { k : "❌" for k in extensions }
        fail_list = {}

        result = "```"
        for k, v in sucess_list.items():
            result += "{0} :\t{1}\n".format(k, v)
        result += "```"
        message = await ctx.send(result)
        
        
        for ext in extensions:
            try:
                self.arona.load_extension(ext)
                self.arona.extensions_list += [ext]
                sucess_list[ext] = "✔️"

                tmp = "```"
                for k, v in sucess_list.items():
                    tmp += "{0} :\t{1}\n".format(k, v)
                tmp += "```"
                await message.edit(content=tmp)

            except Exception as e:
                fail_list[ext] = str(e)

        print(fail_list)


    @commands.command(name="unload")
    async def _unload_extension(self, ctx, *, extensions):
        extensions = extensions.split(" ")
        sucess_list = { k : "❌" for k in extensions }
        fail_list = {}

        result = "```"
        for k, v in sucess_list.items():
            result += "{0} :\t{1}\n".format(k, v)
        result += "```"
        message = await ctx.send(result)

       
        for ext in extensions:
            try:
                self.arona.unload_extension(ext)
                self.arona.extensions_list.remove(ext)
                sucess_list[ext] = "✔️"
                tmp = "```"
                for k, v in sucess_list.items():
                    tmp += "{0} :\t{1}\n".format(k, v)
                tmp += "```"
                await message.edit(content=tmp)

            except Exception as e:
                fail_list[ext] = str(e)
            
        print(fail_list)

    @commands.command(name="reload")
    async def _reload_extension(self, ctx):
        exts = self.arona.extensions_list
        sucess_list = { k : "❌" for k in exts }
        fail_list = {}

        result = "```"
        for k, v in sucess_list.items():
            result += "{0} :\t{1}\n".format(k, v)
        result += "```"
        message = await ctx.send(result)

        
        for ext in exts:
            try:
                self.arona.reload_extension(ext)
                sucess_list[ext] = "✔️"
                tmp = "```"
                for k, v in sucess_list.items():
                    tmp += "{0} :\t{1}\n".format(k, v)
                tmp += "```"
                await message.edit(content=tmp)

            except Exception as e:
                fail_list[ext] = str(e)
            
        print(fail_list)

def setup(arona : arona.Arona):
    arona.add_cog(Manager(arona))