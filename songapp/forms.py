  
from django import forms
from .models import Songs


class playlistForm(forms.Form):
    playlistname = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'new playlist', 'class': 'form-control'}))
    song = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))


class AddSongForm(forms.ModelForm):
    class Meta:
        model = Songs
        fields = "__all__"



