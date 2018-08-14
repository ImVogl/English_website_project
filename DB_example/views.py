# https://docs.djangoproject.com/en/dev/topics/cache/#the-low-level-cache-api
# @classmethod
# http://bionic-wrench.com/

import os

from django.shortcuts import render
from django.http.response import HttpResponse
from django.template.loader import get_template
from django.template import Context
from django.shortcuts import render_to_response
from logs.LogProccessing import write_to_log
from DB_example.data_base import get_userdata
from DB_example.utils import reset_global_variables, set_global_variables, get_content, set_content
from testes.Irregular_verbs_test import irregular_verbs_setup, check_answers_irr
from testes.Substantives_testes import plural_substantive_setup, check_answers_pl
from django.views.decorators.csrf import csrf_exempt
from testes.test_utilits import select_values
from django.core.cache import cache
from ContentClass import Content
import json

# Test page
@csrf_exempt
def index(request):
	if request.method == "POST":
		print('Method is POST')
		print(request.POST.get("content"))
		return HttpResponse(json.dumps({'data': "1"}), content_type='application/json')
	return render_to_response('index.html', {'data': "1"})


# Select test parameters page (test_modal_window.html)
@csrf_exempt
def test_page_function(request):
	# Если метод иной, то ничего не возвращаем
	if request.method != "POST":
		# Default request returned
		return render_to_response('tests\\test_modal_window.html', {"data": "empty"})

	requestTypeList = list(request.POST.keys())[-1]

	## Настройки тестов
	# Настройки для тестирования глаголов
	if "IRREGULAR_SETUP" in requestTypeList:
		content = get_content()
		content.mainContent, content.supportContent, content.isText = irregular_verbs_setup(request)
		if content.isText:
			set_global_variables(len(content.mainContent), "", 0, content)
			return HttpResponse(json.dumps({'text': content.mainContent}), content_type='application/json')
		else:
			outValues = request.POST.get('content[IRREGULAR_SETUP][outValues]')
			set_global_variables(len(content.mainContent), outValues, 0, content)
			return HttpResponse(json.dumps(select_values(content.mainContent[0], outValues)), content_type='application/json')

	# Настройки для тестирования множественного числа существительных
	if "PLURAL_SETUP" in requestTypeList:
		content = get_content()
		content.mainContent, content.supportContent = plural_substantive_setup(request)
		set_global_variables(len(content.mainContent), "", 0, content)
		return HttpResponse(json.dumps(select_values({'singular': content.mainContent[0]})), content_type='application/json')

	## Проверка коррректности введеных пользователем значений
	# Проверка глаголов
	if "IRREGULAR_CHECK" in requestTypeList:
		content = get_content()
		user_answer = {'rus': request.POST.get('content[IRREGULAR_CHECK][rus]'), 
						'simple': request.POST.get('content[IRREGULAR_CHECK][simple]'), 
						'past_simple': request.POST.get('content[IRREGULAR_CHECK][past_simple]'), 
						'pass_participle': request.POST.get('content[IRREGULAR_CHECK][pass_participle]')}

		# Стоит учесть, что тут будет передан массив в масиве
		answer_result = check_answers_irr(user_answer, content, cache.get('outValues'), cache.get('iterator'))

		if not answer_result['simple'][0]:
			content.incorrectValues.append(content.mainContent[cache.get('iterator')][1])
			set_content(content)

		cache.incr('iterator')
		if cache.get('iterator') < cache.get('length'):
			return HttpResponse(json.dumps(answer_result), content_type='application/json')
		else:
			reset_global_variables()
			return HttpResponse(json.dumps(select_values({'incorrectValues':content.incorrectValues})), content_type='application/json')

	# Проверка существительных
	if "PLURAL_CHECK" in requestTypeList:
		content = get_content()
		user_answer = {'singular':request.POST.get('singular'), 
						'plural':request.POST.get('plural')}
		
		 # Стоит учесть, что тут будет передан массив в масиве
		answer_result = check_answers_pl(user_answer, content, cache.get('iterator'))
		if not answer_result['singular'][0]:
			content.incorrectValues.append(content.mainContent[cache.get('iterator')])
			set_content(content)
		
		cache.incr('iterator')
		if cache.get('iterator') < cache.get('length'):
			return HttpResponse(json.dumps(select_values(answer_result)), content_type='application/json')
		else:
			reset_global_variables()
			return HttpResponse(json.dumps(select_values({'incorrectValues':content.incorrectValues})), content_type='application/json')
