import json

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect, render

from .forms import MatchForm, RivalForm
from .models import Match, Team
from .utils import getkey

# Create your views here.
def index(request):
    try:
        matches_to_me = Match.objects.filter(Q(player1=request.user, accept1=False)|Q(player2=request.user, accept2=False)).order_by('time')
        num = len(matches_to_me)
    except:
        num = 0
    return render(request, 'record/index.html', {
        'num': num,
    })

@login_required
def profile(request):
    # 내가 player1이고 accept2가 False 혹은 내가 player2이고 accept1이 False
    matches_by_me = Match.objects.filter(Q(player1=request.user, accept2=False)|Q(player2=request.user, accept1=False)).order_by('time')
    # 내가 player1이고 accept1이 False 혹은 내가 player2이고 accept2가 False
    matches_to_me = Match.objects.filter(Q(player1=request.user, accept1=False)|Q(player2=request.user, accept2=False)).order_by('time')
    return render(request, "record/profile.html", {
        "matches_by_me": matches_by_me,
        "matches_to_me": matches_to_me,
    })

@login_required
def match_cancel(request):
    if request.method == 'POST':
        model = Match.objects.get(pk=request.POST['pk'])
        model.delete()
        return redirect('record:profile')

@login_required
def match_accept(request):
    if request.method == 'POST':
        model = Match.objects.get(pk=request.POST['pk'])
        model.accept1, model.accept2 = True, True
        model.save()
        return redirect('record:profile')

@login_required
def match_show(request):
    if request.method == 'POST':
        form = MatchForm(request.POST)
        if form.is_valid():
            model = form.save(commit=False)
            match_id = "match-"+request.POST['id']
            return render(request, 'record/match_show.html', {
                "model": model,
                "match_id": match_id,
            })
    else:
        pass

@login_required
def match_new(request):
    # request.method 로 분기한다.
    if request.method == 'POST':
        form = MatchForm(request.POST)
        if form.is_valid():
            form = MatchForm(request.POST)
            if form.is_valid():
                model = form.save(commit=False)
                # 상대방이 승인하기전이므로 False로 넣는다.
                player1, player2 = request.user, User.objects.get(pk=int(request.GET['rival']))

                # model에 player를 입력할때는 pk가 작은게 player1, pk가 큰게 player2로 넣는다.
                if player1.pk < player2.pk:
                    model.player1, model.player2 = player1, player2
                    model.accept1, model.accept2 = True, False
                else:
                    # 점수, 팀, 스코어를 뒤집어서 넣어준다.
                    model.player1, model.player2 = player2, player1
                    model.team1, model.team2 = model.team2, model.team1
                    model.score1, model.score2 = model.score2, model.score1
                    model.accept1, model.accept2 = False, True

                model.save()
                response_data = {}
                response_data['pk'] = model.pk

            return JsonResponse(response_data)
    else:
        form = MatchForm()
        teams = Team.objects.all().order_by('teamname')

    return render(request, 'record/match_new.html', {
        'form': form,
        'teams': teams,
    })

@login_required
def find(request, mode):
    if request.is_ajax():
        # username을 받아온뒤 존재하는지 확인한다.
        username = request.POST['username']
        try:
            rival = User.objects.get(username=username)
        except:
            rival = None
        if mode == "new":
            button_text = "전적 추가하러 가기"
        elif mode == "detail":
            button_text = "전적 확인하러 가기"
        return render(request, 'record/findresult.html',{
            'rival': rival,
            'button_text': button_text,
        })

    elif request.method == 'POST':
        pk1 = request.user.pk
        pk2 = int(request.POST['id'])
        # 전적 생성이 요청된 경우.
        if mode == "new":
            url = reverse('record:match_new')
            url = url + '?rival=' + str(pk2)
            return redirect(url)
        # 전적 확인이 요청된 경우.
        elif mode == "detail":
            return redirect('record:detail', pk1, pk2)
    else:
        if mode == "new":
            title_text = "함께 플레이한 유저를 검색해주세요."
        elif mode == "detail":
            title_text = "전적이 궁금한 유저를 입력해주세요."
        return render(request, 'record/rival.html', {
            'title_text': title_text,
        })


@login_required
def detail(request, pk1, pk2):
    if request.user.pk == int(pk1):
        p1, p2 = User.objects.get(pk=pk1), User.objects.get(pk=pk2)

        # pk 값이 작은쪽이 늘 player1으로 만들어져있을 것이다.
        if pk1 < pk2:
            matches = Match.objects.filter(player1=p1, player2=p2, accept1=True, accept2=True).order_by('-time')
        else:
            matches = Match.objects.filter(player1=p2, player2=p1, accept1=True, accept2=True).order_by('-time')

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
        # pk1이 더 크다면, 뒤집어줄 것을 뒤집어준다.
        if pk1 > pk2:
            win, defeat, GF, GA = defeat, win, GA, GF

        last_five = matches[:5]
        curr_five = ""
        if pk1 < pk2:
            for match in last_five:
                if match.score1 > match.score2:
                    curr_five = '승' + curr_five
                elif match.score1 < match.score2:
                    curr_five = '패' + curr_five
                else:
                    curr_five = '무' + curr_five
        else:
            for match in last_five:
                if match.score1 > match.score2:
                    curr_five = '패' + curr_five
                elif match.score1 < match.score2:
                    curr_five = '승' + curr_five
                else:
                    curr_five = '무' + curr_five

        if pk1 < pk2:
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
        else:
            team2s = Match.objects.filter(player1=p2, player2=p1).values('team2').distinct()
            infos = []
            for team2 in team2s:
                team = Team.objects.get(pk=team2['team2'])
                matches = Match.objects.filter(player1=p2, player2=p1, team2=team)
                if len(matches) >= 3:
                    twin, tdraw, tdefeat = 0, 0, 0
                    for m in matches:
                        twin = twin + (m.score1 < m.score2)
                        tdraw = tdraw + (m.score1 == m.score2)
                        tdefeat = tdefeat + (m.score1 > m.score2)
                    point = (twin * 3 + tdraw) / len(matches)
                    infos.append({"teamname": team.teamname, "point": point})
            # point 내림차순으로 정렬.
            infos.sort(key=getkey, reverse=True)

        return render(request, 'record/detail.html', {
            'p1': p1,
            'p2': p2,
            'win': win,
            'draw': draw,
            'defeat': defeat,
            'GF': GF,
            'GA': GA,
            'curr_five': curr_five,
            'last_five': last_five,
            'infos': infos,
            'pk1_is_smaller': (p1.pk < p2.pk),
        })
    else:
        msg = "자신이 경기한 전적만 열람할 수 있습니다."
        return render(request, 'record/error.html', {
            'msg': msg,
        })
