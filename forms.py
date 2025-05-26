from django import forms
from django.contrib.auth.models import User
from .models import Email

class EmailForm(forms.ModelForm):
    sender = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput())
    recipients = forms.ModelMultipleChoiceField(queryset=User.objects.all())
    subject = forms.CharField(max_length=255)
    body = forms.CharField(widget=forms.Textarea)
    attachments = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)

    class Meta:
        model = Email
        fields = ['recipients', 'subject', 'body']

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())  # Added parentheses
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
