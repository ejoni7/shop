from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)


class SendInfoForm(forms.Form):
    address = forms.CharField(max_length=100)
