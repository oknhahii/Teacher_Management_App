from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import User, Class

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = '__all__'
        exclude = ['username', 'email']


class ClassForm(ModelForm):
    class Meta:
        model = Class
        fields = '__all__'
        exclude = ['teacher']