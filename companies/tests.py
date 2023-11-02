import pytest
from djmoney.money import Money

from .models import Company


@pytest.mark.django_db
def test_create_company():
    company = Company.objects.create(
        name='Alfa',
        country='Russia',
        industry='Finance',
        share_capital=Money(1000000, 'USD')
    )

    assert company.name == 'Alfa'
