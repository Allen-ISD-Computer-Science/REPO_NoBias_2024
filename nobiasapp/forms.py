from django import forms
from .models import Link, Text

class SubmitLinkForm(forms.ModelForm):
    class Meta:
        model = Link
        fields = ['link']
        widgets = {
            'link': forms.URLInput(attrs={'style': 'width: 100%; padding: 10px; margin-bottom: 10px; border: 1px solid #ccc; border-radius: 5px; box-sizing: border-box;'}),
        }
class SubmitTextBoxForm(forms.ModelForm):
    class Meta:
        model = Text
        fields = ['text']
        widgets = {
            'text': forms.TextInput(attrs={'style': 'width: 100%; padding: 10px; margin-bottom: 10px; border: 1px solid #ccc; border-radius: 5px; box-sizing: border-box;'}),
        }