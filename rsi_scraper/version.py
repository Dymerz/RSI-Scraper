"""Telemetry
"""
import re
from lxml import html

from .connector import Connector
from .interface import ICommand


class Version(ICommand):
    """Version
    """

    __url_patch_notes = "https://robertsspaceindustries.com/patch-notes"
    __regex_website_version = r'((\d\.?)+)'
    __regex_website_background = r"(background-image\s*:\s*url\(')(.*)('\))"

    def __init__(self, latest: bool = False):
        """
        Args:
            latest (bool): Only return latest.
        """
        self.latest = latest

    async def execute_async(self):
        return self.execute()

    def execute(self):
        result = []
        req = Connector().request(self.__url_patch_notes, method="get")

        if req is None or req.status_code != 200:
            return None

        resp = req.text
        tree = html.fromstring(resp)
        for patch in tree.xpath("//*[contains(@class, 'content-block2') and contains(@class, 'hub-block')]"):
            p = {}

            # get article url
            href = patch.attrib['href']
            if href.startswith('http'):
                p['link'] = href
            else:
                p['link'] = Connector.url_host + href

            # get article title
            for title in patch.xpath("//*[contains(@class, 'title-holder')]/*/text()"):
                p['title'] = title.strip()
                if m := re.search(self.__regex_website_version, title):
                    p['version'] = m.group(1)

            # get background image
            for style in patch.xpath("//*[contains(@class, 'background')]/@style"):
                if m := re.match(self.__regex_website_background, style):
                    background = m.group(2)

                    if background.startswith('http'):
                        p['image'] = background
                    else:
                        p['image'] = Connector.url_host + background

            result.append(p)
        return result
