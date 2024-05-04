from django import forms
from django.contrib.auth.models import User
from . import models
import re
from django.forms import ModelForm, DateInput

class EventForm(ModelForm):
  class Meta:
    model = models.Event
    # datetime-local is a HTML5 input type, format to make date time show on fields
    widgets = {
      'start_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
      'end_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
    }
    fields = ['title','description','start_time','end_time']

  def __init__(self, *args, **kwargs):
    super(EventForm, self).__init__(*args, **kwargs)
    # input_formats parses HTML5 datetime-local input to datetime field
    self.fields['start_time'].input_formats = ('%Y-%m-%dT%H:%M',)
    self.fields['end_time'].input_formats = ('%Y-%m-%dT%H:%M',)


class RegistrationForm(forms.Form):
    username = forms.CharField(label='Username', max_length=25)
    email = forms.EmailField(label='Email')
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput())

    def clean_password2(self):
        if 'password1' in self.cleaned_data:
            password1 = self.cleaned_data['password1']
            password2 = self.cleaned_data['password2']
            if password1 == password2 and password1:
                return password2
        raise forms.ValidationError("Password does not match")

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError("Username already taken")

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        if username:
            if not re.match("^[a-zA-Z0-9_]*$", username):
                raise forms.ValidationError("Username cannot contain special letters (~,!@#$%^&*-+/<>\|{}[]`) ")

    def save(self):
        User.objects.create_user(username=self.cleaned_data['username'], email=self.cleaned_data['email'], password=self.cleaned_data['password1'])
class doctorForm(forms.ModelForm):
    class Meta:
        model=models.Doctor
        fields=['address','mobile','profile_pic','desc']
    class Media:
        js = ('/media/tinymce/jscripts/tiny_mce/tiny_mce.js',
                '',)

class patientForm(forms.ModelForm):
    class Meta:
        model=models.Patient
        fields=['mobile','profile_pic','desc']
