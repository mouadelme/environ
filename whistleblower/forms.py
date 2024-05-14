from django import forms
from django.core.exceptions import ValidationError
from whistleblower.models import UploadFile



class FileForm(forms.ModelForm):
    class Meta:
        model = UploadFile
        fields = ('picture', 'email', 'username', 'reason', 'company', 'public')



