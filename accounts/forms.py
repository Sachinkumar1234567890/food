from django import forms
from accounts.models import User,UserProfile
from django_recaptcha.fields import ReCaptchaField


class UserRegistrationForm(forms.ModelForm):
    confirm_password=forms.CharField(widget=forms.PasswordInput)
    password=forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model=User
        fields=["first_name","last_name","username","email","password"]

    def clean(self):
        cleaned_data = super(UserRegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("Password does not match")

