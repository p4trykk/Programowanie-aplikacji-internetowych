from django import forms
from .models import News
import datetime


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['topic', 'text', 'author']
