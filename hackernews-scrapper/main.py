from bs4 import BeautifulSoup
import requests
import validators

html_text = requests.get('https://news.ycombinator.com/')
result = BeautifulSoup(html_text.content, 'lxml')
news_table = result.find('table', class_='itemlist')
newses = news_table.find_all('tr', class_ = 'athing')
news_meta = news_table.find_all('tr')[1::2]

for (index,news) in enumerate(newses):
    news_head = news.find_all('td', class_='title')
    title = news_head[1].a.text
    link = news_head[1].a['href']
    link = link if (validators.url(link)) else f'https://news.ycombinator.com/{link}'
    web_link = news_head[1].span.a.text if(news_head[1].span) else '-'
    
    increment = 3 if (index > 0) else 0

    timestamp = news_meta[increment].find_all('span', class_='age')[0].a.text
    author = news_meta[increment].find_all('a', class_='hnuser')[0].text if(news_meta[increment].find_all('a', class_='hnuser')) else '-'
    point = news_meta[increment].find_all('span', class_='score')[0].text if(news_meta[increment].find_all('span', class_='score')) else '-'
    comment_count = news_meta[increment].find_all('a')[-1].text if(news_meta[increment].find_all('a')[-1]) else '-'

    print(f"{index+1}. News Title: {title}\n")
    print(f"\tPosted at {timestamp}")
    print(f"\tAuthor: {author}")
    print(f"\tComments: {comment_count}")
    print(f"\tScore news: {point}")
    print(f"\tWeb source: {web_link}")
    print(f"\tSource: {link}")
    print("\n")
    
print("")