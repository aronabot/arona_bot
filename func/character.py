import json
import asyncio

import discord
from discord.ext import commands

import arona

class Character(commands.Cog):
    def __init__(self, arona: arona.Arona):
        self.arona = arona
    
    @commands.command(name="creload")
    async def _reload(self, ctx):
        try:
            self.arona.reload_extension("Character")
        except Exception as e:
            print(e)
        print("character reload complete")
        return

    @commands.command(name="캐릭터")
    async def _command_character(self, ctx, *, name):
        """
        캐릭터의 정보를 디스코드 채팅으로 보내주는 함수
        args:
            name: 해당 캐릭터 이름
        return:
            embed: 해당 캐릭터의 정보가 담긴 embed
        """
        self.arona.server["ID"]
        self.arona.server["character"]["icon"]
        self.arona.server["character"]["ability"]
        self.arona.server["character"]["skills"]

        result = discord.Embed()

        return await ctx.send(embed=result)

def setup(arona : arona.Arona):
    arona.add_cog(Character(arona))