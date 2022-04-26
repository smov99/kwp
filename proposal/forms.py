from django import forms
from prettyjson import PrettyJSONWidget

from proposal.models import ErrorLog


class ErrorLogForm(forms.ModelForm):
    class Meta:
        model = ErrorLog
        fields = "__all__"
        widgets = {"data": PrettyJSONWidget()}


class VerificationForm(forms.Form):
    email = forms.EmailField(max_length=50)
