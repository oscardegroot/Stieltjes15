from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.urlresolvers import reverse
from django import template
import calendar
import locale

register = template.Library()

@register.filter
def atindex(l, i):
    try:
        return l[i]
    except:
        return None


# Library Item
class Item(models.Model):
    name = models.CharField(max_length=500)
    price = models.DecimalField(max_digits=4, decimal_places=2)
    picture = models.CharField(max_length=500, default='https://www.picnic.nl/shared-assets/images/public/img-logo@2x.png')

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse('picnic:detail', kwargs={'pk': self.pk})


# Profile (one to one extension of User class)
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favourite_items = models.ManyToManyField(Item)
    picture = models.FileField(default='images/anonymous.jpg', upload_to="images")
    turfjes = models.IntegerField(default=0)
    boodschap_stand = models.FloatField(default=0)

    def __str__(self):
        return str(self.user.get_full_name())

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()


# Shopping List
class List(models.Model):
    admin = models.ForeignKey(Profile, on_delete=models.CASCADE)
    is_ordered = models.BooleanField(default=False)
    creation_date = models.DateField(auto_now=True)
    deadline = models.DateField()

    def __str__(self):
        locale.setlocale(locale.LC_ALL, 'nld_nld')
        return str(self.admin.user.first_name) + ' bestelt ' + calendar.day_name[(self.deadline.weekday() - 1) % 7] + ' 21:00'

    def str_deadline(self):
        locale.setlocale(locale.LC_ALL, 'nld_nld')
        return 'Levering op ' + calendar.day_name[self.deadline.weekday()]


# List Item
class ListItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    list = models.ForeignKey(List, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

    class Meta:
        unique_together = ('item', 'profile', 'list')

    def __str__(self):
        return str(self.quantity) + 'x ' + str(self.item) + ' \u20ac' + str(self.quantity * self.item.price)


# # Receipt for bookkeeping
# class Receipt(models.Model):
#     ordered_by = models.ForeignKey(Profile, on_delete=models.CASCADE)
#     order_date = models.DateField()
#
#
# class PersonalReceipt(models.Model):
#     profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
#     receipt = models.ForeignKey(Receipt, on_delete=models.CASCADE)
#     price = models.DecimalField(max_digits=4, decimal_places=2)
#     item_description = models.CharField(1000)
#
#     class Meta:
#         unique_together = ('profile', 'receipt')
