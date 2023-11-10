import csv
import tempfile

import dramatiq
import xlsxwriter
from django.template.loader import render_to_string
from weasyprint import HTML

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
    workbook = xlsxwriter.Workbook()
    bold = workbook.add_format({'bold': True})

    worksheet = workbook.add_worksheet('Bonds')

    row_num = 0
    for col_num in range(len(BONDS_COLUMNS)):
        worksheet.write(row_num, col_num, BONDS_COLUMNS[col_num], bold)

    rows = user_preference.bonds.all()

    for row in rows:
        row_num += 1

        for col_num in range(len(row)):
            worksheet.write(row_num, col_num, str(row[col_num]))

    worksheet = workbook.add_worksheet('Shares')

    row_num = 0
    for col_num in range(len(SHARES_COLUMNS)):
        worksheet.write(row_num, col_num, SHARES_COLUMNS[col_num], bold)

    rows = user_preference.shares.all()

    for row in rows:
        row_num += 1

        for col_num in range(len(row)):
            worksheet.write(row_num, col_num, str(row[col_num]))

    workbook.close()
    response.write(workbook)
