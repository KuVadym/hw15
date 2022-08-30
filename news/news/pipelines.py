# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from itemadapter import ItemAdapter
import sqlite3
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import literal
from .spiders.model import Base, News, NewsList
import requests
from bs4 import BeautifulSoup
import lxml.html

class NewsPipeline:
    def __init__(self):
        self.create_conn()
  
    # create connection method to create database
    # or use database to store scraped data
    def create_conn(self):

        self.engine = create_engine("sqlite:///my_news.db")
        Base.metadata.create_all(self.engine)
        Base.metadata.bind = self.engine
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
   
    # store items to databases.
    def process_item(self, item, spider):
        self.putitemsintable(item)
        return item
  
    def putitemsintable(self, item):
        check = self.session.query(NewsList).filter(NewsList.link == item.get('link')[0]+item.get('link')[1][1:])
        if self.session.query(literal(True)).filter(check.exists()).scalar() == True:
            pass
        else:
            news = None
            link = item.get('link')[0]+item.get('link')[1][1:]
            newslist = NewsList(title=item.get('news'), link=link)
            # print(f'{item.get("link")[0]}' == 'https://zakarpattya.net.ua/')
            if item.get('link')[0] == 'https://zakarpattya.net.ua/':
                response = requests.get(link)
                soup = BeautifulSoup(response.text, "lxml")
                subtitles = soup.find('div', {'class':'pc1'}).find_all('h2')
                subs =[]
                for subtitle in subtitles:
                    subs.append(subtitle.get_text(strip=True))
                text = soup.find(id='pubText').find_all('p')
                news_text = []
                for p in text:
                    if p.get_text(strip=True):  
                        news_text.append(p.get_text(strip=True))
                news = News(subtitle=' '.join(subs), text=' '.join(news_text[:-1]), newslist=newslist)
            elif item.get('link')[0] == 'https://uzhgorod.net.ua/':
                response = requests.get(link)
                soup = BeautifulSoup(response.text, "lxml")
                subtitle = soup.find('div', {'class':'column9 rightside'}).find('b').get_text(strip=True)
                text = soup.find('div', {'class':'column9 rightside'}).find_all('p')
                news_text = []
                for p in text:
                    if p.get_text(strip=True):  
                        news_text.append(p.get_text(strip=True))
                news = News(subtitle=subtitle, text=' '.join(news_text), newslist=newslist)
            self.session.add(newslist)
            self.session.commit()
            self.session.close()

