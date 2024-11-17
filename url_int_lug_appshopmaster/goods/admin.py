from django.contrib import admin

from goods.models import Categories, Products, ProductsImage

# admin.site.register(Categories)
# admin.site.register(Products)


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
		prepopulated_fields = {'slug': ('name',)}


class ProductsImageInline(admin.TabularInline):
		model = ProductsImage
		extra = 1  # Количество дополнительных пустых полей для новых изображений
		fields = ['image', 'is_main']

class ProductsAdmin(admin.ModelAdmin):
		inlines = [ProductsImageInline]
		list_display = ['name', 'category', 'price', 'quantity']
		prepopulated_fields = {'slug': ('name',)}

admin.site.register(Products, ProductsAdmin)

