from django.contrib import admin
from .models import *

# admin.site.register(Post)
@admin.register(Notes)
class NotesAdmin(admin.ModelAdmin):
    list_display = ['id','user','title','description']
    list_filter = ['id','user','title','description']
    search_fields = ['id','user','title','description']

@admin.register(Homework)
class HomeworkAdmin(admin.ModelAdmin):
    list_display = ['id','user','title','description']
    list_filter = ['id','user','title','description','due','finished']
    search_fields = ['id','user','title','description','due','finished']

@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ['id','user','title','finished']
    list_filter = ['id','user','title','finished']
    search_fields = ['id','user','title','finished']

