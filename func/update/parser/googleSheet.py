from .parser import *

class GoogleSheet:
    __slots__ = ["parser", "config", "keys"]
    def __init__(self):
        with open("./func/update/parser/config.json", "r", encoding="utf-8") as data:
            self.config = json.load(data)

        self.keys = {i: self.config[i]["key"] for i in self.config if "key" in self.config[i]}
        sinfo = self.config["skills"]
        cinfo = self.config["character"]
        self.parser = {
            "skills": SkillsInfoParser(sinfo["column"], sinfo["rule"], self.config["term"]), 
            "character": CharacterInfoParser(cinfo["column"], cinfo["rule"], self.config["term"])  
        }

    def _check(self, table) -> (bool, str):
        """
        args:
        return:
            bool: 맞는 column이 있는지 확인
            str: 맞는 column이 있다면 그 해당 key를 특정한다.
        """
        keys = sorted(self.keys, key=lambda x: len(self.keys[x]))
        try:
            cidx = [i for i, x in enumerate(table) if isinstance(x, list)][0]
            flag = [set(self.keys[k])-set(table[:cidx]) == set() for k in keys]

            return any(flag), [x for m, x in zip(flag, self.keys) if m][0]
        except IndexError:
            raise IndexError

        except TypeError:
            raise TypeError

    async def _tolist(self, table):
        table = [[el.text or [t.attrs["src"] for t in el("img")] for el in row("td") if el.text or el("div")] for row in table]
        # 빈 시트가 존재할때가 있다.
        for subtable in table:
            try:
                flag, key = self._check(subtable)
                if not flag:
                    continue
                return key, subtable

            except Exception:
                pass

        return None

    async def download(self, url):
        result = {}
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status not in range(200, 300):
                    raise aiohttp.web.HTTPFound(url)

                #원소는 각 시트 정보.
                tables = BeautifulSoup(await resp.text(), "html.parser")("table")
                tasks = [asyncio.create_task(self._tolist(table)) for table in tables]
                tables = [x for x in await asyncio.gather(*tasks) if x is not None]
                for key, data in tables:
                    result[key] = result.get(key, [])
                    result[key].append(data)
                
                for key, table in result.items():
                    tasks = [asyncio.create_task(self.parser[key].parsing(data)) for data in table]
                    result[key] = await asyncio.gather(*tasks)

        return result