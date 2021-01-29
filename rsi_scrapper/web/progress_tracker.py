"""Roadmap
"""
from .connector import Connector
from .interface import ICommand

class ProgressTracker(ICommand):
	"""ProgressTracker
	"""

	__url_progress_tracker = "https://robertsspaceindustries.com/graphql"

	def __init__(self):
		"""
		Args:
			date_min (str): The roadmap start date.
			date_max (str): The roadmap end date.
		"""
		self.date_min = "2020-01-01"
		self.date_max = "2022-12-31"

	async def execute_async(self):
		return self.execute()

	def execute(self):
		return self.get_teams()

	def get_teams(self):
		data = [
			{
				"operationName": "teams",
				"query": """query
					teams($startDate: String!, $endDate: String!) {
						progressTracker {
							teams(startDate: $startDate, endDate: $endDate) {
								...Team
								__typename
							}
							__typename
						}
					}
					fragment Team on Team {
						title  description  uuid  startDate  endDate  numberOfDeliverables  slug  __typename
					}
					""",
				"variables": {
					"startDate": self.date_min,
					"endDate": self.date_max,
				}
			}
		]
		req = Connector().request(self.__url_progress_tracker, method="post", json_data=data)
		if req is None or req.status_code != 200:
			return None
		try:
			resp = req.json()
		except Exception as e:
			print(e, flush=True)
			return None

		if len(resp) > 0 and 'data' not in resp[0]:
			return None

		return resp[0]['data']['progressTracker']['teams']



class ProgressTrackerInfo(ICommand):
	"""ProgressTrackerInfo
	"""

	__url_progress_tracker = "https://robertsspaceindustries.com/graphql"

	def __init__(self, slug: str):
		"""
		Args:
			date_min (str): The roadmap start date.
			date_max (str): The roadmap end date.
			slug (str): The slug identifier to get.
		"""
		self.team_slug = slug
		self.date_min = "2020-01-01"
		self.date_max = "2022-12-31"

	async def execute_async(self):
		return self.execute()

	def execute(self):
		deliverables = self.get_deliverables(self.team_slug)
		disciplines_slugs = [deliv['slug'] for deliv in deliverables]

		disciplines = self.get_disciplines(self.team_slug, disciplines_slugs)

		for i in range(len(deliverables)):
			deliverables[i]['disciplines'] = disciplines[i]
		return deliverables

	def get_deliverables(self, team_slug):
		data = [
			{
				"operationName": "deliverables",
				"query": """query
					deliverables($teamSlug: String!, $startDate: String!, $endDate: String!) {
						progressTracker {
							deliverables(teamSlug: $teamSlug, startDate: $startDate, endDate: $endDate) {
								...Deliverable
								projects {
									...Project
									__typename
								}
								__typename
							}
							__typename
						}
					}
					fragment Deliverable on Deliverable {
						uuid
						slug
						title
						description
						startDate
						endDate
						numberOfDisciplines
						__typename
					}
					fragment Project on Project {
						title
						logo
						__typename
					}
					""",
				"variables": {
					"teamSlug": team_slug,
					"startDate": self.date_min,
					"endDate": self.date_max,
				}
			}
		]
		req = Connector().request(self.__url_progress_tracker, method="post", json_data=data)

		if req is None or req.status_code != 200:
			return None
		try:
			resp = req.json()
		except Exception as e:
			print(e, flush=True)
			return None

		if len(resp) > 0 and 'data' not in resp[0]:
			return None

		return resp[0]['data']['progressTracker']['deliverables']

	def get_disciplines(self, team_slug:str, delivery_slugs:list()):
		data = []
		for del_slug in delivery_slugs:
			data.append({
				"operationName": "disciplines",
				"query": """query
					disciplines($teamSlug: String! $deliverableSlug: String! $startDate: String! $endDate: String! ) {
						progressTracker {
							disciplines(teamSlug: $teamSlug deliverableSlug: $deliverableSlug startDate: $startDate endDate: $endDate ) {
								...Discipline
								timeAllocations {
									...TimeAllocation
									__typename
								}
								__typename
							}
							__typename
						}
					}
					fragment Discipline on Discipline {
						title
						color
						uuid
						numberOfMembers
						__typename
					}
					fragment TimeAllocation on TimeAllocation {
						startDate
						endDate
						uuid
						partialTime
						__typename
					}
					""",
				"variables": {
					"teamSlug": team_slug,
					"deliverableSlug": del_slug,
					"startDate": self.date_min,
					"endDate": self.date_max,
				}
			})

		req = Connector().request(self.__url_progress_tracker, method="post", json_data=data)

		if req is None or req.status_code != 200:
			return None
		try:
			resp = req.json()
		except Exception as e:
			print(e, flush=True)
			return None

		if len(resp) > 0 and 'data' not in resp[0]:
			return None

		return [d['data']['progressTracker']['disciplines'][0] for d in resp]