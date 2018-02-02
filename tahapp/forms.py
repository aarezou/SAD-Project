from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label='label username', max_length='100')
    password = forms.CharField(label='label_password', max_length='100')
    rememberme = forms.BooleanField(initial=False, required=False)


class RegisterForm(forms.Form):
    email = forms.EmailField(max_length='100')
    username = forms.CharField(max_length='100')
    password = forms.CharField(max_length='100')
    #role = forms.ChoiceField()