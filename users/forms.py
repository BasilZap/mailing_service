from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from users.models import User
from django import forms
from skychimp.forms import StyleFormMixin


class UserRegisterForm(StyleFormMixin, UserCreationForm):

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')


class UserForm(StyleFormMixin, UserChangeForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'avatar')

    def __int__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password'].widget = forms.HiddenInput()
