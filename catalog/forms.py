from django import forms

from catalog.models import Product, Version


class StyleFormMixin:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != 'is_current' and field_name != 'is_published':
                field.widget.attrs['class'] = 'form-control'


class ProductForm(StyleFormMixin, forms.ModelForm):
    forbidden_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция',
                       'радар']

    class Meta:
        model = Product
        exclude = ('owner',)

    def clean_name(self):
        cleaned_data = self.cleaned_data.get('name')
        for word in self.forbidden_words:
            if word in cleaned_data:
                raise forms.ValidationError(f'Недопустимые слова {self.forbidden_words}')
        return cleaned_data

    def clean_description(self):
        cleaned_data = self.cleaned_data['description']
        for word in self.forbidden_words:
            if word in cleaned_data:
                raise forms.ValidationError(f'Недопустимые слова {self.forbidden_words}')
        return cleaned_data


class VersionForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Version
        fields = '__all__'
