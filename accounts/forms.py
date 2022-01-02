import unicodedata
from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.hashers import check_password
from django.utils import timezone

User = get_user_model()

class ConfirmPasswordForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('confirm_password', )

    def clean(self):
        cleaned_data = super(ConfirmPasswordForm, self).clean()
        confirm_password = cleaned_data.get('confirm_password')
        if not check_password(confirm_password, self.instance.password):
            self.add_error('confirm_password', 'Password does not match.')

    def save(self, commit=True):
        user = super(ConfirmPasswordForm, self).save(commit)
        user.last_login = timezone.now()
        if commit:
            user.save()
        return user


class UsernameField(forms.CharField):
    def to_python(self, value):
        return unicodedata.normalize('NFKC', super().to_python(value.lower()))


class UserCreationForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username, email and
    password.
    """
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
        'username_taken': _("This username is taken")
    }
    username = forms.CharField(
        label=_("Username"),
        strip=False,
        help_text=_("your username must be unique. It will be public"),
        max_length=254
    )
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput,
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput,
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email")
        field_classes = {'username': UsernameField}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._meta.model.USERNAME_FIELD in self.fields:
            self.fields[self._meta.model.USERNAME_FIELD].widget.attrs.update({
                                                                             'autofocus': True})

    def clean_username(self):
        username = self.cleaned_data.get("username")
        qs = User.objects.filter(username=username)
        if qs.exists() and username:
            raise forms.ValidationError(
                self.error_messages['username_taken'],
                code='username_taken',
            )
        return username.lower()

    def clean_password2(self):
        password1 = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def _post_clean(self):
        super()._post_clean()
        # Validate the password after self.instance is updated with form data
        # by super().
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password2')
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except forms.ValidationError as error:
                self.add_error('password2', error)
        elif username:
            if forms.ValidationError:
                self.add_error('username', forms.ValidationError)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class SignupForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username',
                  'email', 'password', 'password2')
