from django import forms
from django.core.exceptions import ValidationError
from .models import Product

FORBIDDEN_WORDS = [
    'казино', 'криптовалюта', 'крипта', 'биржа',
    'дешево', 'бесплатно', 'обман', 'полиция', 'радар'
]


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'image', 'category', 'price', 'is_published']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'image': forms.FileInput(),
            # Стилизация для checkbox через виджет
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'is_published': 'Опубликовать продукт',
        }
        help_texts = {
            'is_published': 'Если снято, продукт не будет отображаться в общем каталоге',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Стилизация всех полей
        for field_name, field in self.fields.items():
            if field_name != 'is_published':  # Чекбокс стилизуем отдельно
                field.widget.attrs.update({
                    'class': 'form-control',
                    'style': 'margin-bottom: 15px;'
                })

        # Отдельная стилизация для checkbox
        if 'is_published' in self.fields:
            self.fields['is_published'].widget.attrs.update({
                'class': 'form-check-input',
                'style': 'width: auto; margin-right: 10px;'
            })

    def clean_name(self):
        """Валидация названия на запрещенные слова"""
        name = self.cleaned_data.get('name', '').lower()

        for word in FORBIDDEN_WORDS:
            if word in name:
                raise ValidationError(
                    f'Название содержит запрещенное слово: "{word}". '
                    f'Использование слова "{word}" недопустимо.'
                )
        return self.cleaned_data['name']

    def clean_description(self):
        """Валидация описания на запрещенные слова"""
        description = self.cleaned_data.get('description', '')

        # Если описание не указано - пропускаем проверку
        if not description:
            return description

        # Приводим к нижнему регистру для проверки
        description_lower = description.lower()

        for word in FORBIDDEN_WORDS:
            if word in description_lower:
                raise ValidationError(
                    f'Описание содержит запрещенное слово: "{word}". '
                    f'Использование слова "{word}" недопустимо.'
                )
        return description

    def clean_price(self):
        """Валидация цены (не может быть отрицательной)"""
        price = self.cleaned_data.get('price')
        if price is not None and price < 0:
            raise ValidationError('Цена не может быть отрицательной!')
        return price
