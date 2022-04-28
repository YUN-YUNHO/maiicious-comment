import pandas as pd
import requests
from selenium import webdriver
from tqdm import tqdm
from parser_naver_news import *
import chromedriver_autoinstaller


class NaverNewsCrawler:

    def __init__(self, markup='html', timeout=5):
        chromedriver_autoinstaller.install()
        self._session = requests.Session()
        self._markup = markup
        self._timeout = timeout
        self._rank_view_url = 'https://news.naver.com/main/ranking/popularMemo.naver'
        self._headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)\
            Chrome/98.0.4758.102 Safari/537.36'
        }
        self._options = webdriver.ChromeOptions().add_argument('headless')

    def get_ranking_news(self):
        """
        언론사별 댓글 많은 뉴스 기사의 댓글 웹 페이지 url의 리스트를 반환
        """
        r = self._session.get(self._rank_view_url, headers=self._headers, timeout=self._timeout)
        urls = parse_news_url(r.text, 'html.parser')
        return urls

    def get_comments(self, url):
        """
        :param url: 크롤링하려는 댓글 웹 페이지 url
        :return: 뉴스 기사의 제목과 댓글 최대 200개로 이루어진 데이터프레임
        """
        driver = webdriver.Chrome(options=self._options)
        driver.get(url)

        res = pd.DataFrame(data=parse_comments(driver),
                           columns=['Title', 'Comment'])

        return res


if __name__ == "__main__":
    result_df = pd.DataFrame(columns=[
        "Title",
        "Comment"
    ])

    nc = NaverNewsCrawler()
    news_list = nc.get_ranking_news()
    for news in tqdm(news_list):
        result_df = result_df.append(nc.get_comments(news))
        result_df.to_csv('./result.csv', encoding='cp949', index=False)
