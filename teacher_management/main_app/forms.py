from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import User

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = '__all__'
        exclude = ['username', 'email', '']