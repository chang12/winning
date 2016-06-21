from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import Profile


class MyAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(MyAuthenticationForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].label = ''
        self.fields['username'].widget.attrs['placeholder'] = '이름'
        self.fields['password'].widget.attrs['placeholder'] = '비밀번호'


class MyUserCreationForm(UserCreationForm):

    # self.fields['username'].help_text=None

    def save(self, commit=True):
        # 다중 상속시에 상위 클래스들의 메소드 중복 호출을 피하기 위해 super가 사용됨.
        # 인자로 class 이름과 self를 왜 받는지에 대해서는 모름.
        user = super(MyUserCreationForm, self).save(commit=False)
        if commit:
            user.is_active = True
            user.save()

        profile = Profile(user=user)
        profile.save()
        user.profile = profile
        user.save()
        return user

    def __init__(self, *args, **kwargs):
        super(MyUserCreationForm, self).__init__(*args, **kwargs)
        # 각 input 태그의 help_text, label을 제거함.
        for field in self.fields:
            self.fields[field].help_text = None
            self.fields[field].label = ''
        # 각 input 태그에 placeholder를 추가함.
        self.fields['username'].widget.attrs['placeholder'] = "이름"
        self.fields['password1'].widget.attrs['placeholder'] = "비밀번호"
        self.fields['password2'].widget.attrs['placeholder'] = "비밀번호 확인"
