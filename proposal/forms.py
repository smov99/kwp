from django import forms


class VerificationForm(forms.Form):
    email = forms.EmailField(max_length=50)
