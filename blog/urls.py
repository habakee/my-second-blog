from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.post_list, name='post_list'),
    url(r'^wait/$', views.wait, name='wait'),
    url(r'^bar/$', views.bar, name='bar'),
    url(r'^line/$', views.line, name='line'),
    url(r'^pie/$', views.pie, name='pie'),
]