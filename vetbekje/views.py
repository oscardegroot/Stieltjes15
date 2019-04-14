from django.views import generic
from picnic.views import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from vetbekje.models import Battle, Pool, PoolEntry
from picnic.models import Profile
from django.views.generic.edit import CreateView, UpdateView
from vetbekje.forms import BattleForm, PoolForm
from django.shortcuts import render,redirect
from django.contrib import messages
from django.core.urlresolvers import reverse
from stieltjes15.settings import MEDIA_ROOT
import operator

@login_required
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

@login_required
def win_pool_view(request, pk, entry):
    pool = Pool.objects.get(pk=pk)
    winning_entry = PoolEntry.objects.get(pk=entry)
    winner = winning_entry.profile
    losers = PoolEntry.objects.filter(pool=pool).exclude(pk=entry)

    winner.boodschap_stand += pool.value * len(losers)
    winner.save()

    winning_entry.won = True
    winning_entry.save()

    for loser in losers:
        loser.profile.boodschap_stand -= pool.value
        loser.profile.save()

    pool.done = True
    pool.save()

    return redirect(reverse('vetbekje:index'))

@login_required
def add_poolentry_view(request, pk, profile_pk):
    pool = Pool.objects.get(pk=pk)
    profile = Profile.objects.get(pk=profile_pk)

    entry = PoolEntry(profile=profile, entry='', pool=pool)
    entry.save()

    return redirect('vetbekje:pool-entry-select', pk=pool.pk)

@login_required
def remove_poolentry_view(request, pk, profile_pk):
    pool = Pool.objects.get(pk=pk)
    profile = Profile.objects.get(pk=profile_pk)
    entry = PoolEntry.objects.get(pool=pool, profile=profile)
    PoolEntry.delete(entry)

    return redirect('vetbekje:pool-entry-select', pk=pool.pk)

@login_required
def delete_battle_view(request, pk):
    battle = Battle.objects.get(pk=pk)
    Battle.delete(battle)

    return redirect(reverse('vetbekje:index'))

@login_required
def delete_pool_view(request, pk):
    pool = Pool.objects.get(pk=pk)
    Pool.delete(pool)

    return redirect(reverse('vetbekje:index'))



class IndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'vetbekje/index.html'

    def get_queryset(self):
        return Battle.objects.filter(done=False)

    def get_score(self, profile, battles, pools):
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

        for pool in pools:
            try:
                entry = PoolEntry.objects.get(pool=pool, profile=profile)

                if entry.won:
                    losers = PoolEntry.objects.filter(pool=pool).exclude(pk=entry.pk)
                    score += pool.value * len(losers)
                else:
                    score -= pool.value

            except PoolEntry.DoesNotExist:
                continue

        return score

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)

        old_battles = Battle.objects.filter(done=True)
        old_pools = Pool.objects.filter(done=True)
        profiles = [profile for profile in Profile.objects.all()]

        scores = []

        for profile in profiles:
            scores.append(round(self.get_score(profile, old_battles, old_pools), 2))

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

        pools = Pool.objects.filter(done=False)
        entry_list = []
        for i in range(0, len(pools)):
            entry_list.append(PoolEntry.objects.filter(pool=pools[i]))

        context['pool_list'] = pools
        context['entry_list'] = entry_list
        print(entry_list)

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
            pool.save()

            # Add the creator's entry
            entry = PoolEntry(entry='', profile=profile, pool=pool, won=False)
            entry.save()

        else:
            messages.error(request, 'Er klopt iets nie')
            return redirect('vetbekje:pool-new')

        return redirect('vetbekje:pool-entry-select', pk=pool.pk)


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

        pool = context['pool']

        context['entries'] = PoolEntry.objects.filter(pool=pool)
        return context


class PoolEntrySelectView(LoginRequiredMixin, generic.DetailView):
    model = Pool
    template_name = 'vetbekje/pool_entry_select.html'

    def get_context_data(self, **kwargs):
        context = super(PoolEntrySelectView, self).get_context_data(**kwargs)
        context['media_root'] = MEDIA_ROOT

        pool = context['pool']

        entries = PoolEntry.objects.filter(pool=pool)

        profiles = list(Profile.objects.all())
        added = []

        for entry in entries:
            index = profiles.index(entry.profile)
            added.append(profiles.pop(index))

        context['added'] = added
        context['unadded'] = profiles
        print(profiles)
        print(added)
        return context
