from django.conf.urls import url, include
from . import views

app_name = 'dinner'

urlpatterns = [
    # /dinner/index/0
    url(r'^index/(?P<pk>[0-9]+)/$', views.IndexView.as_view(), name='index'),

    # /dinner/bij/0
    url(r'^bij/(?P<pk>[0-9]+)/$', views.bij_view, name='bij'),

    url(r'^feut/(?P<pk>[0-9]+)/$', views.feut_view, name='feut'),

    url(r'^recipe/add/$', views.RecipeFormView.as_view(), name='recipe-add'),

    url(r'^recipe/(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='recipe-detail'),

    url(r'^recipe/(?P<pk>[0-9]+)/remove/$', views.remove_recipe, name='recipe-remove'),

    url(r'^recipe/(?P<pk>[0-9]+)/edit/$', views.RecipeUpdate.as_view(), name='recipe-edit')
]