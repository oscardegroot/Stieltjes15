from django.conf.urls import url, include
from django.contrib import admin
from . import views

app_name = 'vetbekje'

urlpatterns = [
    # vetbekje/
    url(r'^index/', views.IndexView.as_view(), name='index'),

    url(r'^target/(?P<pk>[0-9]+)/$', views.BattleFormView.as_view(), name='target'),

    url(r'^pool/new/$', views.PoolFormView.as_view(), name='pool-new'),

    url(r'^pool/(?P<pk>[0-9]+)/detail/$', views.PoolDetailView.as_view(), name='pool-detail'),

    url(r'^geschil/(?P<pk>[0-9]+)/$', views.BattleDetailView.as_view(), name='battle-detail'),

    url(r'^geschil/(?P<pk>[0-9]+)/win/(?P<target_won>[0-9]+)/$', views.win_battle_view, name='battle-win')
]
