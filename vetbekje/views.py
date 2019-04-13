from django.views import generic
from picnic.views import LoginRequiredMixin
from vetbekje.models import Battle, Pool, PoolEntry
from picnic.models import Profile
from django.views.generic.edit import CreateView, UpdateView
from vetbekje.forms import BattleForm, PoolForm
from django.shortcuts import render,redirect
from django.contrib import messages
from django.core.urlresolvers import reverse
from stieltjes15.settings import MEDIA_ROOT
import operator


def win_battle_view(request, pk, target_won):
    battle = Battle.objects.get(pk=pk)
    challenger = Profile.objects.get(pk=battle.challenger.pk)
    target = Profile.objects.get(pk=battle.target.pk)
    if target_won == '1':
        target.boodschap_stand += battle.value
        challenger.boodschap_stand -= battle.value
        battle.target_won = True
    else:
        target.boodschap_stand -= battle.value*battle.ratio
        challenger.boodschap_stand += battle.value*battle.ratio
        battle.target_won = False

    target.save()
    challenger.save()

    battle.done = True
    battle.save()

    return redirect(reverse('vetbekje:index'))


class IndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'vetbekje/index.html'

    def get_queryset(self):
        return Battle.objects.filter(done=False)

    def get_score(self, profile, battles):
        score = 0

        for battle in battles:
            if battle.challenger == profile:
                if battle.target_won:
                    score -= battle.value
                else:
                    score += battle.value

            elif battle.target == profile:
                if battle.target_won:
                    score += battle.value
                else:
                    score -= battle.value

        return score

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)

        old_battles = Battle.objects.filter(done=True)
        profiles = [profile for profile in Profile.objects.all()]

        scores = []

        for profile in profiles:
            scores.append(round(self.get_score(profile, old_battles), 2))

        profiles_sorted = []
        scores_sorted = []

        while len(scores) > 0:
            i, s = max(enumerate(scores), key=operator.itemgetter(1))
            scores_sorted.append(scores.pop(i))
            profiles_sorted.append(profiles.pop(i))

        context['scores'] = scores_sorted
        context['profiles'] = profiles_sorted
        context['names'] = Profile.objects.filter().exclude(pk=self.request.user.pk)
        context['battles'] = IndexView.get_queryset(self)
        context['pool_list'] = Pool.objects.filter(done=False)


        return context


# Item creation view
class BattleFormView(LoginRequiredMixin, CreateView):
    model = Battle
    form_class = BattleForm

    def post(self, request, **kwargs):
        form_data = BattleForm(request.POST)

        if form_data.is_valid():
            battle = form_data.save(commit=False)
            battle.target = Profile.objects.get(pk=self.kwargs['pk'])
            battle.challenger = Profile.objects.get(user=request.user)

            battle.save()
        else:
            messages.error(request, 'Er klopt iets nie')
            return reverse('vetbekje:target', kwargs={'pk': self.kwargs['pk']})

        return redirect('vetbekje:index')


# Item creation view
class PoolFormView(LoginRequiredMixin, CreateView):
    model = Pool
    form_class = PoolForm

    def post(self, request, **kwargs):
        form_data = PoolForm(request.POST)
        print(form_data)
        if form_data.is_valid():
            # Retrieve data
            pool = form_data.save(commit=False)

            # Add the creator
            profile = Profile.objects.get(user=request.user)
            pool.creator = profile

            # Add the creator's entry
            entry_value = form_data.cleaned_data['entry']
            entry = PoolEntry(entry=entry_value, profile=profile)
            entry.save()

            # Set no winner yet and save the pool
            pool.winner = None
            pool.save()
            pool.entries.add(entry)
            pool.save()

        else:
            messages.error(request, 'Er klopt iets nie')
            return redirect('vetbekje:pool-new')

        return redirect('vetbekje:index')


class BattleDetailView(LoginRequiredMixin, generic.DetailView):
    model = Battle

    def get_context_data(self, **kwargs):
        context = super(BattleDetailView, self).get_context_data(**kwargs)
        context['media_root'] = MEDIA_ROOT
        context['active'] = Profile.objects.get(user=self.request.user).pk
        battle = context['battle']
        context['challenger_value'] = battle.value*battle.ratio
        return context


class PoolDetailView(LoginRequiredMixin, generic.DetailView):
    model = Pool

    def get_context_data(self, **kwargs):
        context = super(PoolDetailView, self).get_context_data(**kwargs)
        context['media_root'] = MEDIA_ROOT
        #pool = context['pool']
        return context
