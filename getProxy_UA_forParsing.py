import requests, random
from random import choice
from bs4 import BeautifulSoup


def get_proxy():

    url = 'https://free-proxy-list.net/'
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'lxml')
    trs = soup.find('table', {'class': 'table table-striped table-bordered'}).find_all('tr')[1:]
    for i in range(999):
        random_td = random.choice(trs)
        if 'yes' in random_td.find_all('td')[6].text.strip(): # if we need https proxy
            # - 'yes'. if 'no' - we will get 'http'
            raw_proxy = random_td.find_all('td')
            break
        else:
            continue
    proxy = raw_proxy[0].text.strip() + ':' + raw_proxy[1].text.strip()  # + raw_proxy[6].text.strip()
    return {'http': f'https://{proxy}'}


def get_user_agent():
    with open('user-agents.txt', 'r') as file:
        random_ua = choice(file.readlines())
        return {'user-agent': f'{random_ua}'}


print(get_user_agent(), '\n', get_proxy())
