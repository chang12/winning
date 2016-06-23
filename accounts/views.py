from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

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

            return redirect('record:index')

    else:
        form = UserCreationForm()

    return render(request, 'accounts/signup.html', {
        'form': form,
    })
