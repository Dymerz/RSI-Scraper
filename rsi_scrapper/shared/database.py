import json, datetime, random, re
import mysql.connector as mariadb

class Controller:

	db = None

	def __init__(self, database = None):
		if database is None:
			self.db = Database()
		else:
			self.db = database

	# Consume user key
	def call_cost(self, key, cost: int = 1):
		self.db.connect()
		self.db.call_cost(key, cost)
		self.db.disconnect()

	def is_maintenance(self):
		self.db.connect()
		res = int(self.db.get_parameter("maintenance"))
		self.db.disconnect()

		return res != 0

	def apikey_exist(self, key):
		self.db.connect()

		res = self.db.apikey_exist(key)
		self.db.disconnect()
		return res

	def apikey_valid(self, key):
		self.db.connect()

		res = self.db.get_apikey(key)
		self.db.disconnect()
		return res[3] > 0 or res[4] == 1

	def add_user(self, handle, user_array):
		self.db.connect()

		if(not self.db.user_exist(handle)):
			self.db.add_user(handle, user_array)
		else:
			self.db.set_user(handle, user_array)
		self.db.disconnect()

	def add_orga(self, sid, orga_array):

		self.db.connect()

		if(not self.db.orga_exist(sid)):
			self.db.add_organization(sid, orga_array)
		else:
			cache = self.db.get_organization(sid)
			if "members_list" in cache and "members_list" not in orga_array:
				orga_array['members_list'] = cache["members_list"]
			self.db.set_organization(sid, orga_array)
		self.db.disconnect()

	def add_version(self, version, live):
		self.db.connect()

		if not self.db.version_exist(version, live):
			self.db.add_version(version, live)
		self.db.disconnect()

	def add_ship(self, ship_id, ship_array):
		self.db.connect()

		if(not self.db.ship_exist(ship_id)):
			self.db.add_ship(ship_id, ship_array)
		else:
			self.db.set_ship(ship_id, ship_array)
		self.db.disconnect()

	def add_roadmap_release(self, name: str, board: str, release_array):
		self.db.connect()

		if board == 'starcitizen':
			board = 1
		elif board == 'squadron42':
			board = 2
		elif board == 'progress-tracker':
			board = 10

		if not self.db.roadmap_exist(name, board, release_array):
			self.db.add_roadmap_release(name, board, release_array)

		self.db.disconnect()

	def add_starmap(self, field: str, name: str, starmap_array):
		self.db.connect()

		if not self.db.starmap_exist(field, name):
			self.db.add_starmap(field, name, starmap_array)
		else:
			self.db.set_starmap(field, name, starmap_array)

		self.db.disconnect()

	def get_versions(self):
		self.db.connect()
		res = self.db.get_versions()
		self.db.disconnect()

		return res

	def get_roadmap_release(self, name: str, board: str, date_min: int, date_max: int):
		if board == 'starcitizen':
			board = 1
		elif board == 'squadron42':
			board = 2

		if date_min is None:
			date_min = 0

		if date_max is None:
			date_max = int(datetime.datetime.now().timestamp())

		self.db.connect()
		res = self.db.get_roadmap_release(name, board, date_min, date_max)
		self.db.disconnect()

		return res

	def get_me(self, apikey: str):
		self.db.connect()

		res = self.db.get_apikey(apikey)
		if res is None:
			return None

		self.db.disconnect()
		return res

	def get_apikey_value(self, oauth_id: str):
		self.db.connect()

		res = self.db.get_apikey_by_discord_id(oauth_id)
		if res is None:
			return None
		value = res['value']

		self.db.disconnect()
		return value

	def get_apikey(self, oauth_id: str):
		self.db.connect()

		res = self.db.get_apikey_by_discord_id(oauth_id)
		if res is None:
			return None

		value = res['user_key']

		self.db.disconnect()
		return value

	def get_all_info(self, oauth_id: str):
		self.db.connect()

		row = self.db.get_apikey_by_discord_id(oauth_id)
		if row is None:
			return None

		self.db.disconnect()
		return row

	def get_stats(self):
		self.db.connect()
		res = self.db.get_stats()
		self.db.disconnect()

		return res

	def get_starmap(self, field: str, name: str=None):
		self.db.connect()
		res = self.db.get_starmap(field, name)
		self.db.disconnect()

		if len(res) == 0:
			return None
		return res

	def get_telemetry(self, version: str, timetable: str):
		self.db.connect()
		res = self.db.get_starmap(version, timetable)
		self.db.disconnect()

		if len(res) == 0:
			return None
		return res

	def set_stats(self, stats_array):
		self.db.connect()

		if self.db.get_stats() == None:
			self.db.add_stats(stats_array)
		else:
			self.db.set_stats(stats_array)

		self.db.disconnect()

	def set_telemetry(self, version: str, timetable: str, telemetry_array):
		self.db.connect()

		if self.db.get_telemetry(version, timetable) == None:
			self.db.add_telemetry(version, timetable, telemetry_array)
		else:
			self.db.set_telemetry(version, timetable, telemetry_array)

		self.db.disconnect()

	def set_apikey_privilege(self, oauth_id: str, privileged: int):

		self.db.connect()

		self.db.set_apikey_privilege(oauth_id, privileged)

		self.db.disconnect()

	def generate_apikey(self, oauth_id: str, privileged=False):
		apikey = "%032x" % random.getrandbits(128)

		self.db.connect()

		while self.db.apikey_exist(apikey):
			apikey = "%032x" % random.getrandbits(128)

		self.db.add_apikeys(apikey, oauth_id, int(privileged))
		apikey = self.db.get_apikey(apikey)[1]

		self.db.disconnect()
		return apikey


	def check_database(self):
		try:
			self.db.connect()
			self.db.disconnect()
			return True
		except Exception:
			return False

	def unregister_user(self, oauth_id: str):
		self.db.connect()

		res = self.db.del_apikey(oauth_id)

		self.db.disconnect()

		return res

class Database:

	database = None
	cursor = None
	host = 'maria'
	password = 'm7T9fMF3J2JjY12mRYJI'

	def connect(self):
		self.database = mariadb.connect(user='root', password=self.password, host=self.host, database='starcitizen-api')
		self.cursor = self.database.cursor()

	def disconnect(self):
		self.cursor.close()
		self.database.close()

	def apikey_exist(self, key):
		self.cursor.execute("SELECT id FROM apikeys WHERE user_key = %s LIMIT 1;", (key,))

		for _ in self.cursor:
			return True
		return False

	def user_exist(self, handle):
		self.cursor.execute("SELECT id FROM users WHERE handle = %s LIMIT 1;", (handle,))

		for _ in self.cursor:
			return True
		return False

	def orga_exist(self, sid):
		self.cursor.execute("SELECT sid FROM organizations WHERE sid = %s LIMIT 1;", (sid,))

		for _ in self.cursor:
			return True
		return False

	def version_exist(self, version, live=1):
		self.cursor.execute("SELECT id FROM versions WHERE name = %s AND live = %s LIMIT 1;", (version, live))

		for _ in self.cursor:
			return True
		return False

	def roadmap_exist(self, name: str, board: str, data):
		self.cursor.execute("SELECT id FROM roadmap WHERE name = %s AND board = %s AND data = %s LIMIT 1;", (name, board, json.dumps(data)))

		for _ in self.cursor:
			return True
		return False

	def ship_exist(self, ship_id):
		self.cursor.execute("SELECT id FROM ships WHERE ship_id = %s LIMIT 1;", (ship_id,))

		for _ in self.cursor:
			return True
		return False

	def starmap_exist(self, field, name):
		self.cursor.execute("SELECT id FROM starmap WHERE field = %s AND name = %s LIMIT 1;", (field, name))

		for _ in self.cursor:
			return True
		return False



	def get_outdated_users(self, day_validity = 10):
		res = []
		self.cursor.execute("SELECT * FROM users WHERE DATE(edition_date) < DATE_SUB(CURDATE(), INTERVAL %s DAY);", (day_validity,))

		for u in self.cursor:
			res.append(u)
		return res

	def get_outdated_organizations(self, day_validity = 10):
		res = []
		self.cursor.execute("SELECT * FROM organizations WHERE DATE(edition_date) < DATE_SUB(CURDATE(), INTERVAL %s DAY);", (day_validity,))

		for o in self.cursor:
			res.append(o)
		return res

	def get_outdated_ships(self, day_validity = 10):
		res = []
		self.cursor.execute("SELECT * FROM ships WHERE DATE(edition_date) < DATE_SUB(CURDATE(), INTERVAL %s DAY);", (day_validity,))

		for o in self.cursor:
			res.append(o)
		return res

	def get_outdated_roadmap(self, day_validity = 10):
		res = []
		self.cursor.execute("SELECT * FROM roadmap WHERE DATE(edition_date) < DATE_SUB(CURDATE(), INTERVAL %s DAY);", (day_validity,))

		for o in self.cursor:
			res.append(o)
		return res

	def get_outdated_stats(self, day_validity = 10):
		res = []
		self.cursor.execute("SELECT * FROM stats WHERE DATE(edition_date) < DATE_SUB(CURDATE(), INTERVAL %s DAY);", (day_validity,))

		for o in self.cursor:
			res.append(o)
		return res

	def get_outdated_starmap(self, day_validity = 10):
		res = []
		self.cursor.execute("SELECT * FROM starmap WHERE DATE(edition_date) < DATE_SUB(CURDATE(), INTERVAL %s DAY);", (day_validity,))

		for o in self.cursor:
			res.append(o)
		return res


	def get_apikey(self, user_key):
		self.cursor.execute("SELECT * FROM apikeys WHERE user_key = %s LIMIT 1;", (user_key,))

		for k in self.cursor:
			return k
		return None

	def get_versions(self):
		versions = []
		self.cursor.execute("SELECT name, live, creation_date FROM versions ORDER BY name DESC;")

		for n, _, _ in self.cursor:
			versions.append(n)
		return versions

	def get_user(self, handle):
		self.cursor.execute("SELECT data FROM users WHERE handle = %s LIMIT 1;", (handle,))

		for data in self.cursor:
			return json.loads(data[0])
		return None

	def get_users(self, handle):
		users = []
		self.cursor.execute("SELECT data FROM users WHERE handle LIKE %s;", ("%{}%".format(handle),))

		for data in self.cursor:
			users.append(json.loads(data[0]))
		return users

	def get_organization(self, sid):
		self.cursor.execute("SELECT data FROM organizations WHERE sid = %s LIMIT 1;", (sid,))

		for data in self.cursor:
			return json.loads(data[0])
		return None

	def get_organizations(self, sid):
		orgas = []
		self.cursor.execute("SELECT data FROM organizations WHERE sid LIKE %s;", ("%{}%".format(sid),))

		for data in self.cursor:
			orgas.append(json.loads(data[0]))
		return orgas

	def get_ships(self, **kwarg):
		ships = []
		operations_lt = ["length_min", "crew_min", "price_min", "mass_min"]
		operations_gt = ["length_max", "crew_max", "price_max", "mass_max"]

		query_tuple = tuple()
		query_part = ""
		for key, values in kwarg.items():

			if type(values) is str or type(values) is float:
				list_values = [values]
			else:
				list_values = values

			for v in list_values:
				op = "="
				if key in operations_gt:
					key = key.rstrip("_max")
					if key == "crew":
						key = "max_crew"
						op = "<="
				elif key in operations_lt:
					key = key.rstrip("_min")
					if key == "crew":
						op = ">="
						key = "min_crew"

				v = v.replace("%", "\\%")
				v = v.replace("_", "\\_")
				v = v.replace("\\", "\\\\")

				# if number/float
				if re.match(r"^\d+?$", v) or re.match(r"^\d+?\.\d+?$", v):
					query_tuple += ("$."+key, v)
				else:
					op = "LIKE"
					query_tuple += ("$."+key, f"%{v}%")

				query_part += "JSON_VALUE(data, %s) "+op+" %s AND "

		if query_part != "":
			query_part = query_part[:-5] + ";"
		else:
			query_part = "1"

		self.cursor.execute("SELECT data FROM ships WHERE " + query_part, query_tuple)

		for data in self.cursor:
			ships.append(json.loads(data[0]))
		return ships

	def get_roadmap_release(self, name: str, board: int, date_min: int, date_max: int):
		releases = []

		query_tuple = (board, date_min, date_max)
		query_part = ""
		if not name is None:
			query_part = "AND name = %s"
			query_tuple += (name,)

		self.cursor.execute("SELECT r.data FROM \
						(SELECT name, MAX(creation_date) as max_date FROM `roadmap` WHERE \
							board = %s AND UNIX_TIMESTAMP(creation_date) > %s AND UNIX_TIMESTAMP(creation_date) < %s "+query_part+" \
						GROUP BY name) as x \
						INNER JOIN roadmap as r ON r.name = x.name AND r.creation_date = x.max_date \
						ORDER BY r.name ASC", query_tuple)

		for data in self.cursor:
			releases.append(json.loads(data[0]))
		return releases

	def get_parameter(self, name):
		self.cursor.execute("SELECT value FROM parameters WHERE name = %s;", (name,))

		for data in self.cursor:
			return json.loads(data[0])
		return []

	def get_apikey_by_discord_id(self, oauth_id):
		self.cursor.execute("SELECT user_key, oauth_id, value, privileged, edition_date, creation_date FROM apikeys WHERE oauth_id = %s;", (oauth_id,))

		for u, d, v, p, e, c in self.cursor:
			return {
				'user_key': u,
				'oauth_id': d,
				'value': v,
				'privileged': p,
				'edition_date': e,
				'creation_date': c,
			}
		return None

	def get_stats(self):
		self.cursor.execute("SELECT data FROM stats LIMIT 1;")

		for data in self.cursor:
			return json.loads(data[0])
		return None

	def get_starmap(self, field, name):
		starmap = []

		if name is None:
			self.cursor.execute("SELECT data FROM starmap WHERE field = %s;", (field,))
		else:
			self.cursor.execute("SELECT data FROM starmap WHERE field = %s AND name = %s LIMIT 1;", (field, name))

		for data in self.cursor:
			starmap.append(json.loads(data[0]))
		return starmap

	def get_telemetry(self, version, timetable):
		self.cursor.execute("SELECT data FROM telemetry WHERE version = %s AND timetable = %s LIMIT 1;", (version, timetable))

		for data in self.cursor:
			return json.loads(data[0])
		return None


	def set_user(self, handle, user_array):
		self.cursor.execute("UPDATE users SET data=%s, edition_date=NOW() WHERE handle=%s", (json.dumps(user_array), handle))
		self.database.commit()

	def set_organization(self, sid, orga_array):
		self.cursor.execute("UPDATE organizations SET data=%s, edition_date=NOW() WHERE sid=%s", (json.dumps(orga_array), sid))
		self.database.commit()

	def set_ship(self, ship_id, ship_array):
		self.cursor.execute("UPDATE ships SET data=%s, edition_date=NOW() WHERE ship_id=%s", (json.dumps(ship_array), ship_id))
		self.database.commit()

	def set_apikey_privilege(self, oauth_id, privileged):
		self.cursor.execute("UPDATE apikeys SET privileged=%s, edition_date=NOW() WHERE oauth_id=%s", (privileged, oauth_id))
		self.database.commit()

	def set_roadmap_release(self, name, board, release_array):
		self.cursor.execute("UPDATE roadmap SET data=%s, edition_date=NOW() WHERE name = %s AND board = %s", (json.dumps(release_array), name, board))
		self.database.commit()

	def set_stats(self, stats_array):
		self.cursor.execute("UPDATE stats SET data=%s, edition_date=NOW();", (json.dumps(stats_array),))
		self.database.commit()

	def set_starmap(self, field, name, starmap_array):
		self.cursor.execute("UPDATE starmap SET data=%s, edition_date=NOW() WHERE field = %s AND name = %s;", (json.dumps(starmap_array), field, name))
		self.database.commit()

	def set_telemetry(self, version, timetable, telemetry_array):
		self.cursor.execute("UPDATE telemetry SET data=%s, edition_date=NOW() WHERE version = %s AND timetable = %s;", (json.dumps(telemetry_array), version, timetable))
		self.database.commit()


	def call_cost(self, user_key, cost):
		self.cursor.execute("UPDATE apikeys SET value=value-%s, edition_date=NOW() WHERE user_key = %s AND privileged = 0", (cost, user_key))
		self.database.commit()

	def refresh_apikeys(self, value):
		self.cursor.execute("UPDATE apikeys SET value=%s;", (value,))
		self.database.commit()


	def add_user(self, handle, user_array):
		self.cursor.execute("INSERT INTO users (handle, data) VALUES (%s, %s)", (handle, json.dumps(user_array)))
		self.database.commit()

	def add_organization(self, sid, orga_array):
		self.cursor.execute("INSERT INTO organizations (sid, data) VALUES (%s, %s)", (sid, json.dumps(orga_array)))
		self.database.commit()

	def add_version(self, version, live):
		self.cursor.execute("INSERT INTO versions (name, live) VALUES (%s, %s)", (version, live))
		self.database.commit()

	def add_ship(self, ship_id, ship_array):
		self.cursor.execute("INSERT INTO ships (ship_id, data) VALUES (%s, %s)", (ship_id, json.dumps(ship_array)))
		self.database.commit()
		self.database.commit()

	def add_roadmap_release(self, name, board, release_array):
		self.cursor.execute("INSERT INTO roadmap (name, board, data) VALUES (%s, %s, %s)", (name, board, json.dumps(release_array)))
		self.database.commit()

	def add_apikeys(self, user_key, oauth_id, privileged):
		self.cursor.execute("INSERT INTO apikeys (user_key, oauth_id, privileged, provider) VALUES (%s, %s, %s, 'discord')", (user_key, oauth_id, privileged))
		self.database.commit()

	def add_stats(self, stats_array):
		self.cursor.execute("INSERT INTO stats (data) VALUES (%s)", (json.dumps(stats_array),))
		self.database.commit()

	def add_starmap(self, field, name, starmap_array):
		self.cursor.execute("INSERT INTO starmap (field, name, data) VALUES (%s, %s, %s)", (field, name, json.dumps(starmap_array)))
		self.database.commit()

	def add_telemetry(self, version, timetable, telemetry_array):
		self.cursor.execute("INSERT INTO telemetry (version, timetable, data) VALUES (%s, %s, %s)", (version, timetable, json.dumps(telemetry_array)))
		self.database.commit()

	def del_apikey(self, oauth_id):
		self.cursor.execute("DELETE FROM apikeys WHERE oauth_id = %s;", (oauth_id,))
		self.database.commit()
		return self.cursor.rowcount == 1
