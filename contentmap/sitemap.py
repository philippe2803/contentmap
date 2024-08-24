import asyncio
import logging
from typing import Literal
import requests
import os

import aiohttp
import trafilatura
from tqdm.asyncio import tqdm_asyncio
from lxml import etree

from contentmap.core import ContentMapCreator


class SitemapToContentDatabase:
    SOURCE_TYPE_URL: Literal['url'] = 'url'
    SOURCE_TYPE_DISK: Literal['disk'] = 'disk'
    SourceType = Literal['url', 'disk']

    def __init__(self, sitemap_sources: list,
                 source_type: SourceType = SOURCE_TYPE_URL,
                 seconds_timeout=10,
                 concurrency=None,
                 include_vss=False):
        self.sitemap_sources = sitemap_sources
        self.source_type = source_type
        self.semaphore = asyncio.Semaphore(concurrency) if concurrency is not None else None
        self.timeout = aiohttp.ClientTimeout(
            sock_connect=seconds_timeout,
            sock_read=seconds_timeout
        )
        self.include_vss = include_vss

    def build(self):
        urls = self.get_urls()
        loop = asyncio.get_event_loop()
        contents = loop.run_until_complete(self.get_contents(urls))
        cm = ContentMapCreator(contents, include_vss=self.include_vss)
        cm.build()

    def get_urls(self):
        all_urls = []
        if self.source_type == self.SOURCE_TYPE_URL:
            for sitemap_url in self.sitemap_sources:
                urls = self._get_urls_from_url(sitemap_url)
                all_urls.extend(urls)
        elif self.source_type == self.SOURCE_TYPE_DISK:
            for directory in self.sitemap_sources:
                for filename in os.listdir(directory):
                    if filename.endswith('.xml'):
                        filepath = os.path.join(directory, filename)
                        urls = self._get_urls_from_disk(filepath)
                        all_urls.extend(urls)
        return all_urls

    def _get_urls_from_url(self, sitemap_url):
        r = requests.get(sitemap_url)
        tree = etree.fromstring(r.content)
        return self._extract_urls_from_tree(tree)

    def _get_urls_from_disk(self, filepath):
        tree = etree.parse(filepath)
        return self._extract_urls_from_tree(tree)

    def _extract_urls_from_tree(self, tree):
        return [
            url.text for url
            in tree.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc")
        ]

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
