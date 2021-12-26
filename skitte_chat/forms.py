from django import forms
from .models import PrivateMessageModel

class ThreadForm(forms.Form):
    username = forms.CharField(label='', max_length=50)


class MessageForm(forms.Form):
    message = forms.CharField(label='', max_length=1000)


class ThreadForm(forms.Form):
    username = forms.CharField(label='', max_length=100)


class MessageForm(forms.ModelForm):
    body = forms.CharField(label='', max_length=1000)

    image = forms.ImageField(required=False)

    class Meta:
        model = PrivateMessageModel
        fields = ['body', 'image']
