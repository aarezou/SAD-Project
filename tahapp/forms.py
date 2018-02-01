from django import forms


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()
    rememberme = forms.BooleanField()


class RegisterForm(forms.Form):
    email = forms.EmailField()
    username = forms.CharField()
    password = forms.CharField()
    type = forms.RadioSelect()