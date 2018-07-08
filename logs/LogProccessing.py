# Файл с функциями для работы с логами


def write_to_log(text):
	outputText = '\r\n'.join(text)
	with open('logs\\Logfile.txt', 'a') as file:
		file.write(outputText)