# Content map

A way to share content from a specific domain using SQLite as an alternative to 
RSS feeds. The purpose of this library is to simply create a dataset for all the
content on your website, using the XML sitemap as a starting point.


## Installation

```bash

pip install contentmap

```

## Quickstart

To build your contentmap.db that will contain all your content using your XML 
sitemap as a starting point, you only need to write the following: 

```python
from contentmap.sitemap import SitemapToContentDatabase

database = SitemapToContentDatabase("https://yourblog.com/sitemap.xml")
database.load()

```

You can control how many urls can be crawled concurrently and also set some timeout.