from django.contrib import admin

from .models import Tag, Idea, Comments, Likes
admin.site.register(Tag)
admin.site.register(Idea)
admin.site.register(Comments)
admin.site.register(Likes)


