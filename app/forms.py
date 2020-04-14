from django import forms
from django.core.validators import validate_email
from .models import Role, Users


Role.objects.all()

STATES = (
    ('', 'Choose...'),
    ('MG', 'Minas Gerais'),
    ('SP', 'Sao Paulo'),
    ('RJ', 'Rio de Janeiro')
)

class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput())

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if validate_email(email):
            raise forms.ValidationError('This not valid email')

        return email
    

class RegisterForm(forms.Form):
    firstname = forms.CharField(max_length=100)
    lastname = forms.CharField(max_length=100)
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput())
    role = forms.ModelChoiceField(
        queryset=None
    )

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['role'].queryset=Role.objects.all()

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if validate_email(email):
            raise forms.ValidationError('This not valid email')
        return email