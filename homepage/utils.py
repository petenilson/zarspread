import requests
import logging
from homepage.models import Tick

log = logging.getLogger('ApiCalls')
timeout= (3, 3)  # connect, read

SITE_URL = 'https://checkthespread.herokuapp.com'

USD_ZAR_URL = 'http://api.fixer.io/latest?base=USD'
XBT_ZAR_URL = 'https://api.mybitx.com/api/1/ticker?pair=XBTZAR'
XBT_USD_URL = 'https://api.bitfinex.com/v2/ticker/tBTCUSD'

def wake_site(url=SITE_URL):
    r = requests.get(url)
    log.debug('wake site response: {}'.format(r.status_code))


def get_data(url, timeout=timeout):
    """
        Returns the json response of the request while handling
        timeouts in the case of the server hanging. Returns
        -1 if the request timeout.
    """
    try:
        r = requests.get(url, timeout=timeout)
    except requests.exceptions.ConnectTimeout as ConnectTimeout:
        log.error('timeout for url: {}'.format(url))
        raise ConnectTimeout
    else:
        return r.json()


def get_usd_zar(data):
    zar_price = data['rates']['ZAR']
    return float(zar_price)


def get_xbt_zar(data):
    zar_price = data['ask']
    return float(zar_price)


def get_xbt_usd(data):
    usd_price = data[0]
    return float(usd_price)


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
    log.debug('xbt_usd_price: {}'.format(xbt_usd_price))

    insert_prices(
        usd_zar=usd_zar_price,
        xbt_zar=xbt_zar_price,
        xbt_usd=xbt_usd_price
    )
