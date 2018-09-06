from django import forms


class TestForm(forms.Form):
    start_date = forms.CharField(max_length=100)
    end_date = forms.CharField(max_length=100)
