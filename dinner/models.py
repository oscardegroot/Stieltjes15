from django.db import models
from picnic.models import Profile, Item
from datetime import date, datetime, timedelta
import locale
import calendar
from django.core.urlresolvers import reverse

class Recipe(models.Model):
    name = models.CharField(max_length=500)
    foodtype = models.CharField(max_length=50, default='Other')
    picture = models.CharField(max_length=500, default='https://www.picnic.nl/shared-assets/images/public/img-logo@2x.png')
    persons = models.IntegerField()
    link = models.CharField(max_length=1000, default='https://www.ah.nl/allerhande')

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse('dinner:recipe-detail', kwargs={'pk': self.pk})

# Library Item
class DinnerDate(models.Model):
    date = models.DateField(default=datetime.now)
    profiles = models.ManyToManyField(Profile,blank=True)
    recipes = models.ManyToManyField(Recipe,blank=True)
    boodschap_feuten = models.ManyToManyField(Profile, related_name="feuten",blank=True)

    class Meta:
        unique_together = ['date']

    def __str__(self):
        if(self.date == datetime.today().date()):
            return 'Vandaag'

        tomorrow = datetime.today() + timedelta(days=1)

        if(self.date == tomorrow.date()):
            return 'Morgen'

        locale.setlocale(locale.LC_ALL, 'nld_nld')

        return calendar.day_name[self.date.weekday()] + ' ' + str(self.date.day) + ' ' + calendar.month_name[self.date.month]



    # def get_absolute_url(self):
    #     return reverse('picnic:detail', kwargs={'pk': self.pk})