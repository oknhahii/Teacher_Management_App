from django.contrib import admin
from .models import User,Class, Subject

# Register your models here.

admin.site.register(User)
admin.site.register(Class)
admin.site.register(Subject)