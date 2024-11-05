from atexit import register
from django import template

from goods.models import Categories



register = template.Library()

@register.simple_tag()
def tag_categories():
		return Categories.objects.all()


# Cоздание класса для тега

# register = template.Library()

# class TagCategoryes(template.Node):
# 	def render(self, context):
# 		categories = Categories.objects.all()
# 		context['categories'] = categories
# 		return ''
	

# @register.simple_tag(takes_context=True)
# def tag_categories(context):
# 	return TagCategoryes().render(context)