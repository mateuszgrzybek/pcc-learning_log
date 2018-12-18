"""Definiuje wzory URL dla learning_logs"""

from django.conf.urls import url

from . import views

urlpatterns = [
    # Strona główna
    url(r'^$', views.index, name='index'),

    # Pokaż wszystkie tematy
    url(r'^topics/$', views.topics, name='topics'),

    # Strona z detalami danego tematu
    url(r'^topics/(?P<topic_id>\d+)/$', views.topic, name='topic'),

    # Strona do tworzenia nowego tematu
    url(r'^new_topic/$', views.new_topic, name='new_topic'),

    # Strona do doawania nowych wpisów
    url(r'^new_entry/(?P<topic_id>\d+)/$', views.new_entry, name='new_entry'),

    # Strona do edycji wpisów
    url(r'^edit_entry/(?P<entry_id>\d+)/$', views.edit_entry, name='edit_entry'),
]
