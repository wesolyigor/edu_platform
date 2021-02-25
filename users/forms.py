from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class CustomUserCreationForm(UserCreationForm):  # klasa bazowa dla formularza Custom Form
    class Meta:
        model = get_user_model()  # pobiera aktualnie używany model, który jest używany w Django
        fields = ("email", "username")


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ("email", "username")
