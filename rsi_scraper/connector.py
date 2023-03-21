"""
A module to perform requests
"""

import os
import requests
from urllib.parse import urljoin


class Connector:

    url_host = 'https://robertsspaceindustries.com'
    __user_agent = f"""StarCitizen REST API/{
        os.getenv('VERSION') or 'DEVELOPMENT'
    } (starcitizen-api.com)"""

    async def request_async(
        self, url: str, json_data: dict = None,
        headers: dict = {}, method: str = "post"
    ):
        """An asynchronous request.

        Args:
            url (str): The URL.
            json_data (dict, optional): The data to send. Default to None.
            headers (dict, optional): Headers parameters. Default to {}.
            method (str, optional): Use the "get" or "post". Default to "post".

        Returns:
            requests.Response: The Response object
        """
        return self.request(url, json_data, headers, method)

    def request(
        self, url: str, json_data: dict = None,
        headers: dict = {}, method: str = "post"
    ):
        """Send a request to the specified url using parameters

        Args:
            url (str): The URL.
            json_data (dict, optional): The data to send. Default to None.
            headers (dict, optional): Headers parameters. Default to {}.
            method (str, optional): Use the "get" or "post". Default to "post".

        Returns:
            requests.Response: The Response object
        """
        headers['Accept-Language'] = 'en-US,en;q=0.5'
        headers['User-Agent'] = self.__user_agent
        headers['Cache-Control'] = "no-cache"
        headers['Cookie'] = "Rsi-Token="

        args = {
            "url": url,
            "headers": headers,
            "stream": False
        }

        if json_data is not None:
            args["json"] = json_data

        proxies = {}
        if os.getenv('HTTP_PROXY'):
            proxies = {'http': os.environ['HTTP_PROXY']}

        req = None
        if method == "post":
            req = requests.post(proxies=proxies, timeout=5, **args)
        elif method == "get":
            req = requests.get(proxies=proxies, timeout=5, **args)
        else:
            return None

        return req

    @classmethod
    def convert_path(cls, path: str):
        return urljoin(cls.url_host, path)
