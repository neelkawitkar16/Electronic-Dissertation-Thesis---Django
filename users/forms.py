from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):

  email = forms.EmailField(required=True)

  def clean_email(self):
      if CustomUser.objects.filter(email=self.cleaned_data['email']).exists():
          raise forms.ValidationError("the given email is already registered")
      return self.cleaned_data['email']

  class Meta(UserCreationForm):
    model = CustomUser
    fields = UserCreationForm.Meta.fields + ('username', 'email', 'age')
    
    
class CustomUserChangeForm(UserChangeForm):
  class Meta:
    model = CustomUser
    fields = UserChangeForm.Meta.fields