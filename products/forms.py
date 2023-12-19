from django import forms
from products.models import Client

class ClientForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = Client
        fields = ['phone_number', 'address']

    def save(self, commit=True):
        client = super(ClientForm, self).save(commit=False)

        client.user.first_name = self.cleaned_data['first_name']
        client.user.last_name = self.cleaned_data['last_name']
        client.user.save()

        if commit:
            client.save()

        return client
