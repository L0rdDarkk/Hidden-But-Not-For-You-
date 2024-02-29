import argparse
import logging
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, quote
from colorama import Fore, Style
from tabulate import tabulate

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logo = r"""
db   db d888888b d8888b. d8888b. d88888b d8b   db   d8888b. db    db d888888b   d8b   db  .d88b.  d888888b   d88888b  .d88b.  d8888b.   db    db  .d88b.  db    db 
88   88   `88'   88  `8D 88  `8D 88'     888o  88   88  `8D 88    88 `~~88~~'   888o  88 .8P  Y8. `~~88~~'   88'     .8P  Y8. 88  `8D   `8b  d8' .8P  Y8. 88    88 
88ooo88    88    88   88 88   88 88ooooo 88V8o 88   88oooY' 88    88    88      88V8o 88 88    88    88      88ooo   88    88 88oobY'    `8bd8'  88    88 88    88 
88~~~88    88    88   88 88   88 88~~~~~ 88 V8o88   88~~~b. 88    88    88      88 V8o88 88    88    88      88~~~   88    88 88`8b        88    88    88 88    88 
88   88   .88.   88  .8D 88  .8D 88.     88  V888   88   8D 88b  d88    88      88  V888 `8b  d8'    88      88      `8b  d8' 88 `88.      88    `8b  d8' 88b  d88 
YP   YP Y888888P Y8888D' Y8888D' Y88888P VP   V8P   Y8888P' ~Y8888P'    YP      VP   V8P  `Y88P'     YP      YP       `Y88P'  88   YD      YP     `Y88P'  ~Y8888P 
"""
author = "By L0rdDarkk"
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

def find(target_url, recursive=False, wordlist=None):
    discovered_directories = set()
    errors = []
    success_messages = []

    paths_to_scan = generate_paths(target_url)

    if wordlist:
        with open(wordlist, 'r') as f:
            custom_paths = f.read().splitlines()
        paths_to_scan.update(custom_paths)

    while paths_to_scan:
        path = paths_to_scan.pop()
        if not path:
            continue

        if path in discovered_directories:
            continue

        # Properly encode the path
        encoded_path = quote(path, safe='/:?=&')

        # Ensure that the URL has a valid schema
        if not urlparse(encoded_path).scheme:
            encoded_path = "http://" + encoded_path  # Assuming HTTP, modify if needed

        try:
            response = requests.get(encoded_path)
            if response.status_code == 200:
                success_messages.append([encoded_path])
                discovered_directories.add(encoded_path)

                if recursive:
                    internal_links = get_internal_links(encoded_path, response.text)
                    for link in internal_links:
                        paths_to_scan.add(link)

            elif response.status_code == 404:
                errors.append([encoded_path, "Not Found"])
            else:
                errors.append([encoded_path, f"HTTP {response.status_code}"])

        except requests.RequestException as e:
            errors.append([encoded_path, str(e)])

    print(logo)
    print(author)
    print("\n")
    print(tabulate(errors, headers=["Errors", "Description"], tablefmt="grid"))
    print("\n")
    print(tabulate(discovered_directories, headers=["Directories"], tablefmt="grid"))
    print("\n")
    print(tabulate(success_messages, headers=["Success Messages"], tablefmt="grid"))

def main():
    parser = argparse.ArgumentParser(description="Simple directory scanner")
    parser.add_argument("-u", "--url", help="Target URL", required=True)
    parser.add_argument("-r", "--recursive", help="Enable recursive directory scanning", action="store_true")
    parser.add_argument("-w", "--wordlist", help="Path to custom wordlist")
    args = parser.parse_args()

    target_url = args.url.strip()
    recursive = args.recursive
    wordlist = args.wordlist

    find(target_url, recursive, wordlist)

if __name__ == "__main__":
    main()
