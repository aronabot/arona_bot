import os
import ijson
import json
import asyncio

class Extraction:
    def __init__(self, src_config: str):
        self.config = self._get_config(src_config)
        self.table = None

    def _get_config(self, src_config: str):
        try:
            with open(src_config, "r", encoding="utf-8") as data:
                return json.load(data)["local"]

        except FileNotFoundError:
            raise FileNotFoundError

    def _get_src(self, key: str) -> str:
        try:
            return os.path.join(self.config["src"], self.config[key])

        except KeyError:
            raise KeyError
    
    def set_table(self, table: str):
        self.table = table

    def extract(self, key: str, item: str) -> dict:
        try:
            with open(self._get_src(self.table), "r", encoding="utf-8") as data:
                objects = ijson.items(data, "DataList.item")
                name = (obj for obj in objects if obj[key] == item)

                for n in name:
                    return n

        except KeyError:
            raise KeyError

class CharacterInfoBuilder:
    def __init__(self):
        self.extraction = Extraction("./config.json")
        self.character_info = {}

    async def _set_property(self, table: str, key: str, item: str, prop: list) -> dict:
        self.extraction.set_table(table)
        result = self.extraction.extract(key, item)
        if result == None:
            return None
        return {k: result[k] for k in prop}

    async def _set_default(self, item):
        prop = ["Id", "DevName", "Rarity", "TacticEntityType", "TacticRole", 
                    "WeaponType", "BulletType", "ArmorType", "AimIKType", "School",
                    "Club", "DefaultStarGrade", "EquipmentSlot"]

        return await self._set_property("Character", "DevName", item, prop)
        
    async def _set_stat(self, item):
        prop = ["CharacterId", "DevName", "AttackPower1", "MaxHP1", "DefensePower1",
                "HealPower1", "DodgePoint", "AccuracyPoint", "CriticalPoint", "Range",
                "StreetBattleAdaptation", "OutdoorBattleAdaptation", "IndoorBattleAdaptation"]

        return await self._set_property("CharacterStat", "CharacterId", item, prop)

    async def _set_profile(self, item):
        prop = ["CharacterId", "PersonalNameKr", "PersonalNameJp", "StatusMessageKr"]
        return await self._set_property("LocalizeCharProfile", "CharacterId", item, prop)

    async def _set_skill(self, item):
        prop = ["CharacterId", "DevName", "NormalSkillGroupId", "ExSkillGroupId", "PublicSkillGroupId", 
                "PassiveSkillGroupId", "ExtraPassiveSkillGroupId"]
        return await self._set_property("CharacterSkillList", "CharacterId", item, prop)

    async def _set_skills(self, item):
        prop = ["LocalizeSkillId", "GroupId", "SkillCost"]
        return await self._set_property("Skill", "GroupId", item, prop)

    async def _set_skills2(self, item):
        prop = ["Key", "NameKr", "DescriptionKr"]
        return await self._set_property("LocalizeSkill", "Key", item, prop)


class Constructure:
    def __init__(self):
        self.builder = CharacterInfoBuilder()

    async def construct(self, item: str):
        a = await self.builder._set_default(item)
        id = a["Id"]
        p = await asyncio.gather(self.builder._set_profile(id), self.builder._set_stat(id), self.builder._set_skill(id))
        for q in p:
            a.update(q)

        tasks = []
        tasks += [asyncio.create_task(self.builder._set_skills(i)) for i in a["NormalSkillGroupId"]]
        tasks += [asyncio.create_task(self.builder._set_skills(i)) for i in a["ExSkillGroupId"]]
        tasks += [asyncio.create_task(self.builder._set_skills(i)) for i in a["PublicSkillGroupId"]]
        tasks += [asyncio.create_task(self.builder._set_skills(i)) for i in a["PassiveSkillGroupId"]]
        tasks += [asyncio.create_task(self.builder._set_skills(i)) for i in a["ExtraPassiveSkillGroupId"]]

        b = await asyncio.gather(*tasks)

        for b1 in b:
            print(await self.builder._set_skills2(b1["LocalizeSkillId"]))

