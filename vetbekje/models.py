from django.db import models
from picnic.models import Profile

# A Battle
class Battle(models.Model):
    challenger = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='challenger')
    target = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='target')
    bet_description = models.CharField(max_length=500)
    value = models.FloatField(default=1)
    ratio = models.FloatField(default=1)
    done = models.BooleanField(default=False)
    target_won = models.BooleanField(default=True)

    def __str__(self):
        return str(self.challenger) + " Versus " + str(self.target)


class Pool(models.Model):
    description = models.CharField(max_length=200, default='')
    value = models.FloatField(default=0.1)
    done = models.BooleanField(default=False)
    creator = models.ForeignKey(Profile, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return "Pool worth " #+ str(self.value)


class PoolEntry(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    entry = models.CharField(max_length=50, default='')
    pool = models.ForeignKey(Pool, related_name='pool', default=None)
    won = models.BooleanField(default=False)

    def __str__(self):
        return "Pool entry van" + self.profile.user.first_name


