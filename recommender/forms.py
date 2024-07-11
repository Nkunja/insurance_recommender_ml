from django import forms
from .models import Customer

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['age', 'income', 'credit_score', 'gender', 'occupation', 'marital_status', 'number_of_dependents']
        # credit score should come from model