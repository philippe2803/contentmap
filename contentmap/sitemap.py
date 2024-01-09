import asyncio
import logging
import requests

import aiohttp
import trafilatura
from tqdm.asyncio import tqdm_asyncio
from lxml import etree

from contentmap.core import ContentMapCreator


class SitemapToContentDatabase:

    def __init__(self, sitemap_url, seconds_timeout=10, concurrency=None):
        self.sitemap_url = sitemap_url
        self.semaphore = asyncio.Semaphore(concurrency) if concurrency is not None else None
        self.timeout = aiohttp.ClientTimeout(
            sock_connect=seconds_timeout,
            sock_read=seconds_timeout
        )

    def load(self):
        urls = self.get_urls()
        loop = asyncio.get_event_loop()
        contents = loop.run_until_complete(self.get_contents(urls))
        cm = ContentMapCreator(contents)
        cm.build()

    def get_urls(self):
        r = requests.get(self.sitemap_url)
        tree = etree.fromstring(r.content)
        urls = [
            url.text for url
            in tree.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc")
        ]
        return urls

    async def get_contents(self, urls):
        async with aiohttp.ClientSession(timeout=self.timeout) as session:
            tasks = [self.fetch_content(session, url) for url in urls]
            return await tqdm_asyncio.gather(*tasks)

    async def fetch_content(self, session, url):
        try:
            if not self.semaphore:
                async with session.get(url) as response:
                    raw = await response.text()
            else:
                async with self.semaphore, session.get(url) as response:
                    raw = await response.text()
            content = trafilatura.extract(raw)
            return {"url": url, "content": content}

        except aiohttp.ClientConnectionError as e:
            logging.error(f"Error while fetching {url}: {e.__repr__}")
            return None
