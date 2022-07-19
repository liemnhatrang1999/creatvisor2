from django.contrib import admin


from api.models import UserAccount

@admin.register(UserAccount)
class UserAdmin(admin.ModelAdmin):
    list_display =('email','nom','prenom','phone')
    ordering = ('nom',)
    search_fields = ('nom',)