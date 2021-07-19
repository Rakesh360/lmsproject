from django.contrib import admin
from .models import *
from django.forms import CheckboxSelectMultiple


admin.site.register(Subject)
admin.site.register(SubjectChapters)
admin.site.register(Lessons)