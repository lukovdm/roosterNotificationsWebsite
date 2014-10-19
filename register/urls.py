from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns('',
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^add_user$',views.add ,name="add"),
    url(r'^remove_user$',views.remove ,name="remove"),
    #url(r'^update_user$', name="update"),
)