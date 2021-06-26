import os

import pytest
import warnings

from rsi_scraper import Connector
import requests

url = 'http://icanhazip.com'


@pytest.mark.connector
def test_request():
    conn = Connector()
    req = conn.request(url)
    assert req.status_code == 200


@pytest.mark.connector
async def test_request_async():
    conn = Connector()
    req = await conn.request_async(url)
    assert req.status_code == 200


@pytest.mark.connector
def test_proxy():

    req = requests.get(url, proxies={})
    ip_public = req.text.strip()
    assert req.status_code == 200

    conn = Connector()
    req = conn.request(url)
    ip_proxy = req.text.strip()
    assert req.status_code == 200

    if os.getenv('HTTP_PROXY'):
        if ip_public == ip_proxy:
            pytest.exit('Bad proxy configuration', 1)
    else:
        warnings.warn(UserWarning('Executing without proxy'))


@pytest.mark.connector
async def test_request_rsi():
    conn = Connector()
    req = await conn.request_async(conn.url_host)
    assert req.status_code == 200
