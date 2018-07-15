import psycopg2
from logs.LogProccessing import write_to_log
from datetime import date, datetime

def get_userdata(num):
	connect = psycopg2.connect(host = 'localhost', user = 'Some_user', password = '', dbname = 'users')
	cursor = connect.cursor()
	cursor.execute("""SELECT * FROM users WHERE unum = %s;""", ( num,))
	result = cursor.fetchall()
	cursor.close()
	connect.close()
	return result[0][3]


def set_userdata(data):
	if len(data) == 7:
		with psycopg2.connect(host = 'localhost', user = 'postgres', password = '82$_ARLu4', dbname = 'users') as connect:
			with connect.cursor() as cursor:
				cursor.execute("""INSERT INTO users VALUES(%s, %s, %s, %s, %s, %s, %s);""",
					(data[0], data[1], data[2], data[3], data[4], data[5], data[6]) )
		cursor.close()
		connect.close()
		return True
	else:
		return False

def compare_log(log, password):
	_num = -1
	connect = psycopg2.connect(host = 'localhost', user = 'Some_user', password = '', dbname = 'users')
	cursor = connect.cursor()
	cursor.execute("""select unum from users where ulogin = %s AND upass = %s;""", (log, password, ))
	_num = cursor.fetchall()
	if _num[0][0] != -1:
		cursor.close()
		connect.close()
		return True, True
	cursor.execute("""select unum from users where ulogin = %s ;""", (log, ))
	_num = cursor.fetchall()
	if _num[0][0] != -1:
		cursor.close()
		connect.close()
		return True, False
	cursor.close()
	connect.close()
	return False, False