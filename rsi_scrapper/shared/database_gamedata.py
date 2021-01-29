import json
import mysql.connector as mariadb

class GameDataController():

	db = None

	def __init__(self, database = None):
		if database is None:
			self.db = GameDataDatabase()
		else:
			self.db = database

	def get_list(self, version, category):
		# TODO: Return None?
		self.db.connect()

		cat_id = self.db.get_category_by_id(category)
		data = self.db.get_names(version, cat_id)

		self.db.disconnect()

	def get_category_list(self):
		self.db.connect()

		data = self.db.get_categories()

		self.db.disconnect()
		return data

	def get_items(self, version, category, name=None):
		self.db.connect()

		cat_id = self.db.get_category_by_id(category)
		data = self.db.get_data(version, cat_id, name)

		self.db.disconnect()
		return data

	def get_search(self, version, category, **kwarg):
		self.db.connect()

		cat_id = self.db.get_category_by_id(category)
		data = self.db.get_search(version, cat_id, **kwarg)

		self.db.disconnect()
		return data

	def get_categories(self):
		self.db.connect()

		res = self.db.get_categories()

		self.db.disconnect()
		return res

	def get_versions(self):
		self.db.connect()

		res = self.db.get_versions()

		self.db.disconnect()
		return res


class GameDataDatabase:

	database = None
	cursor = None
	host = 'maria'

	def connect(self):
		self.database = mariadb.connect(user='gamedata', password='3PtD8xfoQ8NaRRvr', host=self.host, database='starcitizen-gamedata')
		self.cursor = self.database.cursor()

	def disconnect(self):
		self.cursor.close()
		self.database.close()

	def get_category_by_id(self, name):
		self.cursor.execute("SELECT id FROM category WHERE name = %s;", (name,))

		for o in self.cursor:
			return o[0]
		return None

	def get_categories(self):
		res = []
		self.cursor.execute("SELECT name FROM category;")

		for o in self.cursor:
			res.append(o[0])
		return res

	def get_versions(self):
		res = []
		self.cursor.execute("SELECT version FROM gamedata GROUP BY version;")

		for o in self.cursor:
			res.append(o[0])
		return res

	def get_names(self, version, category_id):
		res = []
		self.cursor.execute("SELECT name FROM gamedata WHERE version = %s AND category_id = %s;", (version, category_id))

		for o in self.cursor:
			res.append(o[0])
		return res

	def get_data(self,  version, category_id, name=None):
		res = []
		if name is None:
			self.cursor.execute("SELECT data FROM gamedata WHERE version = %s AND category_id = %s;", (version, category_id))
		else:
			self.cursor.execute("SELECT data FROM gamedata WHERE version = %s AND category_id = %s AND name LIKE %s;", (version, category_id, "%"+name+"%"))

		for o in self.cursor:
			res.append(json.loads(o[0]))
		return res

	def get_search(self, version, category_id, **kwarg):
		gamedata = []

		query_tuple = tuple()

		query_tuple += (version, category_id, category_id)
		query_part = "version = %s AND (category_id = %s OR %s = 10 ) AND "
		for key, values in kwarg.items():
			print(f"{key}->{values}", flush=True)

			v = values
			if "'" in values:
				v = v.replace("'", "\\'")

			try:
				float(v)
			except ValueError:
				v = f"\"{v}\""

			query_part += f"`data` REGEXP '\"({key})\"\s*:\s*({v})' AND "

		if query_part != "":
			query_part = query_part[:-5] + ";"
		else:
			query_part = "1"

		self.cursor.execute("SELECT data, name FROM gamedata WHERE " + query_part, query_tuple)

		for data in self.cursor:
			gamedata.append(json.loads(data[0]))
		return gamedata