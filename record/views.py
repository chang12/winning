from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import MatchForm

# Create your views here.
def index(request):
    return render(request, 'record/index.html')

@login_required
def match_new(request):
    if request.method == 'POST':
        form = MatchForm(request.POST)
        if form.is_valid():
            model = form.save(commit=False)
            model.player1 = request.user
            model.save()
        return redirect('record:index')
    else:
        form = MatchForm()

    return render(request, 'record/match_new.html', {
        'form': form,
    })
