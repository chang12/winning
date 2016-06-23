from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import JsonResponse
from django.shortcuts import render

# from .forms import MyUserCreationForm as UserCreationForm
from .forms import MyUserCreationForm as UserCreationForm


# Create your views here.
def login(request):
    auth_login(request)


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():

            username = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password2')
            email = form.cleaned_data.get('email')

            User.objects.create_user(username, email, password)
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
