

from blog.models import Post


class Search():
	def q_search(query):
		if query.isdigit() and len(query) <= 5:
					return Post.objects.filter(query)
		return Post.objects.filter(description__search=query)