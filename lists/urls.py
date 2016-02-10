from django.conf.urls import url
from . import views as list_views

urlpatterns = [
    url(r'^new$', list_views.new_list, name='new_list'),
    url(r'^(?P<list_id>\d+)/$', list_views.view_list, name='view_list'),
    url(r'^(?P<list_id>\d+)/add_item$', list_views.add_item, name='add_item'),
]

