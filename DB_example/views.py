import os

from django.shortcuts import render
from django.http.response import HttpResponse
from django.template.loader import get_template
from django.template import Context
from django.shortcuts import render_to_response
from logs.LogProccessing import write_to_log
from DB_example.data_base import get_userdata
from testes.Irregular_verbs_test import irregular_verbs_setup, check_answers_irr
from testes.Substantives_testes import plural_substantive_setup, check_answers_pl
from testes.test_utilits import select_values
from ContentClass import content

# Глобальные переменные
outValues = None
iterator = 0
length = 0
content = content()

def set_global_variables():
	return None, 0, 0, content()

# Test page
def index(request):
	username = "1"
	data_name = ""
	if request.method == "POST":
		username = request.POST.get('username')
		try:
			if (username != "") and (0 < int(username) < 7):
				data_name = get_userdata(int(username))
			else:
				data_name = "Incorrect number!"
		except:
			data_name = "Incorrect number!"
		username = ""
	return render(request, 'index.html', {'data_name': data_name})

# Select test parameters page (test_modal_window.html)
def test_page_function(request):
	global content, outValues, iterator, length
	
	# Если метод иной, то ничего не возвращаем
	if request.method != "POST":
		# Default request returned
		return render(request, 'tests\\test_modal_window.html', {})

	requestTypeList = list(request.POST.keys())

	## Настройки тестов
	# Настройки для тестирования глаголов
	if "IRREGULAR_SETUP" in requestTypeList:
		content.mainContent, content.supportContent, content.isText = irregular_verbs_setup(request)
		if content.isText:
			length = len(content.supportContent)
			return render(request, 'tests\\test_modal_window.html', {'text': content.mainContent})
		else:
			length = len(content.mainContent)
			outValues = request.POST.get('outValues')
			return render(request, 'tests\\test_modal_window.html', select_values(content.mainContent[0], outValues))

	# Настройки для тестирования множественного числа существительных
	if "PLURAL_SETUP" in requestTypeList:
		content.mainContent, content.supportContent = plural_substantive_setup(request)
		length = len(content.mainContent)
		return render(request, 'tests\\test_modal_window.html', {'singular': content.mainContent[0]})

	## Проверка коррректности введеных пользователем значений
	# Проверка глаголов
	if "IRREGULAR_CHECK" in requestTypeList:
		user_answer = {'rus':request.POST.get('rus'), 
						'simple':request.POST.get('simple'), 
						'past_simple':request.POST.get('past_simple'), 
						'pass_participle':request.POST.get('pass_participle')}
		
		# Стоит учесть, что тут будет передан массив в масиве
		answer_result = check_answers_irr(user_answer, content, outValues, iterator)
		if not answer_result['simple'][0]:
			content.incorrectValues.append(content.mainContent[iterator][1])

		iterator += 1
		if iterator < length:
			return render(request, 'tests\\test_modal_window.html', answer_result)
		else:
			outValues, iterator, length, content = set_global_variables()
			return render(request, 'tests\\test_modal_window.html', {'incorrectValues':content.incorrectValues})

	# Проверка существительных
	if "PLURAL_CHECK" in requestTypeList:
		user_answer = {'singular':request.POST.get('singular'), 
						'plural':request.POST.get('plural')}
		
		 # Стоит учесть, что тут будет передан массив в масиве
		answer_result = check_answers_pl(user_answer, content, iterator)
		if not answer_result['singular'][0]:
			content.incorrectValues.append(content.mainContent[iterator])
		
		iterator +=1
		if iterator < length:
			return render(request, 'tests\\test_modal_window.html', answer_result)
		else:
			outValues, iterator, length, content = set_global_variables()
			return render(request, 'tests\\test_modal_window.html', {'incorrectValues':content.incorrectValues})
