from django.forms import ModelForm

from .models import Match


# Create the form class.
class MatchForm(ModelForm):
    class Meta:
        # Meta class describes "anything that's not a field".
        model = Match
        exclude = ['player1', 'time']
