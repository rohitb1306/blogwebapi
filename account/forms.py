from django import forms
from .models import MyUser


class signupform(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = [
            "is_auther",
            "is_staff",
            "user_name",
            "first_name",
            "last_name",
            "user_email",
            "user_image",
            "password",
            
        ]
        widgets = {
            "user_name": forms.TextInput(
                attrs={"class": "form-control form-control-lg"}
            ),
            "first_name": forms.TextInput(
                attrs={"class": "form-control form-control-lg"}
            ),
            "last_name": forms.TextInput(
                attrs={"class": "form-control form-control-lg"}
            ),
            "password": forms.PasswordInput(
                attrs={"class": "form-control form-control-lg"}
            ),
            "user_email": forms.EmailInput(
                attrs={"class": "form-control form-control-lg"}
            ),
            "user_image": forms.FileInput(
                attrs={'class':'form-control form-control-lg'}
            ),
            "is_staff": forms.CheckboxInput(
                attrs={'class':'mx-2'}
            ),
            "is_auther": forms.CheckboxInput(
                attrs={'class':'mx-2'}
            ),

        }
class updateprofileform(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = [
            "is_auther",
            "is_staff",
            "user_name",
            "first_name",
            "last_name",
            "user_email",
            "user_image",
            "user_contact",
            
        ]
        widgets = {
            "user_name": forms.TextInput(
                attrs={"class": "form-control form-control-lg"}
            ),
            "first_name": forms.TextInput(
                attrs={"class": "form-control form-control-lg"}
            ),
            "last_name": forms.TextInput(
                attrs={"class": "form-control form-control-lg"}
            ),
            "user_email": forms.EmailInput(
                attrs={"class": "form-control form-control-lg"}
            ),
            "user_image": forms.FileInput(
                attrs={'class':'form-control form-control-lg'}
            ),
            "user_contact": forms.NumberInput(
                attrs={'class':'form-control form-control-lg'}
            ),
            
            "is_staff": forms.CheckboxInput(
                attrs={'class':'mx-2'}
            ),
            "is_auther": forms.CheckboxInput(
                attrs={'class':'mx-2'}
            ),

        }
