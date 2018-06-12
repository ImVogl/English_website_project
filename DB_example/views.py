from django.shortcuts import render
from django.http.response import HttpResponse
from django.template.loader import get_template
from django.template import Context
from django.shortcuts import render_to_response
from .write_to_log import printLog
from .data_base import get_userdata
from testes.irregulat_verbs_test import test_ir, get_text, check_verbs


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

# Testing page (test_verbs.html)
def send_to_page_verb(verbs, num):
	input_index = ['rus', 'inf', 'simple', 'participle']
	user_input = ['']*4
	return render(request, 'test_verbs.html', {'group': VERBS[0]})	# Отправить нужно только часть глаголов в зависимости от
	i = 0															# выбранной сложности VERBS[i][?] - один случайный/русский/руский и инфинитив
	while (i < num) and request.method == "POST":
		j = 0
		for dat in input_index:
			user_input[i] = request.POST.get(dat)
			j += 1
		check_v = check_verbs(user_input, VERBS[i])
		i + = 1
		return render(request, 'test_verbs.html', {'group': VERBS[i + 1]}) # Отправить нужно только часть глаголов в зависимости от выбранной сложности VERBS[i][?]
	# Тест окнчен, нужно вывести результаты

# Select test parameters page (test_verbs.html)
def test(request):
	if request.method == "POST":
		type_test = "test"
		oft = "oft_1"
		num = 0
		VERBS = []
		type_test = request.POST.get('type_test')
		oft = request.POST.get('oft')
		num = int(request.POST.get('num'))
		if oft == 'oft':
			if num < 50:
				oft = 'oft_1'
			elif num > 80:
				oft = 'oft_3'
			else:
				oft = 'oft_2'
		VERBS = test_ir(oft, num)
		if type_test == 'text':
			sentences, verbs_from_table = get_text(VERBS, int(0.5*len(VERBS))) # verbs_from_table - нужна для проверки корректности ввода пользователем данных
			return render(request, 'test_verbs.html', {'text': sentences})
		else:
			send_to_page_verb(VERBS, num)