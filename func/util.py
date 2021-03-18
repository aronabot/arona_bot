import asyncio
import discord
from discord.ext import commands

__all__ = ["sendmsg"]

async def sendmsg(ctx, message):
    """
    args :
        message:
            ```로 감싸서 보낼 메세지의 내용
    returns :
        ctx.send한 메세지 객체 만약 message내용이 없을경우
        None을 반환한다.
    """
    return message and await ctx.send("```{0}```".format(message)) or None