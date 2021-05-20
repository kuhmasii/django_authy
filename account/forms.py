from django import forms
from django.contrib.auth import get_user_model


User = get_user_model()


class RegisterForm(forms.Form):

    username = forms.CharField(max_length=50)
    email = forms.EmailField()
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    password1 = forms.CharField(
        widget=forms.PasswordInput,
        label="Password"
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput,
        label="Confirm password"
    )

    def clean_username(self):
        username = self.cleaned_data.get("username")
        qs = User.objects.filter(username__iexact=username)
        # The iexact makes the query responed to case insensitive

        if qs.exists():
            # exists method return a bool if or not if the query exist in the DB.
            raise forms.ValidationError(
                "Username is invalid, please pick another."
            )
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        qs = User.objects.filter(email__iexact=email)
        # The iexact makes the query responed to case insensitive

        if qs.exists():
            # exists method return a bool if or not if the query exist in the DB.
            raise forms.ValidationError(
                "Email already in use, please pick another."
            )
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    "Passwords don't match"
                )
        return password2


class LoginForm(forms.Form):

    username = forms.CharField(max_length=50)
    password = forms.CharField(
        widget=forms.PasswordInput
    )

    def clean_username(self):
        username = self.cleaned_data.get("username")
        qs = User.objects.filter(username__iexact=username)
        # The iexact makes the query responed to case insensitive

        if not qs.exists():
            # exists method return a bool if or not if the query exist in the DB.
            raise forms.ValidationError(
                "Username is invalid."
            )

        return username
