import json
import asyncio

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

    @commands.command(name="캐릭터")
    async def _command_character(self, ctx, *, name):
        """
        캐릭터의 정보를 디스코드 채팅으로 보내주는 함수
        args:
            name: 해당 캐릭터 이름
        return:
            embed: 해당 캐릭터의 정보가 담긴 embed
        """
        target = self.characters[name]

        result = {attr : await ch.fetch_message(target[attr])
        for attr, ch in self.infoch.items()}

        result["icon"] = result["icon"].attachments[0].url
        result["ability"] = json.loads(result["ability"].content)
        result["skills"] = json.loads(result["skills"].content)

        embed = discord.Embed(title=name)
        embed.set_thumbnail(url = result["icon"])
        embed.add_field(name="정보", value="**소속**: {0[affiliation]}\n\
                                            **편성**: {0[type]}\n\
                                            **역할**: {0[position]}\n\
                                            **공격타입**: {0[attack_type]}\n\
                                            **방어타입**: {0[defence_type]}\n\
                                            **무기**: {0[weapon_type]}\n".format(result["ability"]), inline=True)
        
        embed.add_field(name="스탯", value="**HP**: {0[HP]}\n\
                                            **공격력**: {0[ATK]}\n\
                                            **방어력**: {0[DEF]}\n\
                                            **치유력**: {0[HEAL]}\n\
                                            **명중치**: {0[ACC]}\n".format(result["ability"]["status"]), inline=True)
        
        embed.add_field(name="스킬", value="**EX 스킬: 코스트{0[cost]}**\n(**{0[name]}**) {0[describe]}\n\
                                            **노말 스킬**\n(**{1[name]}**) {1[describe]}\n\
                                            **패시브 스킬**\n(**{2[name]}**) {2[describe]}\n\
                                            **서브 스킬**\n(**{3[name]}**) {3[describe]}\n".format(
                                                result["skills"]["ex"], result["skills"]["basic"], result["skills"]["passive"], result["skills"]["sub"]), inline=False)
        
        #embed.add_field(name="보정", value=1)

        return await ctx.send(embed=embed)

def setup(arona : arona.Arona):
    arona.add_cog(Character(arona))