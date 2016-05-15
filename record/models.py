from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Match(models.Model):
    player1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='player1')
    player2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='player2')
    team1 = models.CharField(max_length=20)
    team2 = models.CharField(max_length=20)
    time = models.DateTimeField(auto_now_add=True)
    score1 = models.IntegerField()
    score2 = models.IntegerField()

    def __str__(self):
        return self.player1.username+' '+self.player2.username+' ('+str(self.time)+')'
