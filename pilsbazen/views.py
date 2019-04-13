from django.shortcuts import redirect
from picnic.models import Profile
from django.views import generic
from django.contrib import messages
from django.core.mail import EmailMessage

def turf_view(request, amount, baas, turver):
    amount = int(amount)

    try:
        p_baas = Profile.objects.get(pk=baas)
        p_turver = Profile.objects.get(pk=turver)

        p_baas.turfjes += amount
        p_baas.save()

        p_turver.turfjes -= amount
        p_turver.save()

        messages.success(request, str(amount) + ' geturft op ' + str(p_turver.user.first_name) + ' van ' + str(p_baas.user.first_name))

        return redirect('pilsbazen:index', pk=baas)
    except Exception as e:
        messages.error(request, 'Please select a pilsbaas first')

        return redirect('pilsbazen:index', pk=baas)

def mail_stand_view(request):
    text = 'Beste ' + request.user.first_name + ',\n\n'
    text += 'Bij deze een kopietje van de stand:\n'

    profiles = Profile.objects.all()
    for profile in profiles:
        text += '\u2022 ' + profile.user.first_name + ' ' + str(profile.turfjes) + '\n'

    text += '\nGroeten,\nStieltjes15'

    email = EmailMessage('Kopie van de Pilsstand', text, to=[request.user.email])
    email.send()

    messages.success(request, 'De stand is naar je gemaild')

    return redirect('pilsbazen:stand')

# Create your views here.
class IndexView(generic.ListView):
    template_name = 'pilsbazen/index.html'

    def get_queryset(self):
        return Profile.objects.all()

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        list = self.get_queryset()

        context['active'] = int(self.kwargs['pk'])

        context['values'] = [1, 24, 3]
        context['names'] = ['Pils', 'Krat', 'Speciaal']

        return context

class StandView(generic.ListView):
    template_name = 'pilsbazen/stand.html'

    def get_queryset(self):
        return Profile.objects.all()