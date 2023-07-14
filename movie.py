from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd

options = webdriver.ChromeOptions()
options.add_argument(
    'user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"'
)

def get_one_item(element):
    item = {}
    infomations = [i for i in element.children if i!='\n']
    item["title"] = infomations[0]["title"]
    for line in infomations[1:]:
        k, v = line.text.split(':\n')
        item[k.strip('\n')] = v.strip('\n').strip(' ').strip('\n')
    return item


def get_information(html: str):
    soup = BeautifulSoup(html, 'html.parser')
    elements = soup.find_all(attrs={'class':'movie-hover-info'})
    data = []
    for ele in elements:
        data.append(get_one_item(ele))
    return data

def write_file(items):
    global row_id
    datas = []
    for item in items:
        datas.append(item.values())
    file = pd.DataFrame(datas)
    file.to_excel('movie.xlsx', startrow=row_id)
    row_id += len(items)


web = webdriver.Chrome()
base_url = 'https://www.maoyan.com/films?showType=3'
for year in range(15, 23):
    for page in range(0, 2001, 30):
        url = base_url + f'&yearId={year-5}&offset={page}'
        web.get(url)
        html = web.page_source
        while '验证' in html:
            html = web.page_source
        one_page_infomation = get_information(html)
        write_file(one_page_infomation)
    input()
    