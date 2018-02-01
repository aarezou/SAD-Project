from django import forms


class RequestForm(forms.Form):
    type = forms.CharField(label='type', max_length=100)
