from .providers.http import HTTPProvider


class Client:
    def __init__(self, provider: HTTPProvider = None):
        if provider is None:
            self._provider = HTTPProvider()
        elif isinstance(provider, (HTTPProvider,)):
            self._provider = provider
        else:
            raise TypeError("provider is not a HTTPProvider")

    def get_price(self, energy_amount: int, period: str = '1H') -> dict:
        # if energy_amount > 32000:
        #     energy_amount = 65000
        # else:
        #     energy_amount = 32000
        # https://develop.itrx.io/api/order-price.html
        response = self._provider.make_request(
            'frontend/order/price',
            get={'energy_amount': energy_amount, 'period': period}
        )
        return (response['total_price'] + response['addition']) / 10 ** 6

    def create_order(self, receive_address, energy_amount: int = 32000, period: str = '1H') -> dict:
        # https://develop.itrx.io/api/order-create.html
        response = self._provider.make_request(
            'frontend/order',
            json={
               'energy_amount': energy_amount,
               'period': period,
               'receive_address': receive_address,
               # 'callback_url': 'http://{mydomain}/callback',
               # 'out_trade_no': '123456',
            },
            sign=True
        )
        return response['serial']
