from urllib.parse import urlparse

import asyncio
import aiohttp
import aiofiles
import json
from bs4 import BeautifulSoup

class Connector:
    controller = {}
    __slots__ = ["site", "term_src"]

    def __init__(self):
        pass

