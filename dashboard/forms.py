from django import forms
from django.db.models import fields
from django.forms import widgets
from .models import *
from django.contrib.auth.forms import *

class NotesForm(forms.ModelForm):
    class Meta:
        model = Notes
        fields = ['title','description']


class DateInput(forms.DateInput):
    input_type = 'date'


class HomeWorkForm(forms.ModelForm):
    class Meta:
        model = Homework
        widgets = {'due':DateInput()}
        fields = ['subject','title','description','due','finished']


class DashboardForm(forms.Form):
    text = forms.CharField(max_length=255,label = "Ma'lumot kiriting ")


class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title','finished']


class ConversionForm(forms.Form):
    CHOICES = [
        ('lenght','Uzunlik'),
        ('mass','Massa'),
    ]
    Process= forms.ChoiceField(choices= CHOICES, widget=forms.RadioSelect)

class ConversionLenghtForm(forms.Form):
    CHOICES = [
        ('yard','Yard'),
        ('foot','Foot'),
    ]
    input = forms.CharField(required=False,label=False,widget=forms.TextInput(
        attrs = {
            'type':'number',
            'placeholder':"Enter the Number"
        }
    ))
    measure1 = forms.CharField(
        label='',widget=forms.Select(choices=CHOICES)
    )
    measure2 = forms.CharField(
        label='',widget=forms.Select(choices=CHOICES)
    )


class ConversionMasstForm(forms.Form):
    CHOICES = [
        ('pound','Pound'),
        ('kilogram','Kilogram'),
    ]
    input = forms.CharField(required=False,label=False,widget=forms.TextInput(
        attrs = {
            'type':'number',
            'placeholder':"Enter the Number"
        }
    ))  
    measure1 = forms.CharField(
        label='',widget=forms.Select(choices=CHOICES)
    )
    measure2 = forms.CharField(
        label='',widget=forms.Select(choices=CHOICES)
    )



class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password1']