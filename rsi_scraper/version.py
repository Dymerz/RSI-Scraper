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

    def __init__(self):
        pass

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
            p['link'] = Connector.convert_path(href)

            # get article title
            for title in patch.xpath("./*[contains(@class, 'title-holder')]/*/text()"):
                p['title'] = title.strip()
                m = re.search(self.__regex_website_version, title)
                if m:
                    p['version'] = m.group(1)

            # get background image
            for style in patch.xpath("./*[contains(@class, 'background')]/@style"):
                m = re.match(self.__regex_website_background, style)
                if m:
                    background = m.group(2)
                    p['image'] = Connector.convert_path(background)

            result.append(p)
            print(p)
        return result
