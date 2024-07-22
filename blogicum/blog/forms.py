from django import forms
from .models import Post
from django.utils import timezone

from django.core.mail import send_mail

from .models import Post


class PostForm(forms.ModelForm):
    """Форма публикации."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['pub_date'].initial = timezone.localtime(
            timezone.now()
        ).strftime('%Y-%m-%dT%H:%M')

    class Meta:
        model = Post
        fields = ('title', 'text', 'image', 'location', 'category', 'pub_date')
        widgets = {
            'pub_date': forms.DateTimeInput(
                format='%Y-%m-%dT%H:%M', attrs={'type': 'datetime-local'})
        }




'''from django import forms

from django.core.exceptions import ValidationError

from django.core.mail import send_mail

from .models import Birthday, Congratulation

from .validators import real_age

BEATLES = {'Джон Леннон', 'Пол Маккартни', 'Джордж Харрисон', 'Ринго Старр'}


class BirthdayForm(forms.ModelForm):
    class Meta:
        model = Birthday
        exclude = ('author',)
        fields = '__all__'
        widgets = {
            'birthday': forms.DateInput(attrs={'type': 'date'},)
        }
        validators = [
            real_age,
        ]

    def clean_first_name(self):
        # Получаем значение имени из словаря очищенных данных.
        first_name = self.cleaned_data['first_name']
        # Разбиваем полученную строку по пробелам
        # и возвращаем только первое имя.
        return first_name.split()[0]

    def clean(self):
        super().clean()
        # Получаем имя и фамилию из очищенных полей формы.
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']
        # Проверяем вхождение сочетания имени и фамилии во множество имён.
        if f'{first_name} {last_name}' in BEATLES:

            send_mail(
                subject='Another Beatles member',
                message=f'{first_name} {last_name} пытался опубликовать запись!',
                from_email='birthday_form@acme.not',
                recipient_list=['admin@acme.not'],
                fail_silently=True,
            )
            raise ValidationError(
                'Мы тоже любим Битлз, но введите, пожалуйста, настоящее имя!'
            )


class CongratulationForm(forms.ModelForm):

    class Meta:
        model = Congratulation
        fields = ('text',)'''
