from django import forms
from main.models import User

# TODO signup 비밀번호 체크
# TODO signup 에러 메시지 발생


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'username', 'password']
