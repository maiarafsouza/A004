import requests
import datetime
import ratelimit
import logging
from backoff import on_exception, expo
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__) # __name__ attribute will be main if this file is executed or name of this file if this script is called from another file
logging.basicConfig(level=logging.INFO)

class MercadoBitcoinApi(ABC): # ABC - abstract base class
    BASE_ENDPOINT = 'https://www.mercadobitcoin.net/api/'

    def __init__(self, coin: str) -> None:
        self.coin = coin
    
    @abstractmethod # Abstract methods have to be implemented by child classes
    def _get_endpoint(self, **kwargs) -> str:
        pass
    
    @on_exception(expo, ratelimit.exception.RateLimitException, max_tries=10)
    @ratelimit.limits(calls=29, period=30)
    @on_exception(expo, requests.exceptions.HTTPError, max_tries=10)
    def get_data(self, **kwargs) -> dict:
        endpoint = self._get_endpoint(**kwargs)
        logger.info(f'Getting data from endpoint {endpoint}')
        response = requests.get(endpoint)
        response.raise_for_status() # Raises exception if status attribute indicates error
        return response.json()
    


class DaySummaryApi(MercadoBitcoinApi):
    type = 'day-summary'

    def _get_endpoint(self, date: datetime.date) -> str:
        endpoint = f'{MercadoBitcoinApi.BASE_ENDPOINT}{self.coin}/{self.type}/{date.year}/{date.month}/{date.day}'
        return endpoint        


class TradesApi(MercadoBitcoinApi):
    type = 'trades'

    def _get_unix_epoch(self, date: datetime.datetime) -> int:
        return int(date.timestamp())

    def _get_endpoint(self, date_from: datetime.datetime = None, date_to: datetime.datetime = None) -> str:
        
        if date_from and not date_to:
            unix_date_from = self._get_unix_epoch(date_from)
            endpoint = f'{MercadoBitcoinApi.BASE_ENDPOINT}{self.coin}/{self.type}/{unix_date_from}'
        
        elif date_from and date_to:
            if date_from > date_to:
                raise RuntimeError('date_from cannot be grater than date_to')
            unix_date_from = self._get_unix_epoch(date_from)
            unix_date_to = self._get_unix_epoch(date_to)
            endpoint = f'{MercadoBitcoinApi.BASE_ENDPOINT}{self.coin}/{self.type}/{unix_date_from}/{unix_date_to}'
        
        else:
            endpoint = f'{MercadoBitcoinApi.BASE_ENDPOINT}{self.coin}/{self.type}/'
        
        return endpoint