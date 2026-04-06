from django import forms
from .models import Publication

class PublicationForm(forms.ModelForm):
    class Meta:
        model = Publication
        fields = ['title', 'short_description', 'full_text', 'image', 'status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Просто и понятно назначаем класс CSS для каждого поля
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})