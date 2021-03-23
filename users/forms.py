from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=100, label='First Name')
    first_name = forms.CharField(max_length=100, label='Last Name')
    
    def clean(self):
        cd = self.cleaned_data
        if cd.get('password1') != cd.get('password2'):
            self.add_error(error="Passwords do not match !", field="password1")
        return cd
    
    class Meta:
        model = User
        fields = ['first_name','last_name','username', 'email', 'password1', 'password2']