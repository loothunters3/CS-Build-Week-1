from django.conf.urls import url
from . import api

urlpatterns = [
    url('init', api.initialize),
    url('move', api.move),
    url('say', api.say),
    url('getmap', api.get_map),
    # Generate a new world
    url('resetworld', api.reset_world),
    # Character Character get/set
    url('setplaychar', api.set_player_char),
    url('getplaychar', api.get_player_char)
]