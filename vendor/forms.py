from django import forms
from accounts.models import UserProfile
from vendor.models import *
from django_recaptcha.fields import ReCaptchaField
from accounts.validators import allow_only_images


class VendorRegistrationForm(forms.ModelForm):
    # confirm_password=forms.CharField(widget=forms.PasswordInput)
    # password=forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model=Vendor
        fields=["restaurant_name","restaurant_license"]

class VendorProfile(forms.ModelForm):
    # profile_picture = forms.FileField(validator = [allow_only_images])
    # cover_photo = forms.FileField(validator = [allow_only_images])

    latitude = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    longitude = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    class Meta:
        model = UserProfile
        fields = ["profile_picture","cover_photo","address","country","state","city","pincode","latitude","longitude"]




    # def clean(self):
    #     cleaned_data = super(VendorRegistrationForm, self).clean()
    #     password = cleaned_data.get('password')
    #     confirm_password = cleaned_data.get('confirm_password')

    #     if password != confirm_password:
    #         raise forms.ValidationError("Password does not match")

class OpeningHoursForm(forms.ModelForm):
    # vendor=forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    class Meta:
        model = Opening_Hours
        fields = ["vendor","days","open_time","close_time","is_opened"]

