__author__ = 'shrey'
from work.models import Work
from django import forms
class Searchform(forms.Form):
    project_name = forms.CharField(max_length = 100,required=False)
    #pr_code = forms.CharField(max_length = 100,required=False)
    project_agency = forms.CharField(max_length = 100,required=False)

class Addworkform(forms.ModelForm):
    class Meta:
        model = Work


class DocumentForm(forms.Form):
    docfile = forms.ImageField(
        label='Select an image',
    )
