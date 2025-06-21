# leader_portal/forms.py

from django import forms
from main.forms import ClubForm  # существующая форма для редактирования клуба
from main.models import Club
from .models import Material


class LeaderClubForm(ClubForm):
    class Meta(ClubForm.Meta):
        model = Club
        fields = [
            "name", "slug", "short_description", "description",
            "logo", "schedule", "location", "leader_name", "leader_contact"
        ]


class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ["title", "file"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "file": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }
