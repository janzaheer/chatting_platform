from django import forms
from .models import RoomAdmin, Room, Comment


class RoomAdminForm(forms.ModelForm):
    class Meta:
        model = RoomAdmin
        fields = '__all__'

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = '__all__'

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = '__all__'
