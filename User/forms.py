from django import forms
from .models import UserAcc, userProfile


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder' : "Enter Password",
        'class': 'form-control'
    }))
    repeat_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder' : "Re-enter Password"
    }))
    class Meta:
        model = UserAcc
        fields = ['first_name','last_name','email','phone_number']


    def __init__(self,*args, **kwargs):
        super(RegistrationForm,self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'

    

    def clean(self):
        cleaned_data = super(RegistrationForm,self).clean()
        password = cleaned_data.get('password')
        repeat_password = cleaned_data.get('repeat_password')

        if password != repeat_password:
            raise forms.ValidationError("Password doesnot match!")


class UserForm(forms.ModelForm):
    class Meta:
        model = UserAcc
        fields = ['first_name','last_name','phone_number']

    def __init__(self,*args, **kwargs):
        super(UserForm,self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'

class UserProfileform(forms.ModelForm):
    profile_picture = forms.ImageField(required=False,error_messages={'invalid':("Image files only")},widget=forms.FileInput)
    class Meta:
        model = userProfile
        fields = ['address_line_1','address_line_2','profile_picture','city','state','country']

    def __init__(self,*args, **kwargs):
        super(UserProfileform,self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'


