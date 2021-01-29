from .database import Controller
import json
from datetime import datetime

class Me:
	def __init__(self, apikey:str):
		self.apikey = apikey

	def get_data(self):
		controller = Controller()
		info = controller.get_me(self.apikey)

		data = {
			"id": info[0],
			"user_key": info[1],
			"oauth_id": info[2],
			"value": info[3],
			"privileged": info[4],
			"provider": info[5],
			"edition_date": int(datetime.timestamp(info[6])),
			"creation_date": int(datetime.timestamp(info[7])),
		}

		return data;
