import asyncio
import discord
import tqdm
from discord.ext import commands

import arona

def update_decorator(func):
    async def updater(*args, **kwargs):
        await kwargs["ctx"].send("start {0}".format(func.__name__))
        try:
            await func(*args, **kwargs)
            await kwargs["ctx"].send("finish {0}".format(func.__name__))
            return 
        except Exception as e:
            await kwargs["ctx"].send("```py\n{0}: {1}```".format(type(e), e))
            return

    return updater


class UpdateManager:
    def __init__(self, arona: arona.Arona):
        self.arona = arona
        self.cache = None

    @update_decorator
    async def update_dummy(self, ctx, content: str):
        tasks = [asyncio.sleep(1) for i in range(20)]
        await asyncio.gather(*tasks)

    @update_decorator
    async def update_character(self, ctx, content: str):
        pass

    @update_decorator
    async def update_normal_event(self, ctx, content: str):
        pass

    @update_decorator
    async def update_pickup_event(self, ctx, content: str):
        pass

    @update_decorator
    async def update_totalwar_event(self, ctx, content: str):
        pass

    @update_decorator
    async def update_daily_mission(self, ctx, content: str):
        pass

    @update_decorator
    async def update_weekly_mission(self, ctx, content: str):
        pass

    @update_decorator
    async def update_special_mission(self, ctx, content: str):
        pass

