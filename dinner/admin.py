from django.contrib import admin
from datetime import date
from dinner.models import Recipe, DinnerDate
from django.utils.translation import ugettext_lazy as _




class DinnerDateNCFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _('Boodschap Niet Geclaimed')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'DinnerDate'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('NC', _('Not Claimed')),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or '90s')
        # to decide how to filter the queryset.
        if self.value() == 'NC':
            return queryset.filter(date__lte=date.today(), boodschap_feuten=None).exclude(profiles=None)

class DinnerDateAdmin(admin.ModelAdmin):
    list_filter = (DinnerDateNCFilter,)

# Register your models here.
admin.site.register(Recipe)
admin.site.register(DinnerDate, DinnerDateAdmin)
