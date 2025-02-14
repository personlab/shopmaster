from django.core.cache import cache


class CacheMixin:
		def set_get_cache(self, query, cache_name, cache_time):
				datacache = cache.get(cache_name)

				if not datacache:
						datacache = query
						cache.set(cache_name, datacache, cache_time)

						return datacache