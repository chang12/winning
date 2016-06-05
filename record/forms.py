from django.forms import ModelForm

from .models import Match, Rival


class MatchForm(ModelForm):
    class Meta:
        # Meta class describes "anything that's not a field".
        model = Match
        exclude = ['player1', 'player2', 'time', 'accept1', 'accept2']


class RivalForm(ModelForm):
    class Meta:
        model = Rival
        fields = '__all__'
