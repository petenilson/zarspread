"""
 bitfinex XBT price in USD
    https://api.bitfinex.com/v2/ticker/tBTCUSD

response:
    [
        4567.8,
        16.7770791,
        4567.8,
        12.74414776,
        -232.2,
        -0.0484,
        4567.8,
        46374.6575428,
        4970,
        4530
]

luno XBT price in ZAR
    https://api.mybitx.com/api/1/ticker?pair=XBTZAR

response:
    {
        "timestamp":1504361873104,
        "bid":"66562.00",
        "ask":"66591.00",
        "last_trade":"66562.00",
        "rolling_24_hour_volume":"598.905659",
        "pair":"XBTZAR"
}

fixer.io USD price in ZAR
    http://api.fixer.io/latest?symbols=USD,ZAR

response:
    {
        "base":"EUR",
        "date":"2017-09-01",
        "rates":
            {
                "USD":1.192,
                "ZAR":15.418
        }
}
"""
import requests
import logging
from models import Tick

log = logging.getLogger('ApiCalls')
timeouts = (3, 3)  # connect, read

USD_ZAR_URL = 'http://api.fixer.io/latest?symbols=USD,ZAR'
XBT_ZAR_URL = 'https://api.mybitx.com/api/1/ticker?pair=XBTZAR'
XBT_USD_URL = 'https://api.bitfinex.com/v2/ticker/tBTCUSD'


def get_data(url, timeout=(0.3, 0.3)):
    """
        Returns the json response of the request while handling
        timeouts in the case of the server hanging. Returns
        -1 if the request timeout.
    """
    try:
        r = requests.get(url, timeout=timeout)
    except requests.exceptions.ConnectTimeout:
        return -1
        log.error('timeout for url: {}'.format(url))
    else:
        return r.json()


def get_usd_zar(data):
    zar_price = data['rates']['zar']
    return zar_price


def get_xbt_zar(data):
    zar_price = data['ask']
    return zar_price


def get_xbt_usd(data):
    usd_price = data[0]
    return usd_price


def insert_prices(usd_zar, xbt_zar, xbt_usd):
    Tick.objects.create(
        XBTZAR=xbt_zar,
        XBTUSD=xbt_usd,
        USDZAR=usd_zar,
    )


def update_prices():

    usd_zar_data = get_data(USD_ZAR_URL)
    usd_zar_price = get_usd_zar(usd_zar_data)
    log.debug('usd_zar_price: {}'.format(usd_zar_price))

    xbt_zar_data = get_data(XBT_ZAR_URL)
    xbt_zar_price = get_xbt_zar(xbt_zar_data)
    log.debug('xbt_zar_price: {}'.format(xbt_zar_price))

    xbt_usd_data = get_data(XBT_USD_URL)
    xbt_usd_price = get_xbt_usd(xbt_usd_data)
    log.debug('xbt_zar_price: {}'.format(xbt_usd_price))

    insert_prices(usd_zar_price, xbt_zar_price, xbt_usd_price)
