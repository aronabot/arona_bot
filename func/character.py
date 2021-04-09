from discord.ext import commands
import arona

class Character(commands.Cog):
    def __init__(self, arona: arona.Arona):
        pass

def setup(arona: arona.Arona):
    arona.add_cog(Character(arona))