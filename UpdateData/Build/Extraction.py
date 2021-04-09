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

    def extract(self, key: str, item=None) -> dict:
        try:
            with open(self._get_src(self.table), "r", encoding="utf-8") as data:
                objects = ijson.items(data, "DataList.item")
                if item != None:
                    name = (obj for obj in objects if obj[key] == item)
                    return [n for n in name][0]
                
                name = (obj for obj in objects)
                return [n for n in name]

        except KeyError:
            raise KeyError