from django import forms
from .models import UserProfile


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = '__all__'

    def save(self, commit=True):
        self.cleaned_data = dict(
            [(k, v) for k, v in self.cleaned_data.items() if v != ""])
        return super(UserProfileForm, self).save(commit=commit)
