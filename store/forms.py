from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import  UserCreationForm

class LoginForm(forms.Form):
    username = forms.CharField(
        label = "Nazwa uzytkownika",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Podaj nazwę użytkownika',
            'autocomplete': 'username',
            'autofocus': True,
        }))
    password = forms.CharField(
        label="Haslo",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Podaj hasło',
            'autocomplete': 'current-password',
        })
    )

class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Hasło",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Podaj hasło'
        }),
        help_text="Hasło musi mieć co najmniej 8 znaków."
    )
    password2 = forms.CharField(
        label="Powtórz hasło",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Powtórz hasło'
        }),
        help_text="Wprowadź ponownie to samo hasło dla potwierdzenia."
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nazwa użytkownika'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Imię'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nazwisko'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Adres e-mail'
            }),
        }
        labels = {
            'username': 'Nazwa użytkownika',
            'first_name': 'Imię',
            'last_name': 'Nazwisko',
            'email': 'E-mail',
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Hasła nie są identyczne.")
        if password1 and len(password1) < 8:
            raise forms.ValidationError("Hasło musi mieć co najmniej 8 znaków.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user