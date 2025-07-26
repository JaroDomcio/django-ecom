from django import forms


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