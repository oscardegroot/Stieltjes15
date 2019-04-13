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


class PoolEntry(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    entry = models.CharField(max_length=50)

    def __str__(self):
        return "Entry for " + self.profile.user.first_name + " betting on " + str(self.entry)


class Pool(models.Model):
    entries = models.ManyToManyField(PoolEntry, related_name='entries')
    description = models.CharField(max_length=200, default='')
    value = models.FloatField(default=0.1)
    winner = models.ForeignKey(PoolEntry, default=None, null=True, on_delete=models.CASCADE, related_name='winner')
    done = models.BooleanField(default=False)
    creator = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return "Pool worth " + str(self.value)
