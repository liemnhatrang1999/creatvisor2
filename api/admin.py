from django.contrib import admin


from api.models import Atelier, Competance, Info_consultant, Info_entrepreneur, Partenaire, Thematique_metier, UserAccount

@admin.register(UserAccount)
class UserAdmin(admin.ModelAdmin):
    list_display =('email','nom','prenom','phone','is_consultant')
    ordering = ('nom',)
    search_fields = ('nom',)

admin.site.register(Atelier)
admin.site.register(Info_entrepreneur)
admin.site.register(Info_consultant)
admin.site.register(Thematique_metier)
admin.site.register(Competance)
admin.site.register(Partenaire)

