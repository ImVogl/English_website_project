# Файл со вспомогательными функциями для тестов
from random import shuffle

def outValues_covert_to_boolean(outValues):
	if outValues == 'simpleRus':
		return True, True, False, False
	if outValues == 'simple':
		return False, True, False, False
	if outValues == 'random':
		boolList = [True, False, False, False]
		shuffle(boolList)
		return boolList[0], boolList[1], boolList[2], boolList[3]

def select_values(content, outValues):
	boolOutValues = outValues_covert_to_boolean(outValues)
	keys = ['rus', 'simple', 'past_simple', 'pass_participle']
	result = {}
	for i in range(4):
		if boolOutValues[i]:
			result[keys[i]] = content[i]
		else:
			result[keys[i]] = ''

	return result