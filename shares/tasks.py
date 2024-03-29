import datetime

import dramatiq
import requests
from bs4 import BeautifulSoup


@dramatiq.actor
def fetch_shares():
    url = 'https://smart-lab.ru/q/shares/'
    headers = {'Content-Type': 'text/html'}
    response = requests.get(url, headers=headers)

    shares = []

    bs = BeautifulSoup(response.text, 'lxml')

    for i in (*list(range(2, 17)), *list(range(18, 42))):
        share_fields = []
        for j in (1, 2, *list(range(6, 12)), 13, 15, 16):
            share_fields.append(bs.find('tbody').find_all('tr')[i].find_all('td')[j].text.strip())
        share_fields.append(' '.join(bs.find('tbody').find_all('tr')[i].find_all('td')[1].find('a').get('title')
                                     .split()[2:]))
        share_fields.append("https://smart-lab.ru/" + bs.find('tbody').find_all('tr')[i].find_all('td')[4]
                            .find('a').get('href'))

        shares.append(share_fields)

    return shares


@dramatiq.actor
def processing_shares(fields):
    fields_list = [field.strip("[]'%").replace(' ', '') for field in fields.split(", ")]
    for i, field in enumerate(fields_list):
        if field == '-' or field == '':
            fields_list[i] = None
        elif i in (2, 3, 4, 6, 7, 8, 9, 10):
            fields_list[i] = float(field)
        elif i == 5:
            time_attr = [int(i) for i in field.split(":")]
            fields_list[i] = datetime.time(*time_attr)

    return fields_list
