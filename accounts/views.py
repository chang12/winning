from uuid import uuid4

# from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.views import login as auth_login
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.http import JsonResponse
from django.shortcuts import redirect, render

from winning import settings

from .forms import MyUserCreationForm as UserCreationForm
from .forms import MyAuthenticationForm as AuthenticationForm
from .models import Token


# Create your views here.
def login(request):
    # 지금 코드 상태에 불필요한 로직이 많아보인다.
    # AuthenticationForm의 validation 과정에 authenticate 하고,
    # return 값의 존재성을 체크하는 과정이 있다.
    # 그리고 User의 is_active 체크 과정도 있다.
    # 일례로, inactive한 user의 정보로 login을 시도하면,
    # 이 view의 로직대로 error를 띄우는게 아니라,
    # AuthenticationForm의 invalid code의 error message가 뜬다.

    if request.method == 'POST':
        data = {}
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    auth_login(request, user)
                    data['status'] = True
                    data['url'] = reverse('record:index')
                    return JsonResponse(data)
                else:
                    data['status'] = False
                    data['error'] = "인증 이메일을 확인해주세요."
                    return JsonResponse(data)
            else:
                data['status'] = False
                data['error'] = "유효하지 않은 계정 정보입니다."
                return JsonResponse(data)

        else:
            error_key = list(form.errors.keys())[0]
            # 그 field의 첫번째 error의 메시지를 획득한다.
            error_message = form.errors[error_key][0]
            data['status'] = False
            data['error'] = error_message
            return JsonResponse(data)

    else:
        messages.warning(request, '유효하지 않은 접근입니다.')
        return redirect('record:index')


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():

            # User를 생성한다.
            username = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password2')
            email = form.cleaned_data.get('email')
            user = User.objects.create_user(username, email, password, is_active=False)

            # Token을 생성해서 DB에 저장한다.
            token = str(uuid4()) + '-' + str(user.pk)
            Token(user=user, token=token).save()

            # 메일 내용을 완성한다.
            confirm_url = settings.DOMAIN_NAME + reverse('accounts:confirm', kwargs={'token': token})
            title = "Winning 서비스의 인증 이메일입니다."
            body = "<p>아래 링크를 클릭하여 계정 생성 과정을 완료해주세요.</p><a href=%s><p>%s</p></a>" % (confirm_url, confirm_url)

            # 메일을 전송한다.
            send_mail(
                title,
                body,
                settings.EMAIL_HOST_USER,
                [user.username],
                html_message=body,
            )

            messages.info(request, '인증 이메일이 발송되었습니다.')
            data = {}
            data['status'] = True
            data['url'] = reverse('record:index')

            return JsonResponse(data)
        else:
            # 적어도 하나의 error는 존재할 것이다.
            # error가 존재하는 field 중 하나를 임의로 받아온다.
            error_key = list(form.errors.keys())[0]
            # 그 field의 첫번째 error의 메시지를 획득한다.
            error_message = form.errors[error_key][0]
            data = {}
            data['status'] = False
            data['error'] = error_message
            return JsonResponse(data)
    else:
        form = UserCreationForm()

    return render(request, 'accounts/signup.html', {
        'form': form,
    })


def confirm(request, token):
    try:
        token = Token.objects.get(token=token)
    except Token.DoesNotExist:
        messages.warning(request, '유효하지 않은 인증 토큰입니다.')
        return redirect('record:index')

    user = token.user
    user.is_active = True
    user.save()
    token.delete()

    messages.info(request, '인증이 완료되었습니다. 로그인하세요.')
    return redirect('record:index')
