from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import redirect
from picnic.models import Profile
from django.views import generic
from dinner.models import DinnerDate, Recipe
from dinner.forms import RecipeForm
from datetime import timedelta, datetime
from django.contrib import messages
from picnic.views import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from functools import reduce
from django.db.models import Q
import operator


def remove_feut(d, p, M):
    for feut in d.boodschap_feuten.all():
        feut.boodschap_stand -= 1 / M
        feut.save()

    d.boodschap_feuten.remove(p)

    M -= 1
    if M > 0:
        for feut in d.boodschap_feuten.all():
            feut.boodschap_stand += 1 / M
            feut.save()

@login_required
def remove_recipe(request, pk):
    recipe = Recipe.objects.get(pk=pk)
    recipe.delete()

    messages.warning(request, 'Removed ' + str(recipe.name) + ' permanently!')

    return redirect('dinner:index', pk=0)

@login_required
def bij_view(request, pk):
    d = DinnerDate.objects.get(pk=pk)

    p = Profile.objects.get(user=request.user)
    N = len(d.profiles.all())
    if p in d.profiles.all():

        for prof in d.profiles.all():
            prof.boodschap_stand += 1 / N
            prof.save()

        if (p in d.boodschap_feuten.all()):
            remove_feut(d, p, len(d.boodschap_feuten.all()))
        d.profiles.remove(p)

        N -= 1
        for prof in d.profiles.all():
            prof.boodschap_stand -= 1 / N
            prof.save()

    else:
        if (d.date == datetime.today().date() and datetime.now().hour >= 19):
            messages.error(request,
                           "Je bent te laat lul, doe ff optijd invullen volgende keer (voor 4u). Ga maar smeken op de app.")
            return redirect('dinner:index', pk=pk)

        if(N > 0):
            for prof in d.profiles.all():
                prof.boodschap_stand += 1 / N
                prof.save()

        d.profiles.add(p)

        N += 1
        for prof in d.profiles.all():
            prof.boodschap_stand -= 1 / N
            prof.save()

    d.save()

    return redirect('dinner:index', pk=pk)

@login_required
def feut_view(request, pk):
    d = DinnerDate.objects.get(pk=pk)

    p = Profile.objects.get(user=request.user)
    M = len(d.boodschap_feuten.all())
    if p in d.boodschap_feuten.all():
        remove_feut(d, p, M)
    else:
        if (d.date == datetime.today().date() and datetime.now().hour >= 22):
            messages.error(request,
                           "Ja viezerik, opbokken.")
            return redirect('dinner:index', pk=pk)

        if M > 0:
            for feut in d.boodschap_feuten.all():
                feut.boodschap_stand -= 1 / M
                feut.save()

        d.boodschap_feuten.add(p)
        M += 1

        for feut in d.boodschap_feuten.all():
            feut.boodschap_stand += 1 / M
            feut.save()

    d.save()

    return redirect('dinner:index', pk=pk)

class IndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'dinner/index.html'

    def get_queryset(self):
        startdate = datetime.today()
        enddate = startdate + timedelta(days=6)
        return DinnerDate.objects.filter(date__range=[startdate, enddate])

    def get_feut_list(self, day):
        feutlist = []
        for feut in day.profiles.all():
            if feut in day.boodschap_feuten.all():
                feutlist.append(True)
            else:
                feutlist.append(False)

        return feutlist

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        list = self.get_queryset()
        startdate = datetime.today()

        i = len(list)
        while i < 6:
            l = DinnerDate(date=startdate + timedelta(days=i))
            l.save()
            i += 1

        pk = int(self.kwargs['pk'])
        d = DinnerDate.objects.filter(pk=pk)
        if not d:
            pk = DinnerDate.objects.get(date=startdate).pk

        d = DinnerDate.objects.get(pk=pk)
        p = Profile.objects.get(user=self.request.user)

        if p in d.profiles.all():
            context['bij'] = 0

            if(p.boodschap_stand <= -1):
                messages.info(self.request, "Je staat laag, beter doe je boodschappen")
        else:
            context['bij'] = 1

        if p in d.boodschap_feuten.all():
            context['feut'] = 0
        else:
            context['feut'] = 1


        context['is_feut'] = self.get_feut_list(d)


        query = DinnerDateListView.get_queryset(self)
        print(query)
        recipe_list = RecipeListView.get_queryset(self)
        if(query):
            old_feuten = self.get_feut_list(query)
        else:
            old_feuten = []

        context['old_feuten'] = old_feuten
        context['feuten'] = d.boodschap_feuten.all()
        context['date'] = d.date
        context['recipe_list'] = recipe_list
        context['search'] = query
        context['search_day'] = query
        context['active'] = pk
        context['profiles'] = d.profiles.all()

        return context

class DinnerDateListView(LoginRequiredMixin, generic.ListView):
    template_name = 'dinner/index.html'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q')

        if not query:
            return []

        try:
            date = datetime.strptime(query, "%d-%m-%Y").date()
        except ValueError:
            if query.lower() == "vandaag":
                date = datetime.now().date()
            elif query.lower() == "morgen":
                date = datetime.now().date() + timedelta(days=1)
                # date = date.date()
            else:
                messages.error(self.request, 'Je hebt poep ingevuld. Ples.')
                return []


        try:
            result = DinnerDate.objects.get(date=date)
        except DinnerDate.DoesNotExist:
            messages.error(self.request, 'Die datum heb ik nie, voer datum in als: d-m-yyyy')
            return []

        if not result.profiles.all():
            messages.warning(self.request, 'Datum bestaat, maar niemand at mee')

        return result

class RecipeUpdate(UpdateView):
    form_class = RecipeForm
    template_name = 'dinner/recipe_form.html'
    model = Recipe

    def form_valid(self, form):
        super(RecipeUpdate, self).form_valid(form)
        messages.success(self.request, 'Recipe edit succesful')
        return redirect('dinner:index', pk=0)

# Item creation view
class RecipeFormView(LoginRequiredMixin, CreateView):
    model = Recipe
    form_class = RecipeForm


class DetailView(LoginRequiredMixin, generic.DetailView):
    model = Recipe
    template_name = 'dinner/recipe_detail.html'


class RecipeListView(LoginRequiredMixin, generic.ListView):
    template_name = 'dinner/index.html'
    paginate_by = 20

    def get_queryset(self):
        result = Recipe.objects.all()
        query = self.request.GET.get('q2')

        if query:
            query_list = query.split()
            result = result.filter(reduce(operator.and_, (Q(name__icontains=q) | Q(foodtype__icontains=q) for q in query_list)))


        return result

