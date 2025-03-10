import os
import sys
from datetime import datetime

import requests
from bs4 import BeautifulSoup

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.database.db_connection import SessionLocal
from app.entities.news import News as NewsEntity


def get_news(pages: int = 10):
    print('-----Crawler Start-----')

    url_base = 'https://tw-nba.udn.com/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0)\
            Gecko/20100101 Firefox/61.0'
    }

    def get_news_url_list(pages: int) -> list:
        """Gets all news URLs"""

        url_news = '/nba/news'
        r = requests.get(url=url_base + url_news, headers=headers)

        links = []
        while pages > 0:
            soup = BeautifulSoup(r.text, 'html.parser')
            news_list_body = soup.find(id='news_list_body')

            # Extract all links from the news list body
            for link in news_list_body.find_all('a', href=True):
                links.append(link['href'])

            # Find the link for the next page
            next_page_link = soup.find('gonext')
            if next_page_link and next_page_link.find('a', attrs={'data-id': 'right'}):
                next_page_url = next_page_link.find('a', attrs={'data-id': 'right'})['href']
                r = requests.get(url=next_page_url, headers=headers)
            else:
                break  # If there's no next page, stop

            pages -= 1  # Decrement the page counter

        return links

    news_url_list = get_news_url_list(pages)

    news_list = []
    for news_url in news_url_list:
        news_id = news_url.split('/')[-1]

        try:
            r = requests.get(url=news_url, headers=headers)
            soup = BeautifulSoup(r.text, 'html.parser')

            story_body_content = soup.find(id='story_body_content')

            news_title = story_body_content.find('h1', class_='story_art_title').text.strip()
            news_date = (
                story_body_content.find('div', class_='shareBar__info--author')
                .find('span')
                .text.strip()
            )
            news_content = ''
            p_tags = story_body_content.select('span > p')
            for p_tag in p_tags:
                news_content += p_tag.text.strip()

            news_entity = NewsEntity(
                id=news_id,
                title=news_title,
                link=news_url,
                content=news_content,
                published_at=datetime.strptime(news_date, '%Y-%m-%d %H:%M'),
            )

            news_list.append(news_entity)

            print(f'{news_id} {news_title} {news_date} ok.')
        except Exception as e:
            print(e)
            continue

    save_news_to_db(news_list)
    print('save completed.')
    print('-----Crawler End-----')


def save_news_to_db(news_list: list[NewsEntity]):
    session = SessionLocal()
    for news_entity in news_list:
        existing_news = (
            session.query(NewsEntity).filter(NewsEntity.link == news_entity.link).first()
        )

        if existing_news is None:
            session.add(news_entity)

    session.commit()
    session.close()


if __name__ == '__main__':
    get_news()
