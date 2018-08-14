from ContentClass import Content
from django.core.cache import cache

def reset_global_variables():
	cache.set("iterator", 0)
	cache.set('length', 0)
	cache.set('outValues', "")
	cache.set('contentMainContent', None)
	cache.set('contentSupportContent', None)
	cache.set('contentIsText', None)
	cache.set('contentIncorrectValues', [])

def set_global_variables(length, outValues, iterator, content):
	cache.set("iterator", iterator)
	cache.set('length', length)
	cache.set('outValues', outValues)
	cache.set('contentMainContent', content.mainContent)
	cache.set('contentSupportContent', content.supportContent)
	cache.set('contentIsText', content.isText)
	cache.set('contentIncorrectValues', content.incorrectValues)

def get_content():
	content = Content()
	content.mainContent = cache.get('contentMainContent')
	content.supportContent = cache.get('contentSupportContent')
	content.isText = cache.get('contentIsText')
	content.incorrectValues = cache.get('contentIncorrectValues')
	return content

def set_content(content):
	cache.set('contentMainContent', content.mainContent)
	cache.set('contentSupportContent', content.supportContent)
	cache.set('contentIsText', content.isText)
	cache.set('contentIncorrectValues', content.incorrectValues)