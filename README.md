# Content map

A way to share content from a specific domain using SQLite as an alternative to 
RSS feeds. The purpose of this library is to simply create a dataset for all the
content on your website, using the XML sitemap as a starting point.  

Possibility to include vector search similarity features in the dataset very easily.

Article that explains the rationale behind this type of datasets [here](https://philippeoger.com/pages/can-we-rag-the-whole-web/).


## Installation

```bash

pip install contentmap

```

## Quickstart

To build your contentmap.db with vector search capabilities and containing all 
your content using your XML sitemap as a starting point, you only need to write the
following: 

```python
from contentmap.sitemap import SitemapToContentDatabase

database = SitemapToContentDatabase(
    sitemap_sources=["https://yourblog.com/sitemap.xml"],
    concurrency=10,
    include_vss=True
)
database.build()

```

This will automatically create the SQLite database file, with vector search 
capabilities (piggybacking on sqlite-vss integration on Langchain).
