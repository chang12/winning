from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Profile


class MyUserCreationForm(UserCreationForm):
    nickname = forms.CharField(min_length=1, max_length=20)

    def save(self, commit=True):
        # 다중 상속시에 상위 클래스들의 메소드 중복 호출을 피하기 위해 super 가 사용됨.
        # 인자로 class 이름과 self를 왜 받는지에 대해서는 모름.
        user = super(MyUserCreationForm, self).save(commit=False)
        if commit:
            user.is_active = True
            user.save()

        profile = Profile(user=user, nickname=self.cleaned_data['nickname'])
        profile.save()
        user.profile = profile
        user.save()
        return user

    def __init__(self, *args, **kwargs):
        super(MyUserCreationForm, self).__init__(*args, **kwargs)

        # UserCreationForm의 각 field 들의 help text를 없애는 코드부분이 있지만 (아마 근우가 쓴 듯), 우선은 생략함.
