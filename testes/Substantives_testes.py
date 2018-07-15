from .tests_db import get_random_substantive
from inflect import engine

def plural_substantive_test(frequency, num):
	singulars_substantives = get_random_substantive(frequency, num)
	plurals_substantives = []
	engine = engine()
	for substatintive in singulars_substantives:
		plurals_substantives.append(engine.plural(substatintive))

	return singulars_substantives, plurals_substantives

# Получение итогового списка существительных
def plural_substantive_setup(request):
	oft = request.POST.get('frequency')
	num = int(request.POST.get('num'))
	if oft == 'oft_1':
		singulars, plurals = plural_substantive_test(80, num)
	if oft == 'oft_2':
		singulars, plurals = plural_substantive_test(40, num)
	if oft == 'oft_3':
		singulars, plurals = plural_substantive_test(30, num)
	if oft == 'oft_4':
		singulars, plurals = plural_substantive_test(15, num)
	else:
		singulars, plurals = plural_substantive_test(0, num)

	return singulars, plurals

def check_answers_pl(user_answer, content, iterator):
	keys = ['singular', 'plural']
	result = {}
	result.keys[0] = [bool(content.mainContent[iterator] == user_answer[keys[0]]), content.mainContent[iterator + 1]]
	result.keys[1] = [bool(content.supportContent[iterator] == user_answer[keys[1]]), '']
	return result
