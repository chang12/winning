from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Team(models.Model):
    teamname = models.CharField(max_length=20)

    class Meta:
        ordering = ['teamname']

    def __str__(self):
        return self.teamname

class Match(models.Model):
    player1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='player1')
    player2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='player2')
    team1 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team1')
    team2 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team2')
    time = models.DateTimeField(auto_now_add=True)
    score1 = models.IntegerField()
    score2 = models.IntegerField()
    accept1 = models.BooleanField()
    accept2 = models.BooleanField()

    def __str__(self):
        return self.player1.username+' '+self.player2.username+' ('+str(self.time)+')'

class Rival(models.Model):
    player = models.ForeignKey(User)
