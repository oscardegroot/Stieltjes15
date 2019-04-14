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

    url(r'^geschil/(?P<pk>[0-9]+)/delete/$', views.delete_battle_view, name='battle-delete'),

    url(r'^pool/(?P<pk>[0-9]+)/delete/$', views.delete_pool_view, name='pool-delete'),

    url(r'^pool/(?P<pk>[0-9]+)/win/(?P<entry>[0-9]+)$', views.win_pool_view, name='pool-win'),

    url(r'^pool/(?P<pk>[0-9]+)/entry_select$', views.PoolEntrySelectView.as_view(), name='pool-entry-select'),

    url(r'^pool/(?P<pk>[0-9]+)/entry_add/(?P<profile_pk>[0-9]+)$', views.add_poolentry_view, name='pool-entry-add'),

    url(r'^pool/(?P<pk>[0-9]+)/entry_remove/(?P<profile_pk>[0-9]+)$', views.remove_poolentry_view, name='pool-entry-remove'),

    url(r'^geschil/(?P<pk>[0-9]+)/win/(?P<target_won>[0-9]+)/$', views.win_battle_view, name='battle-win')
]
