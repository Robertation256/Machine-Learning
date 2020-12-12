import requests
import asyncio
import aiohttp

class ShiXiSengSpider():
    def __init__(self):
        self._portal = "https://mina.shixiseng.com/mina/interns/search"
        self._storage_path = "C:/Users/yz391/Desktop/CrawlerDownloads/ShiXiSengCrawler"
        self.key_word = ['互联网', '教育', '房产', '广告', '金融', '企业服务', '快消', '电子', '医疗', '汽车']
        self.city = []
        self.max_page = 240
        self.result = ""
        self.count = 0

    def process(self, result):
        msg = result["msg"]
        for m in msg:
            res = f"{self.count}|"
            for value in m.values():
                res += str(value)+"|"
            res += "\n"
            self.result += res
            self.count += 1

    async def async_task(self, page, keyword):
        async with aiohttp.ClientSession() as session:
            async with session.get(self._portal, params={"k": keyword, "page": page}) as response:
                if response.status != 200:
                    return None
                result = await response.json(content_type='text/html',encoding='utf-8')
                self.process(result)

    def run(self):
        loop = asyncio.get_event_loop()
        tasks = []
        for k in self.key_word:
            for page in range(self.max_page):
                tasks.append(self.async_task(page,k))
        loop.run_until_complete(asyncio.wait(tasks))
        loop.close()
        with open("C:/Users/yz391/Desktop/CrawlerDownloads/shixisengFinance.txt", "w", encoding="utf-8") as fp:
            fp.write(self.result)



