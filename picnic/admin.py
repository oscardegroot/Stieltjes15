from django.contrib import admin
from .models import ListItem, Item, List, Profile

admin.site.register(ListItem)
admin.site.register(Item)
admin.site.register(Profile)
admin.site.register(List)
