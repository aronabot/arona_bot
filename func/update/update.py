import asyncio
import discord
import pymysql
import aiohttp
import io
import os
import hashlib
from discord.ext import commands

from .parser import GoogleSheet
import arona

class Update(commands.Cog):
    def __init__(self, arona: arona.Arona):
        self.arona = arona
        self.current_task = 0
        self.task_queue = []
        self._init_database()

    @commands.is_owner()
    @commands.command(name="dummy_update")
    async def _dummy_update(self, ctx):
        await ctx.send("더미 업데이트를 진행합니다.")
        self.arona.updating = True

        await asyncio.sleep(20)

        await ctx.send("더미 업데이트를 종료합니다.")
        self.arona.updating = False

    @commands.is_owner()
    @commands.command(name="update")
    async def _update(self, ctx):
        raw_data, downloader  = {}, GoogleSheet()
        await ctx.send("업데이트를 진행합니다.")
        self.arona.updating = True

        for url in self.arona.config["mirror"]:
            try:
                raw_data = await downloader.download(url)
                if raw_data != {}:
                    break

            except Exception as e:
                print(e)
            
        if raw_data == {}:
            await ctx.send("업데이트에 실패하였습니다.")
            self.arona.updating = False
            return
        
        try:
            await self._update_character(ctx, raw_data["character"])
            
        except Exception as e:
            print(e)

        self.arona.updating = False
        return await ctx.send("업데이트를 성공적으로 마쳤습니다.")

    async def _update_character(self, ctx, sheets):
        #전체 캐릭터 시트 업데이트
        sql = "SELECT name FROM characters"
        have_datas = self._execute(sql)
        
        have_datas = have_datas and [c[0] for c in have_datas] or []

        sheets = [[{k: v for k, v in data.items()} for data in sheet if data["name"] not in have_datas] for sheet in sheets]
        total_task = 0
        for sheet in sheets:
            total_task += len(sheet)

        await ctx.send("**{0}**명의 학생 데이터를 업데이트 합니다. 잠시만 기다려주세요...".format(total_task))
        if total_task == 0:
            return

        self.current_task = 0
        update_msg = await ctx.send("**{0}**/{1}".format(total_task, self.current_task))

        positions = self._execute("SELECT * FROM positions", option=pymysql.cursors.DictCursor)
        positions = self._list_to_dict(positions)

        tasks = [asyncio.create_task(self._insert_character(total_task, update_msg, positions, sheet)) for sheet in sheets]
        print("===")
        await asyncio.gather(*tasks)
        print("===")

    async def _upload_character_icon(self, name, url):
        #캐릭터 아이콘 업로드
        icon_channel = self.arona.config["discord"]["character"]["icon"]
        icon_channel = self.arona.get_channel(icon_channel)

        sql = "UPDATE characters SET icon=%s WHERE name=%s"
        message = None
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status not in range(200, 300):
                    return print("Colud not download icon of {0}".format(name))
                
                icon = io.BytesIO(await resp.read())
                message = await icon_channel.send(file=discord.File(icon, "{0}.png".format(name)))
                self._execute(sql, (message.id, name))
                await asyncio.sleep(20)
        return 
        
    async def _insert_character(self, tt, msg, positions, sheet):
        #단일 캐릭터 업데이트
        sql = "INSERT INTO characters(name, combat_outdoor, combat_urban, combat_indoor, HP, ATK, DEF, HEAL, ACC, EVA, CRI, STA, RAN,\
               type, attack_type, defence_type, position_a, position_b)\
               SELECT %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, \
               %s, %s, %s, %s, %s\
               FROM DUAL WHERE NOT EXISTS(SELECT id FROM characters WHERE name=%s)"

        calist = ["outdoor", "urban", "indoor"]
        slist = ["HP", "ATK", "DEF", "HEAL", "ACC", "EVA", "CRI", "STA", "RAN"]
        elist = ["type", "attack_type", "defence_type"]
        
        for data in sheet:
            try:
                positions_a = [0]
                positions_b = [0]
                
                try:
                    async with aiohttp.ClientSession() as session:
                        async with session.get(data["position1"][0]) as resp:
                            h = hashlib.md5(await resp.read()).hexdigest()
                            positions_a = [positions[str(h)]]
                        async with session.get(data["position2"][0]) as resp:
                            h = hashlib.md5(await resp.read()).hexdigest()
                            positions_b = [positions[str(h)]]
                except Exception as e:
                    print(e)
                        

                cal = [data["combat_advantage"][e] for e in calist]
                sl = [data["status"][e] for e in slist]
                el = [data[e] for e in elist]

                self._execute( sql, tuple([data["name"]] + cal + sl + el + positions_a + positions_b + [data["name"]]) )
                await self._upload_character_icon(data["name"], data["icon"])
            except Exception as e:
                print(e)

            self.current_task += 1
            await msg.edit(content="**{0}**/{1}".format(tt, self.current_task))

    def _execute(self, sql, data=None, option=None):
        #sql 실행 함수
        conn = pymysql.connect(**self.arona.config["connect"])
        order = data and [sql, data] or [sql]
        result = None
        try:
            with conn.cursor(option) as curs:
                curs.execute(*order)
                if sql.startswith("SELECT"):
                    result = curs.fetchall()
                else:
                    conn.commit()
        except Exception as e:
            print(e)
        finally:
            conn.close()

        return result

    def _list_to_dict(self, l: list)->dict:
        return {sub_dict["ref_hash"]: sub_dict["name"] for sub_dict in l}

        
    def _init_database(self):
        # 데이터베이스 초기화
        p_data = "./func/update/position_data"
        conn = pymysql.connect(**self.arona.config["connect"])

        cursor = conn.cursor()
        for f in [file for file in os.listdir("./sql") if file.endswith(".sql")]:
            with open(os.path.join("./sql", f), "r", encoding="utf-8") as data:
                try:
                    for sql in data.read().split(";")[:-1]:
                        cursor.execute("{0};".format(sql))
                        conn.commit()

                except Exception as e:
                    print(e)

        for f in [file for file in os.listdir(p_data)]:
            isql = "INSERT INTO positions(ref_hash, name) SELECT %s, %s FROM DUAL WHERE NOT EXISTS(SELECT name FROM positions WHERE name = %s)"
            self._execute(isql, ("0", "없음", "없음"))
            with open(os.path.join(p_data, f), "rb") as img:
                try:
                    ref_hash = hashlib.md5(img.read()).hexdigest()
                    name = f.split(".")[0]
                    self._execute(isql, (ref_hash, name, name))
                except Exception as e:
                    print(e)

        conn.close()

def setup(arona: arona.Arona):
    arona.add_cog(Update(arona))