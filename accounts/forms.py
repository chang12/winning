from django.contrib.auth import password_validation
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django import forms


class MyAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(MyAuthenticationForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = ''
        self.fields['password'].label = ''

        self.fields['username'].widget.attrs['placeholder'] = '이메일'
        self.fields['password'].widget.attrs['placeholder'] = '비밀번호'

        self.error_messages['invalid_login'] = "유효하지 않은 계정 정보 입니다."


class MyUserCreationForm(forms.Form):
    # strip: default는 True이고, True면 중간과 끝 이후의 whitespace를 벗겨내서 저장한다.

    error_messages = {
        'email_already_exists': "이미 등록된 이메일입니다.",
        'password_mismatch': "암호가 일치하지 않습니다.",
    }

    email = forms.EmailField(
        label='',
        widget=forms.EmailInput(
            attrs={"placeholder": "이메일"}
        )
    )
    password1 = forms.CharField(
        label='',
        strip=False,
        widget=forms.PasswordInput(
            attrs={"placeholder": "비밀번호"}
        ),
    )
    password2 = forms.CharField(
        label='',
        strip=False,
        widget=forms.PasswordInput(
            attrs={"placeholder": "비밀번호 확인"}
        ),
    )
    name = forms.CharField(
        max_length=20,
        label='',
        widget=forms.TextInput(
            attrs={"placeholder": "사용자 이름"}
        ),
    )

    # Email 값을 입력하지 않는 것은, default validators가 처리해준다.
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if email:
            if User.objects.filter(username=email).exists():
                raise forms.ValidationError(
                    self.error_messages['email_already_exists'],
                    code='email_already_exists',
                )
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        # password mismatch 문제를 우선 확인하고, validate.
        password_validation.validate_password(password2)

        return password2


# 1) User를 생성하는 과정에서, Profile도 생성하기 위해서 save 함수를 오버라이딩 한다.
# 2) help_text, label을 없애고, placeholder를 추가하기 위해서 생성자를 오버라이딩 한다.
# 위 2가지 목적에 의해 UserCreationForm을 상속받아 새로운 Form을 정의한듯.
# class MyUserCreationForm(UserCreationForm):

#     def save(self, commit=True):
#         # 다중 상속시에 상위 클래스들의 메소드 중복 호출을 피하기 위해 super가 사용됨.
#         # 인자로 class 이름과 self를 왜 받는지에 대해서는 모름.
#         user = super(MyUserCreationForm, self).save(commit=False)
#         if commit:
#             user.is_active = True
#             user.save()

#         profile = Profile(user=user)
#         profile.save()
#         user.profile = profile
#         user.save()

#     def __init__(self, *args, **kwargs):
#         super(MyUserCreationForm, self).__init__(*args, **kwargs)
#         # 각 input 태그의 help_text, label을 제거함.
#         for field in self.fields:
#             self.fields[field].help_text = None
#             self.fields[field].label = ''
#         # 각 input 태그에 placeholder를 추가함.
#         self.fields['username'].widget.attrs['placeholder'] = "이름"
#         self.fields['password1'].widget.attrs['placeholder'] = "비밀번호"
#         self.fields['password2'].widget.attrs['placeholder'] = "비밀번호 확인"
