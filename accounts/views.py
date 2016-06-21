from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.shortcuts import redirect, render

from .forms import MyUserCreationForm


# Create your views here.
def login(request):
    auth_login(request)


def signup(request):
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, '인증 이메일이 발송되었습니다.')
            return redirect('record:index')

    else:
        form = MyUserCreationForm()

    return render(request, 'accounts/signup.html', {
        'form': form,
    })
