from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^edit_readers/$', views.EditReadersView.as_view(), name='edit_readers'),
    url(r'^prepare_table/$', views.PrepareTableView.as_view(), name='prepare_table'),
    url(r'^successfully_logged_out/$', views.LoggedOutView.as_view(), name='logged_out')
]
