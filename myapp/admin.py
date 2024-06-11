from django.contrib import admin
from . import models
# Register your models here.


admin.site.register(models.StickyNote)
admin.site.register(models.Replies)
admin.site.register(models.UserSuggestion)
