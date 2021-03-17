from .connect import Connector
import asyncio
import discord
from discord.ext import commands

import arona

class Updater:
    def __init__(self, arona: arona.Arona):
        self.arona = arona
        self.connector = Connector(arona.config["mirror"])

def setup(arona: arona.Arona):
    arona.add_cog(Updater(arona))