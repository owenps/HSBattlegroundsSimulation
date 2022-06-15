import requests
from alive_progress import alive_bar
from bs4 import BeautifulSoup
import json
from os import path

DATA_PATH = "../data"
WIKI_DOWNLOAD_PATH = DATA_PATH+"/wiki.html"
OUTPUT_PATH = DATA_PATH+"/minions.json"

WIKI_BASE_URL = "https://hearthstone.fandom.com"
WIKI_MINION_POOL_DIR = WIKI_BASE_URL+"/wiki/Battlegrounds/Minion_by_pool"

MINION_ATTRS = ["name","miniontype","taverntier","attack","health","description"]


def fetch_wiki(download:bool):
    print(f"Loading: \t{WIKI_MINION_POOL_DIR}")
    if not download:
        with open(WIKI_DOWNLOAD_PATH, "rb") as f:
            return f.read()

    page = requests.get(WIKI_MINION_POOL_DIR)
    with open(WIKI_DOWNLOAD_PATH, "wb") as f:
        f.write(page.content)
    print(f"Updated \t{WIKI_DOWNLOAD_PATH} complete")
    
    return page.content

def clean_header(s:str):
    s = s.strip() # remove whitespace
    if "/" in s:
        s = s.split("/")[1]
    return s

def empty_minion(name=None):
    temp = { a : None for a in MINION_ATTRS}
    if name: temp["name"] = name
    return temp


def main():
    # if file exists, don't download
    content = fetch_wiki(download=not path.exists(WIKI_DOWNLOAD_PATH))
    # parse webpage with bs4
    soup = BeautifulSoup(content, "html.parser")
    cards = soup.find_all("div", class_="card-image")

    minions = []
    #error_minions = []
    with alive_bar(len(cards)) as bar:
        for card in cards:
            # for each card visit its personal wiki and extract data
            minion_dir = card.find("a").attrs["href"]
            minion_page = requests.get(WIKI_BASE_URL+minion_dir)
    
            little_soup = BeautifulSoup(minion_page.content, "html.parser")
            minion_name = clean_header(little_soup.find(id="firstHeading").text)

            try:
                minion_div = little_soup.find_all("div", class_="stdinfobox")
                minion_body = minion_div[0].find("div",class_="body")
            
                # get minion details
                minion = empty_minion(minion_name)

                # read table headers
                minion_attrs = minion_body.find_all("th")
                for attr in minion_attrs:
                    # check if rows are worth extracting
                    attr_name = ''.join(ch for ch in attr.text if ch.isalnum()).lower()
                    if attr_name not in minion:
                        continue 
                    
                    minion[attr_name] = attr.nextSibling.text
                    
                minions.append(minion)
            except IndexError as e:
                minions.append(empty_minion(minion_name))
            finally:
                bar()

    with open(OUTPUT_PATH,"w") as out:
        json.dump(minions, out)
        print(f"Downloaded to \t{OUTPUT_PATH} complete")

if __name__ == "__main__":
    main()