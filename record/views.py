from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import MatchForm, RivalForm
from .models import Match

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

@login_required
def find(request):
    if request.method == 'POST':
        form = RivalForm(request.POST)
        print("check")
        if form.is_valid():
            # 전적 디테일 페이지로 redirect.
            pk1 = request.user.pk
            pk2 = form.cleaned_data['player'].pk
            return redirect('record:detail', pk1, pk2)
    else:
        form = RivalForm()

    return render(request, 'record/rival.html', {
        'form': form,
    })


@login_required
def detail(request, pk1, pk2):
    if request.user.pk == int(pk1):
        p1 = User.objects.get(pk=pk1)
        p2 = User.objects.get(pk=pk2)
        matches = Match.objects.filter(player1=p1, player2=p2)
        win, draw, defeat = 0, 0, 0
        for match in matches:
            if match.score1 > match.score2:
                win = win + 1;
            elif match.score1 < match.score2:
                defeat = defeat + 1;
            else:
                draw = draw + 1;
        return render(request, 'record/detail.html', {
            'name1': p1.username,
            'name2': p2.username,
            'win': win,
            'draw': draw,
            'defeat': defeat,
        })
    else:
        msg = "자신이 경기한 전적만 열람할 수 있습니다."
        return render(request, 'record/error.html', {
            'msg': msg,
        })
