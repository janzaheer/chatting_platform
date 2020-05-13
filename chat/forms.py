from django import forms
from .models import RoomAdmin, Room


class RoomAdminForm(forms.ModelForm):
    class Meta:
        model = RoomAdmin
        fields = '__all__'

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = '__all__'

