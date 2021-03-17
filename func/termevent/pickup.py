from datetime import datetime
from .termevent import TermEvent
import json
import asyncio

import discord
from discord.ext import commands

import arona

class Pickup(commands.Cog, TermEvent):
    """
    member values:
        infoch:
            type: dict
            이벤트의 정보를 담고있는 채널의 목록
        current_event:
            현재 픽업에 대한 정보
        future_event:
            다음 픽업에 대한 정보
    """
    __slots__ = ["infoch", "current_event", "future_event"]

    def __init__(self, arona: arona.Arona):
        self.arona = arona
        self.infoch = {k : self.arona.get_channel(v) 
                        for k, v in self.arona.server["event"].items()
                        if k not in ["bossinfo", "event", "totalwar"]}

        self.current_event = {}
        self.future_event = {}

    async def _update_pickup(self, now : datetime):
        events = []
        async for msg in self.infoch["pickup"].history(limit=5):
            events += [json.loads(msg.content)]

        events.reverse()
        events += [{}]

        return self._update_event(now, events)
    
    async def _get_message(self, content):
        for k in ["thumbnail", "reward"]:
            content[k] = await self.infoch[k].fetch_message(content[k])

        return content

    @commands.command(name="픽업초기화")
    async def _reset_pickup(self, ctx):
        self.current_event = {}

    @commands.command(name="픽업테스트")
    async def _get_spickup(self, ctx, month, day):
        now = datetime(year=2021, month=int(month), day=int(day))
        if self.current_event == {} or self.current_event['to'] < now:
            self.current_event, self.future_event = await self._update_pickup(now)

            if self.current_event == {}:
                return await ctx.send("현재 진행 중인 **픽업 이벤트**가 없습니다.")

            self.current_event = await self._get_message(self.current_event)

        if self.current_event == {}:
            return await ctx.send("현재 진행 중인 **픽업 이벤트**가 없습니다.")

        f = self.current_event["from"].strftime("%m-%d")
        t = self.current_event["to"].strftime("%m-%d")
        content = "**{0}**\n**{1}** ~ **{2}**\n".format(self.current_event["name"], f, t)

        await ctx.send(content)
        await ctx.send(self.current_event["thumbnail"].attachments[0].url)

    @commands.command(name="픽업")
    async def _get_pickup(self, ctx):
        now = datetime.now()
        if self.current_event == {} or self.current_event['to'] < now:
            self.current_event, self.future_event = await self._update_pickup(now)

            if self.current_event == {}:
                return await ctx.send("현재 진행 중인 **픽업 이벤트**가 없습니다.")

            self.current_event = await self._get_message(self.current_event)
        
        if self.current_event == {}:
            return await ctx.send("현재 진행 중인 **픽업 이벤트**가 없습니다.")
            
        f = self.current_event["from"].strftime("%m-%d")
        t = self.current_event["to"].strftime("%m-%d")
        content = "**{0}**\n**{1}** ~ **{2}**\n".format(self.current_event["name"], f, t)

        await ctx.send(content)
        await ctx.send(self.current_event["thumbnail"].attachments[0].url)


def setup(arona : arona.Arona):
    arona.add_cog(Pickup(arona))