from django.contrib import admin
from . import models

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'password', 'id_card']
    list_editable = ['phone', 'password', 'id_card']
    list_per_page = 20


class LogAdmin(admin.ModelAdmin):
    list_display = ['id', 'time', 'user', 'action']
    list_per_page = 20


admin.site.register(models.User, UserAdmin)
admin.site.register(models.Log, LogAdmin)

admin.site.site_header = "JR"
admin.site.site_title = "JR_HT"
admin.site.index_title = "欢迎使用JR_HT"
