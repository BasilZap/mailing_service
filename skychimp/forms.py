from django import forms
from skychimp.models import MailingConfig


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class MailingConfigForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = MailingConfig
        fields = '__all__'

