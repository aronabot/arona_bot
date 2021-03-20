from abc import ABC, abstractmethod

import asyncio
import aiohttp
import aiofiles
import hashlib
import json

from bs4 import BeautifulSoup

class ParserMissingError(Exception):
    def __init__(self):
        super().__init__("This format haven't Parser")

class Parser(ABC):
    """
    values:
        column  : 해당 시트의 schema
        rule    : 해당 시트의 데이터 순서(규칙)
        term    : 해당 시트 schema의 변환 규칙
    """
    __slots__ = ["column", "rule", "term"]
    def __init__(self, column, rule, term):
        self.column = column
        self.rule = rule
        self.term = term

    @abstractmethod
    async def parsing(self, table):
        pass

class CharacterInfoParser(Parser):
    #스킬 정보 파서
    def _preprocess(self, table) -> list:
        c, r = len(self.column), len(self.rule)
        table = table[c:]
        return [table[i*r : (i+1)*r] for i, _ in enumerate(table[::r])]

    async def _tojson(self, subtable) -> dict:
        advantage = ["outdoor", "urban", "indoor"]
        status = ["HP", "ATK", "DEF", "HEAL", "ACC", "EVA", "CRI", "STA", "RAN"]
        
        result = {self.term[k]: v for k, v in zip(self.rule, subtable) if self.term[k] != ""}

        result["icon"] = result["icon"][0]

        result["combat_advantage"] = {k: result.pop(k) for k in advantage}
        result["status"] = {k: int(result.pop(k)) for k in status}

        return result

    async def parsing(self, table) -> list:
        """
        arg: 
            table: 파싱해야하는 데이터들
        return:
            파싱이 끝난 데이터 dict 형태로 반환된다.
        """
        table = self._preprocess(table)
        tasks = [asyncio.create_task(self._tojson(subtable)) for subtable in table]
        return await asyncio.gather(*tasks)


class SkillsInfoParser(Parser):
    #스킬 정보 파서 
    def _preprocess(self, table) -> list:
        c, t = len(self.column), len(table)
        table = table[c:]
        index = [i for i, d in enumerate(table) if isinstance(d, list)]
        return [table[i:j] for i, j in zip([0]+index, index+[t])][1:]

    async def _tojson(self, subtable) -> dict:
        result = {self.term[k]: v for k, v in zip(self.rule, subtable) if self.term[k] != ""}

        del result["icon"]

        result["ex"] = {
            "cost": int(result.pop("cost")), 
            "content": result.pop("ex")
        }
        result["basic"] = {
            "content": result.pop("basic")
        }
        result["passive"] = {
            "content": result.pop("passive")
        }
        result["sub"] = {
            "content": result.pop("sub")
        } 

        return result

    async def parsing(self, table) -> list:
        """
        arg: 
            table: 파싱해야하는 데이터들
        return:
            파싱이 끝난 데이터 dict 형태로 반환된다.
        """
        table = self._preprocess(table)
        tasks = [asyncio.create_task(self._tojson(subtable)) for subtable in table]
        return await asyncio.gather(*tasks)


