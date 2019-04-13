from django.conf.urls import url, include
from . import views

app_name = 'pilsbazen'

urlpatterns = [
    # /pilsbazen/index/#/
    url(r'^index/(?P<pk>[0-9]+)/$', views.IndexView.as_view(), name='index'),

    # /pilsbazen/turf/#from#on#/
    url(r'^index/(?P<amount>[0-9]+)from(?P<baas>[0-9]+)to(?P<turver>[0-9]+)/$', views.turf_view, name='turf'),

    # /pilsbazen/stand/
    url(r'^stand/$', views.StandView.as_view(), name='stand'),

    # /pilsbazen/stand/
    url(r'^stand/mail/$', views.mail_stand_view, name='stand-mail'),
]