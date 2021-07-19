from django import forms
from froala_editor.widgets import FroalaEditor
from .models import *

class PackageForm(forms.ModelForm):
    class Meta:
        model = CoursePackage
        fields = ['package_description']