from django import forms
from authentication.models import User


class LoginForm(forms.Form):
    """Form to log in a user"""

    username = forms.CharField(
        max_length=63,
        widget=forms.TextInput(
            attrs={"class": "form-control-auth", "placeholder": "Nom d'utilisateur"}
        ),
        label="",
    )
    password = forms.CharField(
        max_length=63,
        widget=forms.PasswordInput(
            attrs={"class": "form-control-auth", "placeholder": "Mot de passe"}
        ),
        label="",
    )


class SignupForm(LoginForm):
    """Form to create a new user or login an existing one"""

    password_confirmation = forms.CharField(
        max_length=63,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control-auth",
                "placeholder": "Confirmer mot de passe",
            }
        ),
        label="",
    )

    def is_valid(self) -> bool:
        # we dont use early returns here because we want to display all errors
        is_valid = super().is_valid()
        if self.cleaned_data["password"] != self.cleaned_data["password_confirmation"]:
            self.add_error(
                "password_confirmation",
                "Le mot de passe et sa confirmation ne sont pas identiques.",
            )
            is_valid = False
        if User.objects.filter(username=self.cleaned_data["username"]).exists():
            self.add_error("username", "Un utilisateur avec ce nom existe déjà.")
            is_valid = False
        return is_valid
