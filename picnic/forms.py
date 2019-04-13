from django.contrib.auth.models import User
from django.contrib.admin.widgets import AdminDateWidget
from django import forms
from django.core.exceptions import ValidationError
from .models import Profile, Item, List
import datetime
from django.forms.extras.widgets import SelectDateWidget

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.CharField(max_length=75, required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=50, required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password', 'email']


class ProfileForm(forms.ModelForm):
    picture = forms.FileField()

    class Meta:
        model = Profile
        fields = ['picture']


class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']

class ItemForm(forms.ModelForm):
    name = forms.CharField(max_length=75, required=True)
    price = forms.DecimalField(max_digits=4, decimal_places=2)

    class Meta:
        model = Item
        fields = ['name', 'price', 'picture']

    def clean_name(self):
        name = self.cleaned_data['name']
        name = name.title()
        return name

    def clean_price(self):
        price = self.cleaned_data['price']
        if price <= 00.00:
            raise ValidationError("Price must be positive")

        return price


class ListForm(forms.ModelForm):
    # A custom empty label with string
    deadline = forms.DateField(widget=SelectDateWidget(empty_label="Nothing", ))
    admin = forms.ModelChoiceField(queryset=Profile.objects.all(), empty_label=None)

    class Meta:
        model = List
        fields = ['admin', 'deadline']

    # Add validity sometime (date > now)

    def __init__(self, *args, **kwargs):
        super(ListForm, self).__init__(*args, **kwargs)
        self.fields['admin'].label = "Wie bestelt er?"
        self.fields['deadline'].label = "Wanneer wordt er besteld?"