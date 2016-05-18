from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.shortcuts import redirect, render

from .forms import MatchForm, RivalForm
from .models import Match, Team
from .utils import getkey

# Create your views here.
def index(request):
    pk = request.user.pk
    users = User.objects.filter(~Q(pk = pk))
    return render(request, 'record/index.html', {
        'users': users,
    })

@login_required
def match_new(request):
    if request.method == 'POST':
        teams = ''
        form = MatchForm(request.POST)
        if form.is_valid():
            model = form.save(commit=False)
            model.player1 = request.user
            pk = int(request.GET['rival'])
            rival = User.objects.filter(pk=pk)
            model.player2 = User.objects.get(pk=pk)
            team1 = Team.objects.get(pk=request.POST['team1'])
            team2 = Team.objects.get(pk=request.POST['team2'])
            model.team1, model.team2 = team1, team2
            model.save()
        return redirect('record:index')
    else:
        form = MatchForm()
        teams = Team.objects.all()

    return render(request, 'record/match_new.html', {
        'form': form,
        'teams': teams,
    })

@login_required
def find(request):
    users = ''
    if request.method == 'POST':
        flag = int(request.GET['flag'])
        pk1 = request.user.pk
        pk2 = int(request.POST['id'])
        # 전적 생성이 요청된 경우.
        if flag == 0:
            url = reverse('record:match_new')
            url = url + '?rival=' + str(pk2)
            return redirect(url)
        # 전적 확인이 요청된 경우.
        else:
            return redirect('record:detail', pk1, pk2)
    else:
        form = RivalForm()
        pk = int(request.user.pk)
        users = User.objects.filter(~Q(pk = pk))

    return render(request, 'record/rival.html', {
        'form': form,
        'users': users,
    })


@login_required
def detail(request, pk1, pk2):
    if request.user.pk == int(pk1):
        p1, p2 = User.objects.get(pk=pk1), User.objects.get(pk=pk2)
        matches = Match.objects.filter(player1=p1, player2=p2).order_by('-time')
        win, draw, defeat, GF, GA = 0, 0, 0, 0, 0

        for match in matches:
            GF = GF + match.score1
            GA = GA + match.score2
            if match.score1 > match.score2:
                win = win + 1;
            elif match.score1 < match.score2:
                defeat = defeat + 1;
            else:
                draw = draw + 1;

        last_five = matches[:5]
        curr_five = ""
        for match in last_five:
            if match.score1 > match.score2:
                curr_five = '승' + curr_five
            elif match.score1 < match.score2:
                curr_five = '패' + curr_five
            else:
                curr_five = '무' + curr_five

        team1s = Match.objects.filter(player1=p1, player2=p2).values('team1').distinct()
        infos = []
        for team1 in team1s:
            team = Team.objects.get(pk=team1['team1'])
            matches = Match.objects.filter(player1=p1, player2=p2, team1=team)
            if len(matches) >= 3:
                twin, tdraw, tdefeat = 0, 0, 0
                for m in matches:
                    twin = twin + (m.score1 > m.score2)
                    tdraw = tdraw + (m.score1 == m.score2)
                    tdefeat = tdefeat + (m.score1 < m.score2)
                point = (twin * 3 + tdraw) / len(matches)
                infos.append({"teamname": team.teamname, "point": point})
        # point 내림차순으로 정렬.
        infos.sort(key=getkey, reverse=True)

        return render(request, 'record/detail.html', {
            'name1': p1.profile.nickname,
            'name2': p2.profile.nickname,
            'win': win,
            'draw': draw,
            'defeat': defeat,
            'GF': GF,
            'GA': GA,
            'curr_five': curr_five,
            'last_five': last_five,
            'infos': infos,
        })
    else:
        msg = "자신이 경기한 전적만 열람할 수 있습니다."
        return render(request, 'record/error.html', {
            'msg': msg,
        })
