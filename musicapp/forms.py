from django import forms
from .models import Songs

class AddSongForm(forms.ModelForm):
    class Meta:
        model = Songs
        fields = "__all__"

