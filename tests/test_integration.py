from mercado_bitcoin.apis import DaySummaryApi
import datetime


class TestDaySummaryApi:

    def test_get_data(self):
        actual = DaySummaryApi(coin='BTC').get_data(date=datetime.date(2023,1,1)).get('date')
        expected = '2023-01-01' # Tests if api returns dict with date == date requested
        assert actual == expected