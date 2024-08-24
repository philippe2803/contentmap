import os
import unittest
import pytest

from unittest.mock import patch, MagicMock
from contentmap.sitemap import SitemapToContentDatabase


class TestSitemapToContentDatabase(unittest.TestCase):
    def create_mock_response(self, content):
        mock_response = MagicMock()
        mock_response.content = content
        return mock_response

    def generate_sample_sitemap_xml(self, url):
        return f'''
            <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">
                <url>
                    <loc>{url}</loc>
                </url>
            </urlset>'''
    @patch('contentmap.sitemap.requests.get')
    def test_get_urls_given_one_sitemap_url(self, mock_get):
        mock_get.return_value = self.create_mock_response(self.generate_sample_sitemap_xml('https://www.example.com/docs/en/example/?topic=testing'))

        sitemap_db = SitemapToContentDatabase(sitemap_sources=['https://example.com/sitemap.xml'], source_type='url')
        urls = sitemap_db.get_urls()

        self.assertEqual(urls, ['https://www.example.com/docs/en/example/?topic=testing'])
        mock_get.assert_called_once_with('https://example.com/sitemap.xml')


    @patch('contentmap.sitemap.requests.get')
    def test_get_urls_given_multiple_sitemap_urls(self, mock_get):
        mock_get.side_effect = [
            self.create_mock_response(self.generate_sample_sitemap_xml('https://www.example.com/docs/en/example/?topic=testing')),
            self.create_mock_response(self.generate_sample_sitemap_xml('https://www.anotherexample.com/docs/en/example/?topic=contact-us'))
        ]

        sitemap_db = SitemapToContentDatabase(sitemap_sources=['https://example.com/sitemap.xml', 'https://anotherexample.com/sitemap.xml'], source_type='url')
        urls = sitemap_db.get_urls()

        self.assertEqual(urls, [
            'https://www.example.com/docs/en/example/?topic=testing',
            'https://www.anotherexample.com/docs/en/example/?topic=contact-us'
        ])
        mock_get.assert_any_call('https://example.com/sitemap.xml')
        mock_get.assert_any_call('https://anotherexample.com/sitemap.xml')
        self.assertEqual(mock_get.call_count, 2)

    def test_get_urls_given_one_location_on_disk(self):
        sitemap_folder_a_path = os.path.join(os.path.dirname(__file__), 'fixtures', 'sitemap_folder_a')
        sitemap_db = SitemapToContentDatabase(sitemap_sources=[sitemap_folder_a_path], source_type='disk')
        urls = sitemap_db.get_urls()

        self.assertEqual(urls, ['https://www.example.com/docs/en/example/?topic=testing',
                                'https://www.example.com/docs/en/example/?topic=contact-us'
                                ])


    def test_get_urls_given_multiple_locations_on_disk(self):
        sitemap_folder_a_path = os.path.join(os.path.dirname(__file__), 'fixtures', 'sitemap_folder_a')
        sitemap_folder_b_path = os.path.join(os.path.dirname(__file__), 'fixtures', 'sitemap_folder_b')
        sitemap_db = SitemapToContentDatabase(sitemap_sources=[sitemap_folder_a_path, sitemap_folder_b_path], source_type='disk')
        urls = sitemap_db.get_urls()

        self.assertEqual(urls, ['https://www.example.com/docs/en/example/?topic=testing',
                                'https://www.example.com/docs/en/example/?topic=contact-us',
                                'https://www.example.com/docs/en/example/?topic=library-overview',
                                'https://www.example.com/docs/en/example/?topic=about-this-content'
                                ])