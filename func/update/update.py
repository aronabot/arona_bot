import asyncio
import discord
import pymysql
import os
from discord.ext import commands

from .parser import GoogleSheet
import arona

class Update(commands.Cog):
    def __init__(self, arona: arona.Arona):
        self.arona = arona
        self._init_database()


    @commands.is_owner()
    @commands.command(name="update")
    async def _update(self, ctx):
        raw_data, downloader  = {}, GoogleSheet()
        await ctx.send("업데이트를 진행합니다.")

        for url in self.arona.config["mirror"]:
            try:
                raw_data = await downloader.download(url)
                if raw_data != {}:
                    break

            except Exception as e:
                print(e)
            
        if raw_data == {}:
            await ctx.send("업데이트에 실패하였습니다.")
            return
        
        try:
            await self._infoupdate(raw_data["character"])
            
        except Exception as e:
            print(e)

        return await ctx.send("업데이트를 성공적으로 마쳤습니다.")
        
    async def _insert_character(self, sheet):
        sql = "INSERT INTO characters(name, combat_outdoor, combat_urban, combat_indoor, HP, ATK, DEF, HEAL, ACC, EVA, CRI, STA, RAN)\
               SELECT %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s\
               FROM DUAL WHERE NOT EXISTS(SELECT id FROM characters WHERE name=%s)"

        calist = ["outdoor", "urban", "indoor"]
        slist = ["HP", "ATK", "DEF", "HEAL", "ACC", "EVA", "CRI", "STA", "RAN"]

        for data in sheet:
            ca = [data["combat_advantage"][e] for e in calist]
            s = [data["status"][e] for e in slist]
            self._insert(sql, tuple([data["name"]] + ca + s + [data["name"]]))

        pass

    async def _infoupdate(self, sheets):
        tasks = [asyncio.create_task(self._insert_character(sheet)) for sheet in sheets]
        await asyncio.gather(*tasks)
        
    def _init_database(self):
        database = pymysql.connect(**self.arona.config["connect"])

        cursor = database.cursor(pymysql.cursors.DictCursor)
        with open("./init_character.sql", "r", encoding="utf-8") as data:
            try:
                for sql in data.read().split(";"):
                    cursor.execute("{0};".format(sql))

            except Exception as e:
                print(e)

        database.close()

    def _insert(self, sql, data):
        conn = pymysql.connect(**self.arona.config["connect"])
        try:
            with conn.cursor() as curs:
                curs.execute(sql, data)
                conn.commit()
        finally:
            conn.close()


def setup(arona: arona.Arona):
    arona.add_cog(Update(arona))