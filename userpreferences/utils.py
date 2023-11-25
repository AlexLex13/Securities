from datetime import datetime

import pandas as pd

from bonds.models import Bond
from shares.models import Share


def create_df(preference):
    bonds = preference.bonds.all().select_related('company')
    shares = preference.shares.all().select_related('company')

    bonds_table = {}
    for i, key in enumerate(Bond.FIELDS):
        bonds_table[key] = [bond.get_fields()[i] for bond in bonds]

    bonds_df = pd.DataFrame(bonds_table)

    shares_table = {}
    for i, key in enumerate(Share.FIELDS):
        shares_table[key] = [share.get_fields()[i] for share in shares]

    shares_df = pd.DataFrame(shares_table)

    return bonds_df, shares_df


def parse_bonds_json(lst):
    bonds = []
    for dct in lst:
        for k, v in dct.items():
            if dct[k]:
                if k in ('volume', 'coupon_value', 'price', 'accumulated_income'):
                   dct[k] = float(v.strip('$').replace(',', ''))
                if k in ('next_coupon_date', 'issue_date', 'maturity_date', 'offer_date'):
                   dct[k] = datetime.strptime(v[:10], '%Y-%m-%d').date()

        bonds.append(dct)
    return bonds


def parse_shares_json(lst):
    shares = []
    for dct in lst:
        for k, v in dct.items():
            if dct[k]:
                if k in ('last_price', 'volume', 'capitalization'):
                    dct[k] = float(v.strip('$').replace(',', ''))
                if k == 'last_transaction_time':
                    datetime.strptime(v, '%H:%M:%S').time()

        shares.append(dct)
    return shares
