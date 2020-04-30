from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
# from pusher import Pusher
from django.http import JsonResponse, HttpResponse
from decouple import config
from django.contrib.auth.models import User
from .models import *
from rest_framework.decorators import api_view
import json

# instantiate pusher
# pusher = Pusher(app_id=config('PUSHER_APP_ID'), key=config('PUSHER_KEY'), secret=config('PUSHER_SECRET'), cluster=config('PUSHER_CLUSTER'))

@csrf_exempt
@api_view(["GET"])
def initialize(request):
    user = request.user
    player = user.player
    player_id = player.id
    uuid = player.uuid
    room = player.room()
    players = room.playerNames(player_id)
    room_data = room.play_map
    return JsonResponse({'uuid': uuid, 'name':player.user.username, 'title':room.title, 'description':room.description, 'players':players, 'map':room_data}, safe=True)


@csrf_exempt
@api_view(["POST"])
def move(request):
    dirs={"n": "north", "s": "south", "e": "east", "w": "west"}
    reverse_dirs = {"n": "south", "s": "north", "e": "west", "w": "east"}
    player = request.user.player
    player_id = player.id
    player_uuid = player.uuid
    data = request.data
    direction = data['direction']
    room = player.room()
    nextRoomID = None
    if direction == "n":
        if world.check_room(curr_room=room, direction=direction):
            nextRoomID = world.grid[tuple(world.change_coords(curr_room=room, direction=direction))].id
        else:
            nextRoomID = world.generate_room(curr_room=room, direction=direction).id
    elif direction == "s":
        if world.check_room(curr_room=room, direction=direction):
            nextRoomID = world.grid[tuple(world.change_coords(curr_room=room, direction=direction))].id
        else:
            nextRoomID = world.generate_room(curr_room=room, direction=direction).id
    elif direction == "e":
        if world.check_room(curr_room=room, direction=direction):
            nextRoomID = world.grid[tuple(world.change_coords(curr_room=room, direction=direction))].id
        else:
            nextRoomID = world.generate_room(curr_room=room, direction=direction).id
    elif direction == "w":
        if world.check_room(curr_room=room, direction=direction):
            nextRoomID = world.grid[tuple(world.change_coords(curr_room=room, direction=direction))].id
        else:
            nextRoomID = world.generate_room(curr_room=room, direction=direction).id
    if nextRoomID is not None and nextRoomID > 0:
        nextRoom = Room.objects.get(id=nextRoomID)
        player.currentRoom=nextRoomID
        player.save()
        players = nextRoom.playerNames(player_id)
        currentPlayerUUIDs = room.playerUUIDs(player_id)
        nextPlayerUUIDs = nextRoom.playerUUIDs(player_id)
        # for p_uuid in currentPlayerUUIDs:
        #     pusher.trigger(f'p-channel-{p_uuid}', u'broadcast', {'message':f'{player.user.username} has walked {dirs[direction]}.'})
        # for p_uuid in nextPlayerUUIDs:
        #     pusher.trigger(f'p-channel-{p_uuid}', u'broadcast', {'message':f'{player.user.username} has entered from the {reverse_dirs[direction]}.'})
        return JsonResponse({'name':player.user.username, 'title':nextRoom.title, 'description':nextRoom.description, 'players':players, 'error_msg':""}, safe=True)
    else:
        players = room.playerNames(player_id)
        return JsonResponse({'name':player.user.username, 'title':room.title, 'description':room.description, 'players':players, 'error_msg':"You cannot move that way."}, safe=True)

@csrf_exempt
@api_view(["POST"])
def say(request):
    # IMPLEMENT
    return JsonResponse({'error':"Not yet implemented"}, safe=True, status=500)

from .world import World
