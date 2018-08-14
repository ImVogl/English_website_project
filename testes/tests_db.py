from logs.LogProccessing import write_to_log
from random import randint
import psycopg2

# Число строчек в базеданных
def getTableLen(tableName, dbName):
	try:
		connect = psycopg2.connect(host = 'localhost', user = 'Some_user', password = '', dbname = dbName)
	except psycopg2.Error as error:
		write_to_log(['PostgreSQL connect error:', error.pgerror])
		connect.close()
		return 0
	
	cursor = connect.cursor()
	try:
		cursor.execute("""SELECT COUNT(*) FROM %s;""", ( tableName, ))
		result = cursor.fetchall()
	except psycopg2.Error as error:
		write_to_log(['PostgreSQL execute error:', error.pgerror])
		return ['']*4
	finally:
		cursor.close()
		connect.close()
	return result[0][0]

# Изъятие неправильного глагола из таблицы
def get_irr(oft):
	try:
		connect = psycopg2.connect(host = 'localhost', user = 'Some_user', password = '', dbname = 'Testes_DB')
	except psycopg2.Error as error:
		write_to_log(['PostgreSQL connect error:', error.pgerror])
		connect.close()

	cursor = connect.cursor()
	try:
		if oft == 'oft_1':
			cursor.execute("""SELECT * FROM irregular_verbs WHERE frequency = %s;""", ( "oft_1",))
		elif oft == 'oft_2':
			cursor.execute("""SELECT * FROM irregular_verbs WHERE frequency = %s OR frequency = %s;""", ( "oft_1", "oft_2", ))
		elif oft == 'oft_3':
			cursor.execute("""SELECT * FROM irregular_verbs WHERE frequency <> %s;""", ( "seldom", ))
		elif oft == 'seldom':
			cursor.execute("""SELECT * FROM irregular_verbs WHERE frequency = %s;""", ( "seldom", ))
		else:
			cursor.execute("""SELECT * FROM irregular_verbs;""")

		result = cursor.fetchall()

	except psycopg2.Error as error:
		write_to_log(['PostgreSQL execute error:', error.pgerror])
		return ['']*4
	finally:
		cursor.close()
		connect.close()

	return result

# Изятие предложений или текста, содержащий указанные неправильные глаголы
def get_sentence(isRegular, verb):
	connect = psycopg2.connect(host = 'localhost', user = 'Some_user', password = '', dbname = 'Testes_DB')
	cursor = connect.cursor()
	# If verb is empty, we get random sentence
	if len(verb) == 0:
		if isRegular:
			n = getTableLen('sentences_with_regular', 'Testes_DB')
			numb = randint(1, n)
			cursor.execute("""SELECT sentence FROM sentences_with_regular WHERE rnum = %s;""", ( str(numb),))
		else:
			n = getTableLen('sentences_with_irregular', 'Testes_DB')
			numb = randint(1, n)
			cursor.execute("""SELECT sentence FROM sentences_with_irregular WHERE inum = %s;""", ( str(numb),))
		result = cursor.fetchall()
		cursor.close()
		connect.close()
		return result
	else:
		if isRegular:
			cursor.execute("""SELECT sentence FROM sentences_with_regular WHERE %s = ANY(verbs);""", ( verb,))
		else:
			cursor.execute("""SELECT sentence FROM sentences_with_irregular WHERE %s = ANY(verbs);""", ( verb,))
		result = cursor.fetchall()
		cursor.close()
		connect.close()
		return result[0], result[1][0]	# Возможно, тут нужно поправить (первый столбец - предложение, второй столбец - список кортеджей, которые содерат списки глаголов)

# Изъятие случайного существительного
def get_random_substantive(frequency, limit):
	try:
		connect = psycopg2.connect(host = 'localhost', user = 'Some_user', password = '', dbname = 'Testes_DB')
	except psycopg2.Error as error:
		write_to_log(['PostgreSQL connect error:', error.pgerror])
		connect.close()

	cursor = connect.cursor()
	try:
		cursor.execute("""SELECT substantive FROM substantives WHERE frequency > %s ORDER BY RANDOM() LIMIT %s;""", (frequency, limit, ))
		result = cursor.fetchall()

	except psycopg2.Error as error:
		write_to_log(['PostgreSQL execute error:', error.pgerror])
		return ['']*4
	finally:
		cursor.close()
		connect.close()
	return result

def get_verb_exact(type, verb):
	try:
		connect = psycopg2.connect(host = 'localhost', user = 'Some_user', password = '', dbname = 'Testes_DB')
	except psycopg2.Error as error:
		write_to_log(['PostgreSQL connect error:', error.pgerror])
		connect.close()

	cursor = connect.cursor()
	try:
		if type == 'irregular':
			cursor.execute("""SELECT * FROM irregular_verbs WHERE infinitive = %s;""", ( verb,))
		else:
			cursor.execute("""SELECT * FROM regular_verbs WHERE infinitive = %s;""", ( verb,))
		result = cursor.fetchall()
	except psycopg2.Error as error:
		write_to_log(['PostgreSQL execute error:', error.pgerror])
		return ['']*4
	finally:
		cursor.close()
		connect.close()
	return result

def get_random_regular(limit):
	try:
		connect = psycopg2.connect(host = 'localhost', user = 'Some_user', password = '', dbname = 'Testes_DB')
	except psycopg2.Error as error:
		write_to_log(['PostgreSQL connect error:', error.pgerror])
		connect.close()

	cursor = connect.cursor()
	try:
		cursor.execute("""SELECT substantive FROM substantives ORDER BY RANDOM() LIMIT %s;""", (limit, ))
		result = cursor.fetchall()
	except psycopg2.Error as error:
		write_to_log(['PostgreSQL execute error:', error.pgerror])
		return ['']*4
	finally:
		cursor.close()
		connect.close()

	return result