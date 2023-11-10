import csv
import tempfile
from io import BytesIO

import dramatiq
from django.template.loader import render_to_string
from weasyprint import HTML
import pandas as pd

BONDS_COLUMNS = [
    'name', 'maturity_years', 'profitability', 'coupon_yield',
    'coupon_yield_last', 'rating', 'volume', 'coupon_value',
    'coupon_payments_frequency', 'accumulated_income', 'duration',
    'price', 'next_coupon_date', 'issue_date', 'maturity_date',
    'offer_date', 'company'
]

SHARES_COLUMNS = [
    'name', 'ticker', 'last_price', 'price_change', 'volume',
    'last_transaction_time', 'weekly_price_change', 'monthly_price_change',
    'annual_price_change', 'capitalization', 'volume_change', 'company'
]


@dramatiq.actor
def create_csv(response, user_preference):
    writer = csv.writer(response)

    writer.writerow(BONDS_COLUMNS)

    bonds = user_preference.bonds.all()

    writer.writerow(['Bonds'])
    for bond in bonds:
        writer.writerow(bond.get_fields())

    writer.writerow([])

    writer.writerow(SHARES_COLUMNS)

    shares = user_preference.shares.all()

    writer.writerow(['Shares'])
    for share in shares:
        writer.writerow(share.get_fields())


@dramatiq.actor
def create_pdf(response, user_preference):
    bonds = user_preference.bonds.all()
    shares = user_preference.shares.all()

    html_string = render_to_string(
        'preferences/pdf-output.html', {'bonds': bonds, 'shares': shares})
    html = HTML(string=html_string)

    result = html.write_pdf()

    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output.seek(0)
        response.write(output.read())


@dramatiq.actor
def create_excel(response, user_preference):
    bonds = user_preference.bonds.all()
    shares = user_preference.shares.all()

    bonds_table = {}
    for i, key in enumerate(BONDS_COLUMNS):
        bonds_table[key] = [bond.get_fields()[i] for bond in bonds]

    bonds_df = pd.DataFrame(bonds_table)

    shares_table = {}
    for i, key in enumerate(SHARES_COLUMNS):
        shares_table[key] = [share.get_fields()[i] for share in shares]

    shares_df = pd.DataFrame(shares_table)

    with BytesIO() as b:
        writer = pd.ExcelWriter(b, engine='xlsxwriter')
        bonds_df.to_excel(writer, sheet_name='Bonds')
        shares_df.to_excel(writer, sheet_name='Shares')
        writer.close()
        response.write(b.getvalue())
