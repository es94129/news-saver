from django.contrib import admin
from blog.models import News, Word

#admin.site.register(News)
class NewsAdmin(admin.ModelAdmin):
	list_display = ('title', 'date')

admin.site.register(News, NewsAdmin)

admin.site.register(Word)