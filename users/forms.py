from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.forms import ModelForm, CharField, PasswordInput, EmailField, TextInput


class RegistrationForm(ModelForm):
    password_confirm = CharField(label="Password Confirmation", widget=PasswordInput, required=True)
    password = CharField(label="Password", widget=PasswordInput, required=True)

    class Meta:
        model = get_user_model()
        fields = ("email", "fullname", "is_instructor", 'password')

    def clean_password(self):
        password = self.cleaned_data.get("password")
        password_confirm = self.cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise ValidationError("Passwords don't match")

        return password_confirm

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])

        if commit:
            user.save()

        return user


class LoginForm(AuthenticationForm):
    username = EmailField(widget=TextInput(attrs={
        "class": "form-control eluwina",
        "type": "text",
        "name": "username",
        "placeholder": "Elo ziom"
    }), label="Email")

    class Meta:
        model = get_user_model()
        fields = ("username", "password")
