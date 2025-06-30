from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Wallet

class UserAdmin(UserAdmin):
		list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'image')
		fieldsets = (
				(None, {'fields': ('username', 'password')}),
				('Personal info', {'fields': ('first_name', 'last_name', 'email', 'image')}),
				('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
		)
		filter_horizontal = ('groups', 'user_permissions',)

admin.site.register(User, UserAdmin)



class WalletAdmin(admin.ModelAdmin):
		list_display = ('short_address', 'telegram_username', 'telegram_first_name', 'created_at')
		search_fields = ('address', 'telegram_username', 'telegram_first_name')
		list_filter = ('created_at',)
		readonly_fields = ('created_at', 'last_login')
		
		def short_address(self, obj):
				return f"{obj.address[:6]}...{obj.address[-4:]}"
		short_address.short_description = 'Адрес кошелька'


admin.site.register(Wallet, WalletAdmin)


# from django.contrib import admin
# from users.models import User, Wallet
# from django.contrib.auth.admin import UserAdmin



# admin.site.register(User, UserAdmin)