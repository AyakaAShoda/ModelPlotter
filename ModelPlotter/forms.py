
from django import forms
import os
from django.core.files.storage import default_storage

VALID_EXTENSIONS = ['.xml']

class UploadFileForm(forms.Form):
    file = forms.FileField()
    def clean_file(self):
        file = self.cleaned_data['file']
        extension = os.path.splitext(file.name)[1] # 拡張子を取得
        if not extension.lower() in VALID_EXTENSIONS:
            raise forms.ValidationError('Choose xml file')