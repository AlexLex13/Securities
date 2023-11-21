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


def parse_bonds_df(df):
    bonds = []
    for lst in df.values:
        field_list = lst[1:-1]
        for i, f in enumerate(field_list):
           if i in (6, 7, 9, 11):
               field_list[i] = float(f.strip('$'))
           if i in range(12, 16):
               field_list[i] = f.date()

        bonds.append(field_list)

    return bonds
