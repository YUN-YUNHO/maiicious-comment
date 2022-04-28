from bs4 import BeautifulSoup as bs
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import ElementNotInteractableException
import time
import random


def parse_news_url(markup, parser):
    urls = []
    soup = bs(markup, parser)
    ranking_news_list = soup.find_all('div', {'class': 'list_content'})
    for news in ranking_news_list:
        href = str(news.find('a')['href'])
        comment_url = href.replace('article', 'article/comment')
        urls.append(comment_url)

    return urls


def parse_comments(driver):
    more_count = 0
    while more_count < 10:    # 더보기 버튼 최대 10번 클릭 제한
        try:
            more_comments = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "a.u_cbox_btn_more")))
            more_comments.send_keys(Keys.ENTER)
            time.sleep(random.randint(1, 3))
            more_count += 1
        except ElementNotInteractableException:
            break

    html = driver.page_source
    soup = bs(html, 'html.parser')

    try:
        comment_contents = soup.findAll('span', {'class': 'u_cbox_contents'})
        comments = [comment.text.replace('\n', ' ').strip() for comment in comment_contents]
        title = soup.find('div', {'class': 'media_end_head_title'}).text.strip()
        titles = [title] * len(comments)
    except TimeoutError:
        return parse_comments(driver)

    return zip(titles, comments)
