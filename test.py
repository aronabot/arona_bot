from UpdateData.Build.Constructure import *
import re

async def main():
    p = re.compile(r"\[.*?\]|/")
    q = re.compile(r"[\n]")
    p.sub("", "[a]안녕하세요")
    q.sub(" ", "")
    c = Constructure()

    r = re.compile(r"Shizuko(?P<skill_name>.*)[0-9]{2,}")
    r.search('ShizukoEx01').group("skill_name")
    
    text = await c.construct("Shizuko_default")
    text["ShizukoEx01"]["DescriptionKr"] = p.sub("", text["ShizukoEx01"]["DescriptionKr"])
    text["ShizukoEx01"]["DescriptionKr"] = q.sub(" ", text["ShizukoEx01"]["DescriptionKr"])


    print(text)
    print(text["ShizukoEx01"]["DescriptionKr"])

if __name__ == "__main__":
    asyncio.run(main())