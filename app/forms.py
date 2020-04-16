from django import forms
from django.core.validators import validate_email
from .models import Role, Users

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

class PlanningForm(forms.Form):
    title = forms.CharField(max_length=100)
    start = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'placeholder': 'y-m-d h:m'}))
    end = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'placeholder': 'y-m-d h:m'}))
    instructor = forms.ModelChoiceField(
        queryset=None
    )
    student = forms.ModelChoiceField(
        queryset=None
    )
     
    def __init__(self, user, *args, **kwargs):
        super(PlanningForm, self).__init__(*args, **kwargs)
        print(user)
        if user.role.id == 2:
            self.fields['instructor'].queryset = Users.objects.filter(id=user.id)
        else:
            self.fields['instructor'].queryset = Users.objects.filter(role="2")
        if user.role.id == 1:
            self.fields['student'].queryset = Users.objects.filter(id=user.id)
        else:
            self.fields['student'].queryset = Users.objects.filter(role="1")


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ['firstname', 'lastname', 'email', "role"]

        firstname = forms.CharField(max_length=100)
        lastname = forms.CharField(max_length=100)
        email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Email'}))
        password = forms.CharField(widget=forms.PasswordInput(), required=False)
        role = forms.ModelChoiceField(
            queryset=None
        )

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['role'].queryset=Role.objects.all() 