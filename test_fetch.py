import requests
import unittest
from bs4 import BeautifulSoup
from unittest.mock import patch, MagicMock
from fetch import fetch, download_assets, rewrite_urls, save_html

class TestFetch(unittest.TestCase):
    @patch('requests.get')
    def test_fetch(self, mock_get):
        mock_response = MagicMock()
        mock_response.text = '<html></html>'
        mock_get.return_value = mock_response

        fetch('http://example.com', False)

        mock_get.assert_called_once_with('http://example.com')

    @patch('requests.get')
    def test_download_assets(self, mock_get):
        mock_response = MagicMock()
        mock_response.content = b''
        mock_get.return_value = mock_response

        soup = BeautifulSoup('<html><img src="http://example.com/image.jpg"></html>', 'html.parser')
        download_assets(soup, 'http://example.com', '.')

        mock_get.assert_called_once_with('http://example.com/image.jpg', headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'})

    def test_rewrite_urls(self):
        soup = BeautifulSoup('<html><img src="http://example.com/image.jpg"></html>', 'html.parser')
        soup = rewrite_urls(soup, 'http://example.com', '.')

        self.assertEqual(soup.find('img')['src'], 'image.jpg')

    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    def test_save_html(self, mock_open):
        soup = BeautifulSoup('<html></html>', 'html.parser')
        save_html(soup, 'output.html')

        mock_open.assert_called_once_with('output.html', 'w', encoding='utf-8')
        handle = mock_open()
        handle.write.assert_called_once_with('<html></html>')

    @patch('requests.get')
    def test_fetch_with_valid_url(self, mock_get):
        mock_response = MagicMock()
        mock_response.text = '<html></html>'
        mock_get.return_value = mock_response

        fetch('http://example.com', False)

        mock_get.assert_called_once_with('http://example.com')

if __name__ == '__main__':
    unittest.main()
