from django import forms
from .models import ListRetraite, OperateRetraite

class ListRetraiteForm(forms.ModelForm):
    class Meta:
        model = ListRetraite
        fields = ['titre', 'beneficiaire', 'nni', 'date_retraite', 'ville', 'age', 'telephone']
        widgets = {
            'titre': forms.TextInput(attrs={'class': 'form-control', 'onchange': 'updateOperateRetraiteFields()'}),
            'beneficiaire': forms.TextInput(attrs={'class': 'form-control'}),
            'nni': forms.TextInput(attrs={'class': 'form-control'}),
            'date_retraite': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'ville': forms.TextInput(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control'}),
        }
        
        
        

class OperateRetraiteForm(forms.ModelForm):
    class Meta:
        model = OperateRetraite
        fields = ['Numero_titre', 'beneficiaire', 'nni', 'montant']
        widgets = {
            'beneficiaire': forms.TextInput(attrs={'readonly': 'readonly', 'class': 'form-control'}),
            'nni': forms.TextInput(attrs={'readonly': 'readonly', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(OperateRetraiteForm, self).__init__(*args, **kwargs)
        self.fields['montant'].widget.attrs['class'] = 'form-control'