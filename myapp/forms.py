from django import forms
from .models import Notes,homework,Todo
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class NotesForm(forms.ModelForm):
    class Meta:
        model = Notes
        fields = ['title','description']
        widgets = {
            # 'user': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class DateInput(forms.DateInput):
    input_type = 'date'

class homeworkForm(forms.ModelForm):
    class Meta:
        model = homework
        widgets = {'due':DateInput()}
        widgets = {
            # 'user': forms.Select(attrs={'class': 'form-control'}),
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'due': DateInput(attrs={'class': 'form-control'}),
            # 'is_finished': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        fields = ['subject','title','description','due','is_finished']


class DashboardForm(forms.Form):
    text = forms.CharField(max_length=100,label='Enter Your Search:',  widget=forms.TextInput(attrs={'class': 'form-control'}))


class todoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title','is_finished']
        widgets = {
            # 'user':forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            # 'is_finished': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class ConversionForm(forms.Form):
    CHOICES = [('length','Length'),('mass','Mass')]
    measurement = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)


class ConversionLength(forms.Form):
    CHOICES = [('yard','Yard'),('foot','Foot')]    
    input = forms.CharField(required=False,label=False,widget=forms.TextInput(
        attrs={'type':'number','placeholder':'Enter your number : ','class':'form-control mt-1'}
    ))
    measure1 = forms.CharField(label='',widget=forms.Select(attrs={'class':'form-select mt-3 p-2 text-success w-50'}, choices=CHOICES))
    measure2 = forms.CharField(label='',widget=forms.Select(attrs={'class':'form-select mt-3 p-2 text-success w-50'}, choices=CHOICES))


class ConversionMassForm(forms.Form):
    CHOICES = [('pound', 'Pound'), ('kilogram', 'Kilogram')]    
    input = forms.CharField(
        required=False,
        label=False,
        widget=forms.TextInput(attrs={
            'type': 'number',
            'placeholder': 'Enter your number : ',
            'class': 'form-control mt-1',
        })
    )
    measure1 = forms.CharField(
        label='',
        widget=forms.Select(attrs={
            'class': 'form-select mt-3 p-2',
        }, choices=CHOICES)
    )
    measure2 = forms.CharField(
        label='',
        widget=forms.Select(attrs={
            'class': 'form-select mt-3 p-2',  
        }, choices=CHOICES)
    )






class UserRegistrtionForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','password1','password2']    