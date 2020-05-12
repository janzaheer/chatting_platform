from django import forms
from .models import RoomAdmin


class RoomAdminForm(forms.ModelForm):
    class Meta:
        model = RoomAdmin
        fields = '__all__'
