from random import randint
import psycopg2

def getTableLen(tableName, dbName):
	connect = psycopg2.connect(host = 'localhost', user = 'Some_user', password = '', dbname = dbName)
	cursor = connect.cursor()
	cursor.execute("""SELECT COUNT(*) FROM %s;""", ( tableName, ))
	result = cursor.fetchall()
	cursor.close()
	connect.close()
	return result[0][0]

def get_irr(oft):
	connect = psycopg2.connect(host = 'localhost', user = 'Some_user', password = '', dbname = 'Testes_DB')
	cursor = connect.cursor()
	if oft == 'oft_1':
		cursor.execute("""SELECT * FROM irregular_verbs WHERE frequency = %s;""", ( "group_1",))
	elif oft == 'oft_2':
		cursor.execute("""SELECT * FROM irregular_verbs WHERE frequency = %s AND frequency = %s;""", ( "group_1", "group_2", ))
	elif oft == 'oft_3':
		cursor.execute("""SELECT * FROM irregular_verbs WHERE frequency != %s;""", ( "seldom", ))
	elif oft == 'seldom':
		cursor.execute("""SELECT * FROM irregular_verbs WHERE frequency == %s;""", ( "seldom", ))
	else:
		cursor.execute("""SELECT * FROM irregular_verbs;""")
	result = cursor.fetchall()
	cursor.close()
	connect.close()
	return result[0:4]

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