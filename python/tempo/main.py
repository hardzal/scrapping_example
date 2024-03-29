from bs4 import BeautifulSoup
import requests

import pandas as pd
from requests.api import post

bulan = [1,2,3,4,5,6]
tanggal = [32,29,32,31,32,31]
link = 'https://www.tempo.co/indeks'

data_set = {"post_title": [], "post_thumbnail_url": [], "post_summary": [], "post_date": [], "post_url": [], "post_image_url": [], "post_image_caption": [], "post_content": [], "post_tags": []}
# data_set = {"post_title": [], "post_thumbnail_url": [], "post_summary": [], "post_date": [], "post_url": []}

def search_posts(posts):
    for post in posts:
        post_url = post.find('a', class_='col')
        post_title = post.find('h2', class_='title')
        post_thumbnail_url = post.find('img')
        post_summary = post.find('p')
        post_date = post.find('span', class_='col')
        
        data_set['post_title'].append(post_title.text)
        data_set['post_thumbnail_url'].append(post_thumbnail_url['src'])
        data_set['post_summary'].append(post_summary)
        data_set['post_url'].append(post_url['href'])
        data_set['post_date'].append(post_date.text)

        access_post = requests.get(post_url['href'])
        post_detail_html = BeautifulSoup(access_post.content, 'lxml')
        post_detail = post_detail_html.find('article')
        post_image = post_detail.find('img')
        post_image_caption = post_detail.find('figcaption')
        post_content = post_detail.find('div', id='isi')
        post_tags_list = post_detail.find('div', class_='tags')
        post_tag = post_tags_list.find_all('a')

        data_set['post_image_url'].append(post_image['src'])
        data_set['post_image_caption'].append(post_image_caption)
        data_set['post_content'].append(post_content)
        data_set['post_tags'].append(','.join(str(item.text) for item in post_tag))
    
if __name__ == '__main__':
    count = 1
    for bln in bulan:
        for tgl in range(1, tanggal[bulan.index(bln)]):
            html_result = [] 
            if(tgl < 10):
                html_result = requests.get(f"{link}/2021/0{bln}/0{tgl}")
                print(f"{link}/2021/0{bln}/0{tgl}")
            else:
                html_result = requests.get(f"{link}/2021/0{bln}/{tgl}")
                print(f"{link}/2021/0{bln}/{tgl}")
            result = BeautifulSoup(html_result.content, 'lxml')
            post_wrapper = result.find('ul', class_='wrapper')
            posts = post_wrapper.find_all('div', class_='card card-type-1')

            search_posts(posts)
         
            count = count + 1
        if count == 3: break

    df = pd.DataFrame(data_set, columns=['post_title', 'post_thumbnail_url', 'post_summary', 'post_date', 'post_url', 'post_image_url', 'post_image_caption', 'post_content', 'post_tags'])
    # df = pd.DataFrame(data_set, columns=['post_title', 'post_thumbnail_url', 'post_summary', 'post_date', 'post_url'])
    df.to_csv(r'D:\Code\scrapping-example\python\tempo\dataset\result.csv', index = False, header=True)

    print(df)
    print(f"saved!{len(df)}")