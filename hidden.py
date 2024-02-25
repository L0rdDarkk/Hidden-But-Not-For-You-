import argparse
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

logo = r"""
db   db d888888b d8888b. d8888b. d88888b d8b   db   d8888b. db    db d888888b   d8b   db  .d88b.  d888888b   d88888b  .d88b.  d8888b.   db    db  .d88b.  db    db 
88   88   `88'   88  `8D 88  `8D 88'     888o  88   88  `8D 88    88 `~~88~~'   888o  88 .8P  Y8. `~~88~~'   88'     .8P  Y8. 88  `8D   `8b  d8' .8P  Y8. 88    88 
88ooo88    88    88   88 88   88 88ooooo 88V8o 88   88oooY' 88    88    88      88V8o 88 88    88    88      88ooo   88    88 88oobY'    `8bd8'  88    88 88    88 
88~~~88    88    88   88 88   88 88~~~~~ 88 V8o88   88~~~b. 88    88    88      88 V8o88 88    88    88      88~~~   88    88 88`8b        88    88    88 88    88 
88   88   .88.   88  .8D 88  .8D 88.     88  V888   88   8D 88b  d88    88      88  V888 `8b  d8'    88      88      `8b  d8' 88 `88.      88    `8b  d8' 88b  d88 
YP   YP Y888888P Y8888D' Y8888D' Y88888P VP   V8P   Y8888P' ~Y8888P'    YP      VP   V8P  `Y88P'     YP      YP       `Y88P'  88   YD      YP     `Y88P'  ~Y8888P 
"""
author=""" By L0rdDarkk"""
COMMON_PATHS = [
    "admin", "login", "wp-admin", "wp-login", "administrator", 
    "phpmyadmin", "admin.php", "login.php", "index.php", 
    "backup", "uploads", "images", "css", "js", "fonts"
]

def generate_paths(url):
    paths = set()
    for path in COMMON_PATHS:
        paths.add(urljoin(url, path))
    return paths

def get_internal_links(url, html_content):
    internal_links = set()
    soup = BeautifulSoup(html_content, 'html.parser')
    for link in soup.find_all('a', href=True):
        absolute_link = urljoin(url, link['href'])
        parsed_link = urlparse(absolute_link)
        if parsed_link.netloc == urlparse(url).netloc:
            internal_links.add(absolute_link)
    return internal_links

def dirsearch(target_url, recursive=False):
    discovered_directories = set()
    paths_to_scan = generate_paths(target_url)

    while paths_to_scan:
        path = paths_to_scan.pop()
        if path in discovered_directories:
            continue

        response = requests.get(path)
        if response.status_code == 200:
            print(f"[+] Directory found: {path}")
            discovered_directories.add(path)

            if recursive:
                internal_links = get_internal_links(path, response.text)
                for link in internal_links:
                    paths_to_scan.add(link)

        elif response.status_code != 404:
            print(f"[?] Possible directory: {path}")

def main():
    print(logo)  
    print(author)
    parser = argparse.ArgumentParser(description="Simple directory scanner")
    parser.add_argument("-u", "--url", help="Target URL", required=True)
    parser.add_argument("-r", "--recursive", help="Enable recursive directory scanning", action="store_true")
    args = parser.parse_args()

    target_url = args.url
    recursive = args.recursive

    dirsearch(target_url, recursive)

if __name__ == "__main__":
    main()
