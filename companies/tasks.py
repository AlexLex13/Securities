import dramatiq
import requests
from bs4 import BeautifulSoup


@dramatiq.actor
def fetch_brokers():
    url = 'https://smart-lab.ru/q/shares/'
    headers = {'Content-Type': 'text/html'}
    response = requests.get(url, headers=headers)

    brokers = []

    bs = BeautifulSoup(response.text, 'lxml')

    for i in range(43, 73):
        broker_fields = []
        for j in (1, 2, *list(range(6, 12)), 13, 15, 16):
            broker_fields.append(bs.find('tbody').find_all('tr')[i].find_all('td')[j].text.strip())
        brokers.append(broker_fields)

    return brokers
