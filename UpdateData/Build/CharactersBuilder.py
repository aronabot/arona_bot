from .Extraction import asyncio, json, Extraction

class CharactersBuilder:
    def __init__(self):
        self.extraction = Extraction("./config.json")

        with open("./UpdateData/Build/CharacterInfoConfig.json", "r", encoding="utf-8") as config:
            self.config = json.load(config)

    async def _set_property(self, table: str, key: str, prop: list) -> dict:
        self.extraction.set_table(table)
        result = self.extraction.extract(key)
        if result == None:
            return None
        return {k: result[k] for k in prop}

    async def build(self, _):
        self._set_property("Charcter", , ["Id", "DevName"])

        return result