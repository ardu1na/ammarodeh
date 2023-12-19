from django import forms
from django.contrib.auth.models import User
from products.models import Client

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['phone_number', 'address']

    first_name = forms.CharField(max_length=30, required=True, label='Nombre')
    last_name = forms.CharField(max_length=30, required=True, label='Apellido')
    email = forms.EmailField(max_length=254, required=True, label='Correo electrónico')


    def __init__(self, *args, **kwargs):
        super(ClientForm, self).__init__(*args, **kwargs)
        self.fields['phone_number'].label = 'Número de teléfono'
        self.fields['address'].label = 'Dirección'

        
    def save(self, commit=True):
        client = super(ClientForm, self).save(commit=False)
        client.user.first_name = self.cleaned_data['first_name']
        client.user.last_name = self.cleaned_data['last_name']
        client.user.email = self.cleaned_data['email']
        if commit:
            client.user.save()
            client.save()


