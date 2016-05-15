from django.shortcuts import redirect, render

from .forms import MyUserCreationForm

# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('record:index')

    else:
        form = MyUserCreationForm()

    return render(request, 'accounts/signup.html', {
        'form': form,
    })
