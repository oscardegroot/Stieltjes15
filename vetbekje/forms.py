
from django import forms
from django.core.exceptions import ValidationError
from .models import Battle, Pool
from django.utils.safestring import mark_safe


class BattleForm(forms.ModelForm):
    value = forms.FloatField(max_value=2, min_value=0.01, initial=1.0, required=True)
    bet_description = forms.CharField(max_length=500, required=True)
    ratio = forms.FloatField(max_value=100, min_value=0.01, initial=1.0, required=True)

    class Meta:
        model = Battle
        fields = ['bet_description', 'value', 'ratio']

    def __init__(self, *args, **kwargs):
        super(BattleForm, self).__init__(*args, **kwargs)
        self.fields['value'].label = "Hoeveel BP is de inzet?"
        self.fields['bet_description'].label = "Waar zet je op in?"
        a = "Speciaal voor Johan's slechte decision making:<br> gebruik een ratio! Als jij wint krijg jij zoveel keer de inzet:"
        a = mark_safe(a)
        self.fields['ratio'].label = a


class PoolForm(forms.ModelForm):
    description = forms.CharField(max_length=200, required=True)
    value = forms.FloatField(max_value=2, min_value=0.01, initial=1.0, required=True)

    class Meta:
        model = Pool
        fields = ['description', 'value']

    def __init__(self, *args, **kwargs):
        super(PoolForm, self).__init__(*args, **kwargs)
        self.fields['value'].label = "Hoeveel BP is de inzet pp?"
        self.fields['description'].label = "Waar gaat de pool over?"
