from .Extraction import asyncio, json, Extraction

class CharacterInfoBuilder:
    def __init__(self):
        self.extraction = Extraction("./config.json")

        with open("./Func/Build/CharacterInfoConfig.json", "r", encoding="utf-8") as config:
            self.config = json.load(config)

    async def _set_property(self, table: str, key: str, item: str, prop: list) -> dict:
        self.extraction.set_table(table)
        result = self.extraction.extract(key, item)
        if result == None:
            return None
        return {k: result[k] for k in prop}

    async def _set_character(self, item):
        return await self._set_property("Character", "DevName", item, self.config["Character"])
        
    async def _set_character_stat(self, item):
        return await self._set_property("CharacterStat", "CharacterId", item, self.config["CharacterStat"])

    async def _set_localize_char_profile(self, item):
        return await self._set_property("LocalizeCharProfile", "CharacterId", item, self.config["LocalizeCharProfile"])

    async def _set_character_skill_list(self, item):
        return await self._set_property("CharacterSkillList", "CharacterId", item, self.config["CharacterSkillList"])

    async def _set_skill(self, item):
        return await self._set_property("Skill", "GroupId", item, self.config["Skill"])

    async def _set_localize_skill(self, item):
        return await self._set_property("LocalizeSkill", "Key", item, self.config["LocalizeSkill"])

    async def build(self, item):
        result = await self._set_character(item)
        CharacterId = result["Id"]
        default = [self._set_character_stat, self._set_localize_char_profile, self._set_character_skill_list]
        
        for tmp in await asyncio.gather(*[func(CharacterId) for func in default]):
            result.update(tmp)

        skill_groups = ["NormalSkillGroup", "ExSkillGroup", "PublicSkillGroup", "PassiveSkillGroup", "ExtraPassiveSkillGroup"]
        
        
        set_skill_tasks = []
        for group in skill_groups:
            set_skill_tasks += [self._set_skill(id) for id in result["{0}Id".format(group)]]

        skills = {}
        set_localize_skill_tasks = []
        for skill in await asyncio.gather(*set_skill_tasks):
            skills[skill["LocalizeSkillId"]] = skill
            set_localize_skill_tasks += [self._set_localize_skill(skill["LocalizeSkillId"])]

        for localize_skill in await asyncio.gather(*set_localize_skill_tasks):
            skills[localize_skill["Key"]].update(localize_skill)
        
        result.update(skills)
        
        for skill in skills:
            result[result[skill]["GroupId"]] = result[skill]
            del result[skill]

        return result

