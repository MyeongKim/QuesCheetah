# 직접 개발한 코드

from django import forms
from main.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _


class UserCreationForm(forms.ModelForm):
    error_messages = {
        'password_mismatch': _("입력한 비밀번호가 같지 않습니다."),
    }
    password1 = forms.CharField(label=_("비밀번호"), widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("비밀번호 확인"), widget=forms.PasswordInput, help_text=_("확인을 위해 입력하신 비밀번호를 다시 입력해주세요."))

    class Meta:
        model = User
        fields = ("email", "username")

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'username', 'password']


class AuthenticationFormWithInactiveUsersOkay(AuthenticationForm):
    def confirm_login_allowed(self, user):
        pass
