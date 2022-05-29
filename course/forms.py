from .models import Order
from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class orderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'


class createUserForm(UserCreationForm):
    fullname = forms.CharField(label = "Fullname")
    linkedin =forms.CharField(label="linkedin")
    age=forms.IntegerField(label="age")
    class Meta:
        model = User
        fields=["username","email","password1","password2","fullname","linkedin","age"]
    
    def save(self, commit=True):
        user = super(createUserForm, self).save(commit=False)
        fullname= self.cleaned_data["fullname"]
        linkedin = self.cleaned_data["linkedin"]
        age=self.cleaned_data["age"]
        user.linkedin = linkedin
        user.fullname = fullname
        user.age=age
        if commit:
            user.save()
        return user


