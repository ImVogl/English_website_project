#!/usr/bin/env python
import os
import sys
from logs.LogProccessing import write_to_log
from datetime import datetime

if __name__ == "__main__":

	write_to_log(['Server started: ' + str(datetime.now()), ''])
	os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DB_example.settings")
	try:
		from django.core.management import execute_from_command_line
	except ImportError as exc:
		write_to_log(['Start server error:', sys.exc_info()])
		raise ImportError(
			"Couldn't import Django. Are you sure it's installed and "
			"available on your PYTHONPATH environment variable? Did you "
			"forget to activate a virtual environment?"
		) from exc
	execute_from_command_line(sys.argv)