# ITRX.io Client

A client for interacting with the [ITRX.io API](https://itrx.io/)

## Prerequisites

Get an API Key: https://itrx.io/en/buyer/api 

```shell
export ITRX_API_KEY=your-api-key
export ITRX_API_SECRET=your-api-secret
```

## Installation

To install the package, use pip:

```sh
pip install git+https://github.com/Romamo/itrx.git
```

## Usage

```python
from itrx import Client

client = Client()
# Get last USDT transactions
price = client.get_price(64000)
response = client.create_order('receiving address')
print(response)
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
```
