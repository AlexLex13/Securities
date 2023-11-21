import json
import tempfile
from io import StringIO, BytesIO

import dramatiq
import pandas as pd
from django.template.loader import render_to_string
from weasyprint import HTML

from userpreferences.utils import create_df

@dramatiq.actor
def create_json(response, user_preference):
    bonds_df, shares_df = create_df(user_preference)

    with StringIO() as io:
        res = {}

        bonds_df.to_json(io, orient='records', date_format='iso', force_ascii=False, default_handler=str)
        res.update({"Bonds": json.loads(io.getvalue().strip())})
        io.truncate(0)
        io.seek(0)
        shares_df.to_json(io, orient='records', date_format='iso', force_ascii=False, default_handler=str)
        res.update({"Shares": json.loads(io.getvalue().strip())})
        io.truncate(0)
        io.seek(0)

        json.dump(res, io, indent=4, ensure_ascii=False)

        response.write(io.getvalue())


@dramatiq.actor
def create_pdf(response, user_preference):
    bonds = user_preference.bonds.all().select_related('company')
    shares = user_preference.shares.all().select_related('company')

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
    bonds_df, shares_df = create_df(user_preference)

    with BytesIO() as b:
        writer = pd.ExcelWriter(b, engine='xlsxwriter')
        bonds_df.to_excel(writer, sheet_name='Bonds')
        shares_df.to_excel(writer, sheet_name='Shares')
        writer.close()
        response.write(b.getvalue())
