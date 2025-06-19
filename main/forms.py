# main/forms.py

from django import forms
from .models import Category, Club, News, Application


class ContactForm(forms.Form):
    """Форма обратной связи на странице Контакты."""
    name = forms.CharField(
        label="Ваше имя",
        max_length=100,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Введите ваше имя"
        })
    )
    email = forms.EmailField(
        label="E-mail",
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "you@example.com"
        })
    )
    message = forms.CharField(
        label="Сообщение",
        widget=forms.Textarea(attrs={
            "class": "form-control",
            "rows": 5,
            "placeholder": "Текст вашего сообщения"
        })
    )


class CategoryForm(forms.ModelForm):
    """CRUD-форма для работы с категориями кружков."""

    class Meta:
        model = Category
        fields = ["name", "slug"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "slug": forms.TextInput(attrs={"class": "form-control"}),
        }


class ClubForm(forms.ModelForm):
    """CRUD-форма для создания и редактирования кружков/студий."""

    class Meta:
        model = Club
        fields = [
            "name",
            "slug",
            "short_description",
            "description",
            "logo",
            "categories",
        ]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "slug": forms.TextInput(attrs={"class": "form-control"}),
            "short_description": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "logo": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "categories": forms.CheckboxSelectMultiple(),
        }


class NewsForm(forms.ModelForm):
    """Форма для создания/редактирования новостей и событий."""

    class Meta:
        model = News
        fields = [
            "title",
            "slug",
            "content",
            "category",
            "is_approved",
            "published_at",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "slug": forms.TextInput(attrs={"class": "form-control"}),
            "content": forms.Textarea(attrs={"class": "form-control", "rows": 6}),
            "category": forms.Select(attrs={"class": "form-select"}),
            "is_approved": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "published_at": forms.DateTimeInput(attrs={"class": "form-control", "type": "datetime-local"}),
        }


class ApplicationForm(forms.ModelForm):
    """Форма подачи заявки на вступление в кружок/студию."""

    class Meta:
        model = Application
        fields = [
            "club",
            "name",
            "email",
            "message",
        ]
        widgets = {
            "club": forms.Select(attrs={"class": "form-select"}),
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "message": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
        }
