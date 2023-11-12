from django.contrib import admin
from .models import User, Subject, Lecture

admin.site.register(User)
admin.site.register(Subject)
admin.site.register(Lecture)