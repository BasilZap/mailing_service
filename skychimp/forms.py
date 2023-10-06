from django import forms
from skychimp.models import MailingConfig, Client, UserMail, MailingTry


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class MailingConfigForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = MailingConfig
        exclude = ('owner',)


class ClientForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Client
        exclude = ('owner',)


class UserMailForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = UserMail
        fields = '__all__'


class MailingTryConfigForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = MailingTry
        fields = '__all__'
