from django.conf import settings
from django import forms

from .models import Skit

MAX_SKIT_LENGTH = settings.MAX_SKIT_LENGTH

class SkitForm(forms.ModelForm):
    class Meta:
        model = Skit
        fields = ['content','image', 'video']
    
    def clean_content(self):
        content = self.cleaned_data.get("content")
        if len(content) > MAX_SKIT_LENGTH:
            raise forms.ValidationError("This skit is too long")
        return content