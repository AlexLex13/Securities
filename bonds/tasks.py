import datetime

import dramatiq
import requests
from bs4 import BeautifulSoup


@dramatiq.actor
def fetch_bonds():
    url = 'https://smart-lab.ru/q/bonds/'
    headers = {'Content-Type': 'text/html'}

    response = requests.get(url, headers=headers)
    bs = BeautifulSoup(response.text, 'lxml')

    bonds = []
    for i in range(1, 42):
        company_title = bs.find('tbody').find_all('tr')[i].find_all('td')[2].find('a')
        bond_fields = []

        if company_title:

            for j in (1, *list(range(3, 18))):
                bond_fields.append(bs.find('tbody').find_all('tr')[i].find_all('td')[j].text.strip())

            bond_fields.append(' '.join(company_title.get('title').split()[2:]))

        else:
            continue

        bonds.append(bond_fields)

    return bonds


@dramatiq.actor
def processing_bonds(fields):
    fields_list = [field.strip("[]'%") for field in fields.split(", ")]
    for i, field in enumerate(fields_list):
        if field == '-':
            fields_list[i] = None
        elif i in (1, 2, 3, 4, 6, 7, 8, 9, 10, 11):
            fields_list[i] = float(field)
        elif i in range(12, 16):
            date_attr = list(reversed([int(i) for i in field.split(".")]))
            date_attr[0] += 2000
            fields_list[i] = datetime.date(*date_attr)

    return fields_list
