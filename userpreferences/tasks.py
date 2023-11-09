import csv
import tempfile

import dramatiq
from django.template.loader import render_to_string
from weasyprint import HTML


@dramatiq.actor
def create_csv(response, user_preference):
    writer = csv.writer(response)

    writer.writerow(['name', 'maturity_years', 'profitability', 'coupon_yield',
                     'coupon_yield_last', 'rating', 'volume', 'coupon_value',
                     'coupon_payments_frequency', 'accumulated_income', 'duration',
                     'price', 'next_coupon_date', 'issue_date', 'maturity_date',
                     'offer_date', 'company'])

    bonds = user_preference.bonds.all()

    writer.writerow(['Bonds'])
    for bond in bonds:
        writer.writerow([bond.name, bond.maturity_years, bond.profitability, bond.coupon_yield,
                         bond.coupon_yield_last, bond.rating, bond.volume, bond.coupon_value,
                         bond.coupon_payments_frequency, bond.accumulated_income, bond.duration,
                         bond.price, bond.next_coupon_date, bond.issue_date,
                         bond.maturity_date, bond.offer_date, bond.company.name])

    writer.writerow([])

    writer.writerow(['name', 'ticker', 'last_price', 'price_change', 'volume',
                     'last_transaction_time', 'weekly_price_change', 'monthly_price_change',
                     'annual_price_change', 'capitalization', 'volume_change', 'company'])

    shares = user_preference.shares.all()

    writer.writerow(['Shares'])
    for share in shares:
        writer.writerow([share.name, share.ticker, share.last_price, share.price_change,
                         share.volume, share.last_transaction_time, share.weekly_price_change,
                         share.monthly_price_change, share.annual_price_change,
                         share.capitalization, share.volume_change, share.company.name])


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
