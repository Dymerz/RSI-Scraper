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
	__regex_website = r'((\d\.?)+)'

	def __init__(self, latest: bool=False):
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
		for i in range(1, int(tree.xpath("count(//*[contains(@class, 'content-block2') and contains(@class, 'hub-block')])")) + 1):
			for v in tree.xpath("//*[contains(@class, 'content-block2') and contains(@class, 'hub-block')][{}]/*[contains(@class, 'title-holder')]/*/text()".format(i)):
				m = re.search(self.__regex_website, v.strip())
				if m:
					result.append(m.group(1))
			if self.latest:
				break

		return result
