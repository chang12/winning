from django.forms import ModelForm

from .models import Match, Rival


# Create the form class.
class MatchForm(ModelForm):
    class Meta:
        # Meta class describes "anything that's not a field".
        model = Match
        exclude = ['player1', 'time']


class RivalForm(ModelForm):
    class Meta:
        model = Rival
        fields = '__all__'
