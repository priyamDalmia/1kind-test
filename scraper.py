import re
from typing import Dict
from dataclasses import dataclass

import requests
from bs4 import BeautifulSoup as bs

# scraped "items" will be return in this format. 
ITEM_DICT = {
        "id": None,
        "topic": None,
        "title": None, 
        "subtitle": None,
        "article": None,
        "meta": [],
        }

@dataclass
class ScraperConfig:
    # TODO dataclass list 
    keywords = ["nft", "crypto", "blockchain", "bitcoin"]
    host_url: str = "https://www.bbc.co.uk/search?q=%s&page=%s"
    # site specific tags and parameters 
    item_class: str = "ssrcss-11rb3jo-Promo"
    title_class: str = "Headline"
    subtitle_class: str = "Paragraph"
    article_link_class: str = "PromoLink"
    article_class: str = "Para"
    metadata_class: str = "MetadataText"

    def __repr__(self):
        return f"Scraping articles on {self.keywords} from address {self.host_url[7:21]}"

class Scraper:
    def __init__(self, config: ScraperConfig = ScraperConfig(), url = None):
        self.config = config
        self.page_count = 0
        self.keywords = iter(self.config.keywords)
        self.topic = next(self.keywords)
        if not url:
            self._url = self.format_url()

        self.get_html_soup()

    def format_url(self):
        url = self.config.host_url % (\
                self.topic, self.page_count+1)
        try:
            requests.get(url)
        except Exception as e:
            print("Error: Invalid Host URL. Please provide a correct address.")
        return url

    def get_html_soup(self):
        # TODO get a timeout cluase here 
        webpage = requests.get(self._url)
        self.soup = bs(webpage.content, "html.parser")
        self.items = iter(self.soup.find_all(class_=self.config.item_class))

    def get_item(self) -> Dict:
        item_data = ITEM_DICT.copy()
        try:
            item = next(self.items)
        except Exception:
            if self.page_count > 20:
                self.topic = next(self.keywords)
                self.page_count = 0
            self.get_next_page()
            print(f"BBC Topic: {self.topic}, Search Page: {self.page_count}")
            return item_data

        # get current topic
        item_data["topic"] = self.topic

        # get title
        if a:= item.find(\
                class_=re.compile(self.config.title_class)):
            item_data["title"] = a.text

        # get subtitle
        if a:= item.find(\
                class_=re.compile(self.config.subtitle_class)):
            item_data["subtitle"] = a.text

        # get article link
        if a:= item.find(\
                class_=re.compile(self.config.article_link_class))['href']:
            try:
                # if id is not numerical - not a text article.
                item_data["id"] = re.findall(r'\b\d+\b', a)[0]
                item_data["article_link"] = a
                # get article
                item_data["article"] = self.get_item_article(link = a)
            except:
                return item_data

        # get metadata
        if a:= item.find(\
                class_=re.compile("MetadataText")):
            metadata = []
            for meta_item in a:
                metadata.append(meta_item.text)
            item_data["metadata"] = metadata

        return item_data 

    def get_item_article(self, link):
        article = ""
        article_page = requests.get(link)
        soup = bs(article_page.content, "html.parser")
        body = soup.find_all(class_=[
            re.compile("story-body"),
            re.compile("Article"),
            ])
        try:
            for i in body[0].find_all("p"):
                article = article + i.text
        except:
            return None
        return article

    def get_next_page(self):
        self.page_count+=1
        self._url = self.format_url()
        self.get_html_soup()
        pass

    def __repr__(self):
        return f"Scraping site BBC."

if __name__ == "__main__":
    # FOR DEBUGGING ONLY.
    scraper = Scraper()
    for i in range(11):
        item = scraper.get_item()
        print(f"{i}: {item['title']}")
