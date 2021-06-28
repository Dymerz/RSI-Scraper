"""Roadmap
"""
from .connector import Connector
from .interface import ICommand


class ProgressTracker(ICommand):
    """ProgressTracker
    """

    __url_progress_tracker = "https://robertsspaceindustries.com/graphql"

    def __init__(self, date_min="2020-01-01", date_max="2022-12-31"):
        """
        Args:
            date_min (str): The roadmap start date.
            date_max (str): The roadmap end date.
        """
        self.date_min = date_min
        self.date_max = date_max
        self.limit = 20
        self.offset = 0

    async def execute_async(self):
        return self.execute()

    def execute(self):
        return self.get_teams()

    def get_teams(self):
        data = [
            {
                "operationName": "teams",
                "query": """query
                    teams(
                        $startDate: String!,
                        $endDate: String!,
                        $search: String,
                        $teamSlug: String,
                        $deliverableSlug: String,
                        $projectSlugs: [String],
                        $disciplineSlugs: [String],
                        $sortBy: SortMethod,
                        $offset: Int,
                        $limit: Int
                    ) {
                        progressTracker {
                            teams(
                                startDate: $startDate
                                endDate: $endDate
                                search: $search
                                teamSlug: $teamSlug
                                deliverableSlug: $deliverableSlug
                                projectSlugs: $projectSlugs
                                disciplineSlugs: $disciplineSlugs
                                sortBy: $sortBy
                                offset: $offset
                                limit: $limit) {
                                    totalCount
                                    metaData {
                                        ...Team
                                        timeAllocations {
                                            ...TimeAllocation
                                            __typename
                                        }
                                        __typename
                                    }
                                    __typename
                                }
                            __typename
                        }
                    }
                    fragment Team on Team {
                        title
                        description
                        uuid
                        abbreviation
                        startDate
                        endDate
                        numberOfDeliverables
                        slug
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
                    "startDate": self.date_min,
                    "endDate": self.date_max,
                    "offset": self.offset,
                    "limit": self.limit
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

        return resp[0]['data']['progressTracker']['teams']['metaData']


class ProgressTrackerInfo(ICommand):
    """ProgressTrackerInfo
    """

    __url_progress_tracker = "https://robertsspaceindustries.com/graphql"

    def __init__(self, slug: str, date_min="2020-01-01", date_max="2022-12-31"):
        """
        Args:
            slug (str): The slug identifier to get.
            date_min (str): The roadmap start date.
            date_max (str): The roadmap end date.
        """
        self.team_slug = slug
        self.date_min = date_min
        self.date_max = date_max

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
                    deliverables(
                        $startDate: String!,
                        $endDate: String!,
                        $search: String,
                        $deliverableSlug: String,
                        $teamSlug: String,
                        $projectSlugs: [String],
                        $categoryIds: [Int],
                        $sortBy: SortMethod,
                        $offset: Int,
                        $limit: Int
                    ) {
                        progressTracker {
                            deliverables(
                                startDate: $startDate
                                endDate: $endDate
                                search: $search
                                deliverableSlug: $deliverableSlug
                                teamSlug: $teamSlug
                                projectSlugs: $projectSlugs
                                categoryIds: $categoryIds
                                sortBy: $sortBy
                                offset: $offset
                                limit: $limit
                            ) {
                                totalCount
                                metaData {
                                    ...Deliverable card {
                                        ...Card
                                        __typename
                                    }
                                    projects {
                                        ...Project
                                        __typename
                                    }
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
                        numberOfTeams
                        updateDate
                        totalCount
                        __typename
                    }
                    fragment Card on Card {
                        id
                        title
                        description
                        category
                        release {
                            id
                            title
                            __typename
                        }
                        board {
                            id
                            title
                            __typename
                        }
                        updateDate
                        thumbnail
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

        return resp[0]['data']['progressTracker']['deliverables']['metaData']

    def get_disciplines(self, team_slug: str, delivery_slugs: list()):
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
