from django import forms
from .models import csvfile
class file_class(forms.ModelForm):
    #title = forms.CharField(max_length=50)
    file = forms.FileField()
    class Meta:
        model = csvfile
        fields = ('req_file',)
