from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^show_readers/$', views.ShowReadersView.as_view(), name='show_readers'),
    url(r'^reader/(?P<pk>[0-9]+)/delete_reader/$', views.DeleteReaderView.as_view(),
        name='delete_reader'),
    url(r'^reader/(?P<pk>[0-9]+)/$', views.ReaderDetailView.as_view(),
        name='reader_detail'),
    url(r'^prepare_table/$', views.PrepareTableView.as_view(), name='prepare_table'),
    url(r'^successfully_logged_out/$', views.LoggedOutView.as_view(),
        name='logged_out')
]
