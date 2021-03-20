import json
import asyncio
import pymysql
import discord
from discord.ext import commands

import arona

class Character(commands.Cog):
    """
    member values:
        infoch:
            type: dict
            캐릭터의 정보를 가지고 있는 채널의 목록
        characters:
            type: dict
            현재 등록되어 있는 캐릭터의 정보의 레퍼런스를 담고 있다.
    """
    __slots__ = ["infoch", "characters"]

    def __init__(self, arona: arona.Arona):
        self.arona = arona

        self.infoch = {k : self.arona.get_channel(v) 
                        for k, v in self.arona.server["character"].items()}
        
        with open("resource/character.json", encoding="utf-8") as data:
            self.characters = json.load(data)

    @commands.command(name="리스트")
    async def _list_character(self, ctx):
        """
        사용방법 : !리스트
        """
        conn = pymysql.connect(**self.arona.config["connect"])
        sql = "SELECT name FROM characters"
        result = []
        try:
            with conn.cursor() as curs:
                curs.execute(sql)
                result = curs.fetchall()
        finally:
            conn.close()

        text = ""
        for i, j, k in zip(result[::3], result[1::3], result[2::3]):
            text += "{0}  {1}  {2}\n".format(i[0], j[0], k[0])
        embed = discord.Embed(title="캐릭터 리스트", description=text)
        await ctx.send(embed=embed)

    @commands.command(name="캐릭터")
    async def _select_character(self, ctx, *, name):
        """
        사용방법 : !캐릭터 <찾을 캐릭터의 이름>
        """

        conn = pymysql.connect(**self.arona.config["connect"])
        sql = "SELECT * FROM characters as c\
               INNER JOIN exskills as ex\
                   ON ex.id=c.ex_skill\
               INNER JOIN skills as basic\
                   ON basic.id=c.basic_skill\
               INNER JOIN skills as passive\
                   ON passive.id=c.passive_skill\
               INNER JOIN skills as sub\
                   ON sub.id=c.sub_skill\
               WHERE c.name like %s"
    
        result = ()
        try:
            with conn.cursor(pymysql.cursors.DictCursor) as curs:
                curs.execute(sql, name+"%")
                result = curs.fetchall()
        finally:
            conn.close()

        if result == ():
            return await ctx.send("**{0}**(이)라는 캐릭터는 없습니다. 선생님".format(name))

        if len(result) > 1:
            string = ""
            for r in result:
                string += "- {0}\n".format(r["name"])
            return await ctx.send("선생님께서 찾으시는 캐릭터는 누구인가요?\n{0}".format(string))

        result = result[0]
        url = await self.infoch["icon"].fetch_message(result["icon"])
        url = url.attachments[0].url


        embed = discord.Embed(title=result["name"])
        embed.set_thumbnail(url = url)
        embed.add_field(name="정보", value="**편성**: {0[type]}\n\
                                            **역할**: {0[position_a]}/{0[position_b]}\n\
                                            **공격타입**: {0[attack_type]}\n\
                                            **방어타입**: {0[defence_type]}\n".format(result), inline=True)
        
        embed.add_field(name="스탯", value="**HP**: {0[HP]}\n\
                                            **공격력**: {0[ATK]}\n\
                                            **방어력**: {0[DEF]}\n\
                                            **치유력**: {0[HEAL]}\n\
                                            **명중치**: {0[ACC]}\n".format(result), inline=True)

        embed.add_field(name="스킬", value="**EX 스킬: 코스트{0[cost]}**\n{0[content]}\n\
                                            **노말 스킬**\n{0[basic.content]}\n\
                                            **패시브 스킬**\n{0[passive.content]}\n\
                                            **서브 스킬**\n{0[sub.content]}\n".format(result), inline=False)

        return await ctx.send(embed=embed)

def setup(arona : arona.Arona):
    arona.add_cog(Character(arona))