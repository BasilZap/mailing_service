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
        exclude = ('mailing_state', 'owner')

    def __init__(self, *args, **kwargs):
        """При инициализации формы добавляем фильтрацию - пользователь
        не должен видеть клиентов и сообщения, которые создавали
        другие пользователи"""
        self.current_user = kwargs.pop('user', None)
        super(MailingConfigForm, self).__init__(*args, **kwargs)
        self.fields['clients'].queryset = Client.objects.filter(
            owner=self.current_user)


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


class ModeratorMailingConfigForm(StyleFormMixin, forms.ModelForm):
    disabled_fields = ('clients', 'message', 'mailing_start_time', 'mailing_period', 'mailing_stop_time', 'owner')

    class Meta:
        model = MailingConfig
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ModeratorMailingConfigForm, self).__init__(*args, **kwargs)
        for field in self.disabled_fields:
            self.fields[field].disabled = True


