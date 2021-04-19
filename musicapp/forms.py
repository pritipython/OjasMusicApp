from django import forms
from .models import GeethUsers, Songs, Playlist
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate


class PlaylistForm(forms.ModelForm):
    class Meta:
        model = Playlist
        fields = '__all__'


class GeethUsersForm(forms.ModelForm):
    class Meta:
        model = GeethUsers
        fields = ['user', 'name', 'email', 'phoneno', 'profile_pic']

    def __init__(self, *args, **kwargs):
        super(GeethUsersForm, self).__init__(*args, **kwargs)
        self.fields['user'].disabled = True
        self.fields['user'].label = "username"


class UserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter Username', 'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password',
                                                                 'class': 'form-control'}))

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("This user does not exist!")
            if not user.check_password(password):
                raise forms.ValidationError("Incorrect password!")
            if not user.is_active:
                raise forms.ValidationError("This user is not active")
        return super(UserLoginForm, self).clean(*args, **kwargs)


class RegistrationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Email-Id',
                                                           'class': 'form-control'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password',
                                                                 'class': 'form-control'}))
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Re Enter Password', 'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', ]

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        if commit:
            user.save()
        return user

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = ""
        self.fields['email'].label = ""
        self.fields['password1'].label = ""
        self.fields['password2'].label = ""