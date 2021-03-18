from urllib.parse import urlparse

import asyncio
import aiohttp
import aiofiles
import json
from bs4 import BeautifulSoup

class GoogleSheets:
    """
    values:
        url: 크롤링할 사이트의 주소
        term_src: 해당 시트의 schema를 rename 시키는 dict의 위치
        skey: 해당 시트 skill의 정보가 있는 부분의 schema다.
        mkey: 해당 시트의 데일리 미션과 위클리 미션 부분의 schema다.
        ckey: 해당 시트 charater의 정보가 있는 부분의 schema다.
    """
    __slots__ = ["url", "term_src"]
    bkey = ['주로 얻을 수 있는 위치. 제조에서도 얻을 수 있음', '이미지', '이름', '획득처']
    skey = ["이미지", "이름", "코스트",  "내용", "노말스킬", "패시브스킬", "서브스킬", "비고",]
    mkey = ['デイリー 데일리 / 일일 미션', 'ウィークリー 위클리 / 주간 미션', '미션명', '보상', '번역', '비고', '미션명', '보상', '번역', '비고']
    ckey = ['이미지', '이름', '편성위치', 'HP', '공격력', '방어력', '치유력', '명중치', '회피치', '치명타', '안정치', '사정거리', '역할', '엄폐', '무기', '공격타입', '방어타입', '장소 보너스']
    
    def __init__(self):
        self.url = None
        self.term_src = None

    def set_url(self, url: str):
        self.url = url

    def set_term(self, term_src: str):
        self.term_src = term_src

    def _check_key(self, table) -> bool:
        #이 함수는 해당 table의 첫 칼럼(schema에 대응된다.)의 요소가 skey나 ckey의 값을 포함하고 있는지 확인하는 함수이다.
        #칼럼이 짧은 순으로 비교하도록 유도한다.
        #알맞은 키를 반환한다. (데이터 파싱에 도움을 받기 위해서이다.)
        keys = sorted([self.bkey, self.skey, self.mkey, self.ckey], key=lambda x: len(x))
        try:
            flag = [set(table[0:len(key)]) - set(key) == set() for key in keys]
            return any(flag), [x for m, x in zip(flag, keys) if m][0]
        except TypeError:
            #print(type(table), table)
            return False, None

    async def parsing(self, table, term):
        result = []
        temps = [[el.text or [t.attrs["src"] for t in el("img")] for el in row("td") if el.text or el("div")] for row in table]

        for t in temps:
            flag, keys = self._check_key(t)
            if not flag:
                continue
            keys[0]
            idxs = [i for i, v in enumerate(t) if isinstance(v, list)]
            try:
                result += [t[i:j] for i, j in zip([0]+idxs, idxs + [len(t) if t[-1] != len(t) else []])][1:]
            except IndexError:
                continue
                
            
        return result

    async def download(self) -> list:
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url) as response:
                if response in range(200, 300):
                    print("DOWNLOAD ERROR")
                    return
                
                with open(self.term_src, "r", encoding="utf-8") as data:
                    term = json.load(data)
                    
                    bs = BeautifulSoup(await response.text(), "html.parser")("table")
                    tasks = [asyncio.create_task(self.parsing(b, term)) for b in bs]
                    table = await asyncio.gather(*tasks)

        return table

class Connector:
    controller = { "docs.google.com" : GoogleSheets() }
    __slots__ = ["site", "term_src"]

    def __init__(self, url_list, term_src : str):
        self.site = {url: urlparse(url).netloc for url in url_list}
        self.term_src = term_src

    async def download(self) -> list:
        for url, loc in self.site.items():
            current_cont = self.controller[loc]
            current_cont.set_url(url)
            result = await current_cont.download()

            if result != []:
                break
        
        #만약 result가 제대로 나오지 않는다면 인터넷 연결이나
        #confing mirror에 적힌 사이트들에 문제가 생긴 것 이므로 다른 사이트를 이용하도록 한다.
        return result
