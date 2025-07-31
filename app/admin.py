from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from .models import Category

class CategoryAdmin(DraggableMPTTAdmin):
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(Category, CategoryAdmin)