from django.db import models
from picnic.models import Profile

# # Create your models here.
# class Pilsbaas(models.Model):
#     stand = models.IntegerField()
#     profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
#
#     def __str__(self):
#         return str(self.profile) + ' stand: ' + str(self.stand)