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
import json
from django.views.decorators.csrf import csrf_exempt

# Глобальные переменные
outValues = None
iterator = 0
length = 0
content = content()

def set_global_variables():
	return None, 0, 0, content()

# Test page
@csrf_exempt
def index(request):
	if request.method == "POST":
		print('Method is POST')
		print(request.POST.get("content"))
		return HttpResponse(json.dumps({'data': "1"}), content_type='application/json')
	return render_to_response('index.html', {'data': "1"})

# Select test parameters page (test_modal_window.html)
def test_page_function(request):
	global content, outValues, iterator, length
	
	# Если метод иной, то ничего не возвращаем
	if request.method != "POST":
		# Default request returned
		return HttpResponse(json.dumps({}), content_type='application/json')

	requestTypeList = list(request.POST.keys())

	## Настройки тестов
	# Настройки для тестирования глаголов
	if "IRREGULAR_SETUP" in requestTypeList:
		content.mainContent, content.supportContent, content.isText = irregular_verbs_setup(request)
		if content.isText:
			length = len(content.supportContent)
			return HttpResponse(json.dumps({'text': content.mainContent}), content_type='application/json')
		else:
			length = len(content.mainContent)
			outValues = request.POST.get('outValues')
			return HttpResponse(json.dumps(select_values(content.mainContent[0], outValues)), content_type='application/json')

	# Настройки для тестирования множественного числа существительных
	if "PLURAL_SETUP" in requestTypeList:
		content.mainContent, content.supportContent = plural_substantive_setup(request)
		length = len(content.mainContent)
		return HttpResponse(json.dumps(select_values({'singular': content.mainContent[0]})), content_type='application/json')

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
			return HttpResponse(json.dumps(answer_result), content_type='application/json')
		else:
			outValues, iterator, length, content = set_global_variables()
			return HttpResponse(json.dumps(select_values({'incorrectValues':content.incorrectValues})), content_type='application/json')

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
			return HttpResponse(json.dumps(select_values(answer_result)), content_type='application/json')
		else:
			outValues, iterator, length, content = set_global_variables()
			return HttpResponse(json.dumps(select_values({'incorrectValues':content.incorrectValues})), content_type='application/json')
