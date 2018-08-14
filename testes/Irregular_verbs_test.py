from .tests_db import get_irr, get_sentence, get_verb_exact
from .test_utilits import select_values
from numpy import arange, random, delete, zeros
from random import shuffle


# Choice 'num' random numbers from 'numb'
def un_numbers(numb, num):
	n = zeros(num, dtype = int)
	for i in range(num):
		j = 0
		while j < num:
			flag = True
			n[i] = random.choice(numb, 1)
			for k in range(0, i - 1):
				if n[i] == n[k]:
					flag = False
			if flag:
				j += 1
	return n

# Get text with specific verbs
def get_text(verbs, numreg):
	result = []
	new_verbs = []
	for verb in verbs:
		sentence, verbs_array = get_sentence(False, verb)
		result.append(sentence)
		new_verbs.append(verbs_array)
	for i in range(numreg):
		result.append(get_sentence(True, ''))
	shuffle(result)
	return result, new_verbs

# Адаптация списка глаголов
def test_ir(oft, num):
	verbs = get_irr(oft)
	numbers = arange(len(verbs))
	delnum = un_numbers(numbers, len(verbs) - num)
	numbers = delete(numbers, delnum)
	shuffle(numbers)
	result = []
	for i in range(num):
		result.append(verbs[numbers[i]][0:4])
	return result

# Получение итогового списка глаголов 
def irregular_verbs_setup(request):
	frequency = request.POST.get('content[IRREGULAR_SETUP][frequency]')
	num = int(request.POST.get('content[IRREGULAR_SETUP][num]'))

	doesAddRegular = 'True' in request.POST.get('content[IRREGULAR_SETUP][doesAddRegular]')
	if frequency == 'oft':
		if num < 50:
			oft = 'oft_1'
		elif num > 80:
			oft = 'oft_3'
		else:
			oft = 'oft_2'
	elif frequency == 'seldom':
		oft = 'seldom'
	elif frequency == 'all' or frequency == 'text':
		oft = ''

	verbs = test_ir(oft, num)
	if frequency == 'text':
		sentences, verbs_from_table = get_text(verbs, int(0.5*len(verbs))) # verbs_from_table - нужна для проверки корректности ввода пользователем данных
		return sentences, verbs_from_table, True
	else:
		if doesAddRegular:
			verbs += get_random_regular(int(0.3*num))
			shuffle(verbs)
		return verbs, None, False

def check_answers_irr(user_answer, content, outValues, iterator):
	result = {}
	keys = ['rus', 'simple', 'past_simple', 'pass_participle']
	if content.isText:
		if not bool(content.supportContent.count(user_answer['simple'])):
			return {'rus':[False, None], 'simple':[False, None], 'past_simple':[False, None], 'pass_participle':[False, None]}
		verbs = get_verb_exact('irregular', user_answer['simple'])
		for i in range(4):
			if verbs[i] == user_answer[keys[i]]:
				result[keys[i]] = True
			else:
				result[keys[i]] = False
	else:
		nextValues = select_values(content.mainContent[iterator + 1], outValues)
		for i in range(4):
			if content.mainContent[iterator][i] == user_answer[keys[i]]:
				result[keys[i]] = [True, nextValues[keys[i]]]
			else:
				result[keys[i]] = [False, nextValues[keys[i]]]

	return result
