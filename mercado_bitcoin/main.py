
import datetime
import time
from schedule import repeat, every, run_pending
from mercado_bitcoin.writers import DataWriter
from mercado_bitcoin.ingestors import DaySummaryIngestor

if __name__ == '__main__':
    day_summary_ingestor = DaySummaryIngestor(
        coins=['BTC', 'ETH', 'LTC'], 
        default_start_date=datetime.date(2023, 1, 1), 
        writer=DataWriter
        )

    @repeat(every(1).seconds)
    def job():
        day_summary_ingestor.ingest()

    while True:
        run_pending()
        time.sleep(0.5)
