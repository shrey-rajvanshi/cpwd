__author__ = 'shrey'
from work.models import Work
from django import forms
from django.forms.fields import *
from django.forms.widgets import *
from django.forms.extras.widgets import *
class Searchform(forms.Form):
    project_name = forms.CharField(max_length = 100,required=False)
    #pr_code = forms.CharField(max_length = 100,required=False)
    project_agency = forms.CharField(max_length = 100,required=False)

class Addworkform(forms.ModelForm):
    class Meta:
        model = Work

    def __init__(self, *args, **kwargs):
        super(Addworkform, self).__init__(*args, **kwargs)
        self.fields['pe_date']=DateField(input_formats=['%d/%m/%Y','%Y-%m-%d',],required=False)
        self.fields['nit_date']=DateField(input_formats=['%d/%m/%Y','%Y-%m-%d',],required=False)
        self.fields['ts_date']=DateField(input_formats=['%d/%m/%Y','%Y-%m-%d',],required=False)
        self.fields['date_start']=DateField(input_formats=['%d/%m/%Y','%Y-%m-%d',],required=False)
        self.fields['stipulated_date']=DateField(input_formats=['%d/%m/%Y','%Y-%m-%d',],required=False)
        self.fields['actual_date']=DateField(input_formats=['%d/%m/%Y','%Y-%m-%d',],required=False)


class DocumentForm(forms.Form):
    docfile = forms.ImageField(
        label='Select an image',
    )
