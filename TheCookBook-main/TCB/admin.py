from django.contrib import admin
from .models import Recipe, Report, Cuisine, Category, Comment
# Register your models here.

# admin.site.register(Users)
admin.site.register(Recipe)
admin.site.register(Report)
admin.site.register(Cuisine)
admin.site.register(Category)
admin.site.register(Comment)