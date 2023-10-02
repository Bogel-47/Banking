from django import forms
from .models import CustomUser, Customer, Transaction, User
from django.forms.widgets import DateInput
from django.contrib.auth.forms import AuthenticationForm

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['account_id', 'name']

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['account', 'transaction_date', 'description', 'debit_credit_status', 'amount']
        widgets = {
            'transaction_date': DateInput(attrs={'type': 'date'}),
        }

class CustomUserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['username', 'password']

class RegistrationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Konfirmasi Password', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone_number', 'address', 'agency')

    def clean_password2(self):
        # Periksa apakah kedua kata sandi yang dimasukkan cocok
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Kata sandi tidak cocok')
        return password2

    def save(self, commit=True):
        # Simpan pengguna dengan kata sandi yang dienkripsi
        user = super(RegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user
    
class ExcelUploadForm(forms.Form):
    excel_file = forms.FileField(label='Pilih file Excel')    
