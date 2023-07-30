import argparse
import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime
from urllib.request import urlopen, urlretrieve
from urllib.parse import urljoin, urlparse

def fetch(url, metadata):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except Exception as err:
        print(err)
        
        return

    soup = BeautifulSoup(response.text, 'html.parser')

    dir = url.replace('https://', '').replace('http://', '')

    if not os.path.exists(dir):
        os.makedirs(dir)
 
    soup = download_assets(soup, url, dir)
    html = rewrite_urls(soup, url, dir)
    save_html(html, dir + '/index.html')

    if metadata:
        num_links = len(soup.find_all('a'))
        num_images = len(soup.find_all('img'))
        last_fetch = datetime.now().strftime('%a %b %d %Y %H:%M %Z')
        print(f'site: {url}\nnum_links: {num_links}\nimages: {num_images}\nlast_fetch: {last_fetch}')

def download_assets(soup, url, output_folder):
    assets_details = extract_asset_details(soup, url)
    
    for tag, asset_url, asset_filename in assets_details:
        if not asset_filename:
            continue

        outpath = os.path.join(output_folder, asset_filename)

        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

        try:
            response = requests.get(asset_url, headers=headers)
        except Exception as err:
            print(err)
            return

        with open(outpath, 'wb') as out_file:
            out_file.write(response.content)

    return soup

def rewrite_urls(soup, url, output_folder):
    assets_details = extract_asset_details(soup, url)
    
    for tag, asset_url, asset_filename in assets_details:
        local_path = os.path.join(output_folder, asset_filename)
        stripped_path = local_path.split('/', 1)[-1]

        if tag.name == 'img':
            tag['src'] = stripped_path
        elif tag.name == 'script':
            tag['src'] = stripped_path
        else:  
            tag['href'] = stripped_path

    return soup

def extract_asset_details(soup, base_url):
    asset_tags = soup.find_all(['img', 'script', 'link'])
    
    asset_details = []

    for tag in asset_tags:
        original_url = tag.get('src') or tag.get('href')
        if original_url is None:
            continue
        
        asset_url = urljoin(base_url, original_url)
        asset_filename = os.path.basename(urlparse(asset_url).path)
        
        asset_details.append((tag, asset_url, asset_filename))
        
    return asset_details

def save_html(soup, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(str(soup))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('urls', nargs='+')
    parser.add_argument('--metadata', action='store_true')
    args = parser.parse_args()

    for url in args.urls:
        fetch(url, args.metadata)

if __name__ == '__main__':
    main()
