from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.views import generic
from django.views.generic import View
from .models import List, Item, ListItem, Profile
from .forms import UserForm, ProfileForm, LoginForm, ItemForm, ListForm
from django.core.urlresolvers import reverse
from urllib.parse import urlencode
from django.core.mail import EmailMessage
from functools import reduce
from django.db.models import Q
import datetime
import operator

def logout_view(request):
    logout(request)
    return redirect('home')


def url_with_querystring(path, **kwargs):
    return path + '?' + urlencode(kwargs)

@login_required
def remove_item(request, pk):
    item = Item.objects.get(pk=pk)
    item.delete()

    messages.warning(request, 'Removed ' + str(item.name) + ' permanently!')

    return redirect('picnic:index')

@login_required
def find_item_on_list(request, pk):
    item = Item.objects.get(pk=pk)
    profile = Profile.objects.get(user=request.user)
    list = List.objects.get(is_ordered=False)

    try:
        list_item = ListItem.objects.get(item=item, profile=profile, list=list)
    except ListItem.DoesNotExist:
        list_item = ListItem(item=item, profile=profile, list=list)

    return list_item

@login_required
def update_profile(request):
    if request.method == 'POST':
        profile = Profile.objects.get(user=request.user)
        form = ProfileForm(data=request.POST, files=request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated!')
            return redirect(reverse('picnic:index'))
        else:
            messages.error(request, 'Invalid Upload!')

    else:
        form = ProfileForm(instance=request.user)

    return render(request, 'picnic/registration_form.html', {'form': form})

@login_required
def notify_view(request, pk):
    list = List.objects.get(pk=pk)

    profile = list.admin
    time_left = 20 - (datetime.datetime.now().hour - 1)

    text = 'Beste ' + profile.user.first_name + ',\n\n'
    text += request.user.first_name + ' wilt je er aan herinneren dat je vandaag zou bestellen.'
    text += ' Je hebt nog ' + str(time_left) + ' uur om te bestellen. Beter verzaak je niet!\n'
    text += '\nGroeten,\nStieltjes15'

    email = EmailMessage('Vergeet niet te bestellen vandaag!', text, to=[profile.user.email])
    email.send()

    return redirect('picnic:index')

@login_required
def get_url_with_query(request):
    q = request.GET.get('q')

    if not q:
        q = ''

    print(q)

    return url_with_querystring(reverse('picnic:index'), q=q)

@login_required
def change_item_on_list(request, pk, amount):

    list_item = find_item_on_list(request, pk)
    list_item.quantity += amount

    if(list_item.quantity > 0):
        list_item.save()
        if list_item.quantity == 1 and amount == 1:
            messages.success(request, 'Added ' + str(list_item.item.name) + ' to your list')
        elif amount > 0:
            messages.info(request, 'Added ' + str(amount) + ' ' + str(list_item.item.name))
        else:
            messages.info(request, 'Removed ' + str(-amount) + ' ' + str(list_item.item.name))
    else:
        list_item.delete()
        messages.warning(request, 'Removed ' + str(list_item.item.name) + ' from your list')

    return redirect(get_url_with_query(request))


@login_required
def add_item_to_list_view(request, pk):
    return change_item_on_list(request, pk, 1)

@login_required
def remove_item_from_list_view(request, pk):
    list_item = find_item_on_list(request, pk)
    list_item.delete()

    messages.warning(request, 'Removed ' + str(list_item.item.name) + ' from your list')

    return redirect(get_url_with_query(request))


@login_required
def subtract_item_from_list_view(request, pk):
    return change_item_on_list(request, pk, -1)


def order_mail_text(request, profile, cost):
    text = 'Beste ' + profile.user.first_name + ',\n\n'
    text += request.user.first_name + ' heeft de bestelling doorgezet.'
    text += ' Je totale kosten zijn \u20ac'
    text += str(cost) + '. Hier heb je een overzicht van je zooi:\n\n'
    for item in profile.objects:
        text += '\u2022 ' + str(item) + '\n'

    text += '\nGroeten,\nStieltjes15'
    return text

# Send an email to all relevant profiles
def send_order_mail(request, list):
    profiles = []
    costs = []
    for list_item in ListItem.objects.filter(list=list):
        p = list_item.profile
        item_price = list_item.item.price * list_item.quantity

        if not p in profiles:
            profiles.append(p)
            costs.append(item_price)
        else:
            costs[profiles.index(p)] += item_price

    i = 0
    for profile in profiles:
        profile.objects = ListItem.objects.filter(list=list, profile=profile)

        if not list.is_ordered:
            email = EmailMessage('Picnic Bestelling Geplaatst', order_mail_text(request, profile, costs[i]), to=[profile.user.email])
            email.send()

        i += 1


@login_required
def finish_order_view(request):
    list = List.objects.get(is_ordered=False)
    send_order_mail(request, list)
    list.is_ordered = True
    list.admin = Profile.objects.get(user=request.user)

    list.save()
    messages.success(request, 'Order Confirmed!')
    return redirect('picnic:list-order-done', pk=list.pk)


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls):
        return login_required(super(LoginRequiredMixin, cls).as_view())


class IndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'picnic/index.html'

    def get_queryset(self):
        return List.objects.filter(is_ordered=False)

    def get_all_items(self, item, list):
        return ListItem.objects.filter(item=item, list=list)

    def get_active(self):
        return [True, False]

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        lists = context['object_list']

        if(lists):
            list = lists[0]
            quantities = []
            temp_list = []
            prices = []

            # Find the quantities per item
            for item in Item.objects.all():
                l = self.get_all_items(item, list)

                if l:
                    q = 0
                    for listitem in l:
                        q += listitem.quantity

                    temp_list.append(item)
                    quantities.append(q)
                    prices.append(q * item.price)

            if lists:
                context['object_list'] = list

            notify = (datetime.datetime.now().day == list.deadline.day)
            context['notify'] = notify

            context['prices'] = prices
            context['subtitle'] = List.str_deadline(list)
            context['item_list'] = temp_list
            context['quantities'] = quantities
            context['total'] = sum(prices)

        context['old_lists'] = List.objects.filter(is_ordered=True)[:5]
        context['search_list'] = ItemListView.get_queryset(self)
        context['active'] = self.get_active()
        return context


class MyIndexView(IndexView):

    def get_all_items(self, item, list):
        p = Profile.objects.filter(user=self.request.user)
        return ListItem.objects.filter(item=item, profile=p, list=list)

    def get_active(self):
        return [False, True]


class OverviewOrderView(generic.ListView):
    template_name = 'picnic/order.html'

    def get_queryset(self):
        return List.objects.get(pk=self.kwargs['pk'])

    def get_active(self):
        return [True, False]

    def get_context_data(self, **kwargs):
        context = super(OverviewOrderView, self).get_context_data(**kwargs)
        list = self.get_queryset()

        profiles = []
        costs = []
        for list_item in ListItem.objects.filter(list=list):
            p = list_item.profile
            item_price = list_item.item.price * list_item.quantity

            if not p in profiles:
                profiles.append(p)
                costs.append(item_price)
            else:
                costs[profiles.index(p)] += item_price

        for profile in profiles:
            profile.objects = ListItem.objects.filter(list=list, profile=profile)

        context['costs'] = costs
        context['total'] = sum(costs)
        context['profiles'] = profiles
        context['is_ordered'] = list.is_ordered
        context['active'] = self.get_active()

        return context


class DetailOrderView(OverviewOrderView):

    def get_active(self):
        return [False, True]


class ItemListView(LoginRequiredMixin, generic.ListView):
    template_name = 'picnic/index.html'
    paginate_by = 20

    def get_queryset(self):
        result = Item.objects.all()

        query = self.request.GET.get('q')
        if query:
            query_list = query.split()
            result = result.filter(reduce(operator.and_, (Q(name__icontains=q) for q in query_list)))

        return result


class DetailView(LoginRequiredMixin, generic.DetailView):
    model = Item
    template_name = 'picnic/item_detail.html'


class OrderDoneView(LoginRequiredMixin, View):
    template_name = 'picnic/order_done.html'
    context_object_name = 'pk'

    def get(self, request, **kwargs):
        pk = self.kwargs['pk']
        return render(request, self.template_name, {'pk':pk})

# Item creation view
class ItemFormView(LoginRequiredMixin, CreateView):
    model = Item
    form_class = ItemForm


class ListFormView(LoginRequiredMixin, CreateView):
    model = List
    form_class = ListForm

    def post(self, request):
        form_data = ListForm(request.POST)

        if(form_data.is_valid()):
            list = form_data.save(commit=False)
            list.creation_date = datetime.datetime.now().date()

            # Ensure that no other list is still unordered
            try:
                other_list = List.objects.get(is_ordered=False)
                other_list.is_ordered = False
                other_list.save()
                list.save()
            except List.DoesNotExist:
                list.save()
        else:
            messages.error(request, 'Given date is not valid!')
            return redirect('picnic:list-add')

        return redirect('picnic:index')

class ItemUpdate(UpdateView):
    form_class = ItemForm
    template_name = 'picnic/item_form.html'
    model = Item

    def form_valid(self, form):
        super(ItemUpdate, self).form_valid(form)
        messages.success(self.request, 'Item edit succesful')
        return redirect('picnic:detail', pk=self.object.pk)


# Log a user in
class LoginFormView(View):
    form_class = LoginForm
    template_name = 'picnic/login_form.html'

    def get(self, request):
        if request.user.is_authenticated():
            return redirect('picnic:index')

        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:

                if user.is_active:
                    login(request, user)
                    redirect_to = self.request.GET.get('next')
                    if(redirect_to):
                        return redirect(redirect_to)
                    else:
                        return redirect('picnic:index')
        else:
            return render(request, self.template_name, {'form': request.POST})

# Register a user
class UserFormView(View):
    template_name = 'picnic/registration_form.html'

    # On submit
    def post(self, request):
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST)

        # If the data is valid
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            profile = profile_form.save(commit=False)

            username = user_form.cleaned_data['username']
            password = user_form.cleaned_data['password']
            user.username = username
            user.set_password(password)
            user.save()

            profile.user = user

            user = authenticate(username=username, password=password)

            if user is not None:

                if user.is_active:
                    login(request, user)
                    return redirect('picnic:index')
        else:
            return render(request, self.template_name, {
                'user_form': user_form,
                'profile_form': profile_form,
            })

    # Loading the page first, give them an empty form
    def get(self, request):
        user_form = UserForm(None)
        profile_form = ProfileForm(None)
        return render(request, self.template_name, {
            'user_form': user_form,
            'profile_form': profile_form,
        })


# class UserFormView(View):
#     form_class = UserForm
#     template_name = 'shoplist/registration_form.html'
#
#     # Display blank form
#     def get(self, request):
#         form = self.form_class(None)
#         return render(request, self.template_name, {'form':form})
#
#     # Process form data
#     def post(self, request):
#         form = self.form_class(request.POST)
#
#         if form.is_valid():
#             user = form.save(commit=False)
#
#             # cleaned (normalised) data
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#             user.username = username
#             user.set_password(password)
#             user.save()
#
#             # returns User objects if credentials are correct
#             user = authenticate(username=username, password=password)
#
#             if user is not None:
#
#                 if user.is_active:
#                     login(request, user)
#                     return redirect('shoplist:index')
#
#         return render(request, self.template_name, {'form': form})