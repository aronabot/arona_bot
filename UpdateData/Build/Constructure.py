from .CharacterInfoBuilder import asyncio, CharacterInfoBuilder

class Constructure:
    def __init__(self):
        self.builder = CharacterInfoBuilder()

    async def construct(self, item: str):
        return await self.builder.build(item)