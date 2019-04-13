from django.conf.urls import url, include
from django.contrib import admin
from . import views

app_name = 'picnic'

urlpatterns = [
    # picnic/
    url(r'^$', views.IndexView.as_view(), name='index-total'),

    url(r'^mylist/$', views.MyIndexView.as_view(), name='index'),

    # picnic/item/list/
    url(r'^item/list$', views.ItemListView.as_view(), name='item-list'),

    # picnic/profile/edit
    url(r'^profile/edit/', views.update_profile, name='profile-edit'),

    # picnic/list/order/#
    url(r'^list/order/(?P<pk>[0-9]+)/$', views.OverviewOrderView.as_view(), name='list-order'),

    # picnic/list/notify/
    url(r'^list/notify/(?P<pk>[0-9]+)/$', views.notify_view, name='list-notify'),

    # picnic/list/order/details/#
    url(r'^list/order/detail/(?P<pk>[0-9]+)/$', views.DetailOrderView.as_view(), name='list-order-detail'),

    # picnic/list/order/finish/
    url(r'^list/order/finish/$', views.finish_order_view, name='list-order-finish'),

    # picnic/list/order/#/done/
    url(r'^list/order/(?P<pk>[0-9]+)/done/$', views.OrderDoneView.as_view(), name='list-order-done'),

    # picnic/list/add/
    url(r'^list/add/$', views.ListFormView.as_view(), name='list-add'),

    # picnic/item/#/subtract-from-list
    url(r'^item/(?P<pk>[0-9]+)/subtract-from-list/$', views.subtract_item_from_list_view, name='subtract-from-list'),

    # picnic/item/#/remove-from-list
    url(r'^item/(?P<pk>[0-9]+)/remove-from-list/$', views.remove_item_from_list_view, name='remove-from-list'),

    # picnic/item/#/add-to-list
    url(r'^item/(?P<pk>[0-9]+)/add-to-list/$', views.add_item_to_list_view, name='add-to-list'),

    # picnic/item/#/
    url(r'^item/(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),

    # picnic/item/#/remove/
    url(r'^item/(?P<pk>[0-9]+)/remove/$', views.remove_item, name='item-remove'),

    # picnic/item/#/edit/
    url(r'^item/(?P<pk>[0-9]+)/edit/$', views.ItemUpdate.as_view(), name='item-edit'),

    # picnic/register/
    url(r'^register/$', views.UserFormView.as_view(), name='register'),

    # picnic/login/
    url(r'^login/$', views.LoginFormView.as_view(), name='login'),

    # picnic/logout/
    url(r'^logout/$', views.logout_view, name='logout'),

    # picnic/item/add/
    url(r'^item/add/$', views.ItemFormView.as_view(), name='item-add')
]
#http://stieltjes15.pythonanywhere.com/picnic/list/order/detail/28/