"""Get User
"""
from datetime import datetime
from lxml import html

from .connector import Connector
from .interface import ICommand


class User(ICommand):
    """Get User
    """

    __url_profile = "https://robertsspaceindustries.com/citizens/{0}"
    __url_affiliation = "https://robertsspaceindustries.com/citizens/{0}/organizations"

    def __init__(self, user_handle):
        """Get user info.

        Args:
            user_handle (str): The user handle.
        """
        super().__init__()
        self.user_handle = user_handle

    async def execute_async(self):
        return self.execute()

    def execute(self):
        return self.get_user_info(self.user_handle)

    def get_user_info(self, user_handle: str):
        """Get the user profile.

        Args:
            user_handle (str): The user handle.

        Returns:
            dict: The user info.
        """

        # format url
        url = self.__url_profile.format(user_handle)

        # request website
        req = Connector().request(url, method="get")

        if req is None or req.status_code == 404:
            return {}
        elif req.status_code != 200:
            return None

        # get html contents
        tree = html.fromstring(req.content)

        # begin store basic data
        result = {"profile": {}, "organization": {}}

        result["profile"]["page"] = {}
        result["profile"]["page"]["url"] = url

        # get identifier
        for v in tree.xpath('//title/text()'):
            result["profile"]["page"]["title"] = v.strip()
            break

        # get identifier
        for v in tree.xpath('//*[contains(@class, "label") and text() = "UEE Citizen Record"]/following-sibling::*[1]/text()'):
            result["profile"]["id"] = v.strip()
            break

        # get displayed name
        for v in tree.xpath('//*[@class="info"][1]/p[1]/*[@class="value"]/text()'):
            result["profile"]["display"] = v.strip()
            break

        # get handle
        for v in tree.xpath('//*[contains(@class, "label") and text() = "Handle name"]/following-sibling::*[1]/text()'):
            result["profile"]["handle"] = v.strip()
            break

        # get badge
        for v in tree.xpath('//*[@class="info"][1]/p[last()]/*[@class="value"]/text()'):
            result["profile"]["badge"] = v.strip()
            break

        # get badge image
        for v in tree.xpath('//*[@class="info"][1]/*[@class="entry"]/*[@class="icon"]/img/@src'):
            d = v.strip()
            if d[0:1] == '/':
                d = "https://robertsspaceindustries.com" + d
            result["profile"]["badge_image"] = d
            break

        # get profile image
        for v in tree.xpath('//*[contains(@class, "title") and contains(text(), "Profile")]/following-sibling::*/div[@class="thumb"]/img/@src'):
            result["profile"]["image"] = Connector.convert_path(v.strip())
            break

        # get organization image
        for v in tree.xpath('//*[contains(@class, "title") and contains(text(), "Main organization")]/following-sibling::*/div[@class="thumb"]/a/img/@src'):
            result["organization"]["image"] = Connector.convert_path(v.strip())
            break

        # get organization name
        for v in tree.xpath('//a[contains(@class, "value") and contains(@class, "data")]/text()'):
            result["organization"]["name"] = v.strip()
            break

        # get organization SID (Spectrum Identification)
        for v in tree.xpath('//*[contains(@class, "label") and text() = "Spectrum Identification (SID)"]/following-sibling::*[1]/text()'):
            result["organization"]["sid"] = v.strip()
            break

        # get organization rank
        for v in tree.xpath('//*[contains(@class, "label") and text() = "Organization rank"]/following-sibling::*[1]/text()'):
            result["organization"]["rank"] = v.strip()
            break

        # get organization stars
        result["organization"]["stars"] = len(tree.xpath(".//*[contains(@class, 'ranking')]/span[contains(@class, 'active')]"))

        # get enlist date
        for v in tree.xpath('//*[contains(@class, "label") and text() = "Enlisted"]/following-sibling::*[1]/text()'):
            result["profile"]["enlisted"] = datetime.strptime(v.strip(), "%b %d, %Y").strftime('%Y-%m-%dT%H:%M:%S.%f')
            break

        # find country and/or region
        for v in tree.xpath('//*[contains(@class, "label") and text() = "Location"]/following-sibling::*[@class="value"]/text()'):
            result["profile"]["location"] = {}
            if "," in v.strip():
                arr = v.split(",")  # location splitter
                result["profile"]["location"]["country"] = arr[0].strip()
                result["profile"]["location"]["region"] = arr[1].strip()
            else:
                result["profile"]["location"]["country"] = v.strip()
            break

        # get fluency
        for v in tree.xpath('//*[contains(@class, "label") and text() = "Fluency"]/following-sibling::*[1]/text()'):
            result["profile"]["fluency"] = [x.strip() for x in v.split(",")]
            break

        # get website
        for v in tree.xpath('//*[contains(@class, "label") and text() = "Website"]/following-sibling::*/text()'):
            result["profile"]["website"] = v.strip()
            break

        # get bio
        result["profile"]["bio"] = ""
        for v in tree.xpath('//*[contains(@class, "label") and text() = "Bio"]/following-sibling::*[@class="value"]//text()'):
            result["profile"]["bio"] += v
        result["profile"]["bio"] = result["profile"]["bio"].strip()

        # remove useless bio
        if result["profile"]["bio"] == "":
            del result["profile"]["bio"]

        result["affiliation"] = self._get_user_affiliations(user_handle)

        return result

    def _get_user_affiliations(self, user_handle: str):
        """Get user affiliations.

        Args:
            user_handle (str): The user handle.

        Returns:
            dict: The user affiliations.
        """

        # format url
        url = self.__url_affiliation.format(user_handle)

        # request website
        req = Connector().request(url, method="get")

        if req is None or req.status_code == 404:
            return {}
        elif req.status_code != 200:
            return None

        # get html contents
        tree = html.fromstring(req.content)

        # store basic data
        result = []

        for a in tree.xpath("//*[contains(@class, 'affiliation')]"):
            aff = {}

            for v in a.xpath(".//*[contains(@class, 'entry')]/strong[contains(../span, 'SID')]/text()"):
                aff["sid"] = v.strip()
                break

            for v in a.xpath(".//*[contains(@class, 'orgtitle')]/a/text()"):
                aff["name"] = v.strip()
                break

            for v in a.xpath(".//*[contains(@class, 'entry')]/strong[contains(../span, 'rank')]/text()"):
                aff["rank"] = v.strip()
                break
            aff["stars"] = len(a.xpath(".//*[contains(@class, 'ranking')]/span[contains(@class, 'active')]"))

            for v in a.xpath(".//img/@src"):
                aff["image"] = Connector.convert_path(v.strip())
                break

            result.append(aff)

        return result
