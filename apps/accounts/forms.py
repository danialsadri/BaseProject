from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import UserModel


class UserCreationForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ['phone_number', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(label='پسورد', help_text='شما میتوانید پسورد را با <a href=\'../password/\'>این فرم</a> تغییر بدهید')

    class Meta:
        model = UserModel
        fields = ['phone_number', 'password']
