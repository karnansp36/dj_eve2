from django.contrib import admin
from .models import User_post, Comments
# Register your models here.

class User_postAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'image')
    list_filter = ('title', 'description')
    search_fields = ('title', 'description')

admin.site.register(User_post, User_postAdmin)