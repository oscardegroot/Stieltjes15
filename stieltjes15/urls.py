"""stieltjes15 URL Configuration"""

from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from django.views.generic.base import TemplateView
from django.conf import settings

app_name = 'home'

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='picnic/home.html'), name='home'),
    url(r'^admin/', admin.site.urls),
    url(r'^picnic/', include('picnic.urls')),
    url(r'^vetbekje/', include('vetbekje.urls')),
    url(r'^pilsbazen/', include('pilsbazen.urls')),
    url(r'^dinner/', include('dinner.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
