from django.conf.urls import url
from . import api

urlpatterns = [
    url('init', api.initialize),
    url('move', api.move),
    url('say', api.say),
    url('getmap', api.get_map),
    url('genworld', api.gen_world)
]