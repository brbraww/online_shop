from django import forms
from .models import Order


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'city', 'adress', 'postal_code']
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'adress': 'Адрес',
            'postal_code': 'Почтовый индекс',
            'city': 'Город'
        }