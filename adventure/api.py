from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
# from pusher import Pusher
from django.http import JsonResponse, HttpResponse
from decouple import config
from django.contrib.auth.models import User
from .models import *
from rest_framework.decorators import api_view
import json
from .util import generate_starting_room, change_coords

# instantiate pusher
# pusher = Pusher(app_id=config('PUSHER_APP_ID'), key=config('PUSHER_KEY'), secret=config('PUSHER_SECRET'), cluster=config('PUSHER_CLUSTER'))

@csrf_exempt
@api_view(["GET"])
def initialize(request):
    user = request.user
    player = user.player
    player_id = player.id
    uuid = player.uuid
    if player.currentRoom == -1:
        gen_world(user, player)

    room = Room.objects.get(id=player.currentRoom)
    players = room.playerNames(player_id)
    room_map = room.play_map
    return JsonResponse({'uuid': uuid, 'name':player.user.username, 'title':room.title, 'description':room.description, 'players':players, 'map':room_map}, safe=True)

def gen_world(user, player):
    wm = World_Model()
    wm.save()
    start_room = generate_starting_room(wm)
    wm.coords ={'[0, 0]': str(start_room.id)}
    wm.users.add(user)
    wm.save()
    if player.currentWorld:
        player.currentWorld.delete()
    player.currentRoom = start_room.id
    player.currentWorld = wm
    player.save()

@csrf_exempt
@api_view(["POST"])
def reset_world(request):
    user = request.user
    player = user.player
    gen_world(user, player)
    return HttpResponse(status=200)


# Get and set of player characters
@csrf_exempt
@api_view(["PUT"])
def set_player_char(request):
    player = request.user.player
    player.char_id = request.data['char_id']
    player.save()
    return HttpResponse(status=200)

@csrf_exempt
@api_view(["GET"])
def get_player_char(request):
    player = request.user.player
    return JsonResponse({"char_id":player.char_id}, status=200, safe=True)

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
    cw = player.currentWorld
    room = Room.objects.get(id=player.currentRoom)
    nextRoomID = None

    if cw.check_room(curr_room=room, direction=direction):
        targ_coords = change_coords(direction=direction, curr_room=room)
        nextRoomID = cw.coords[str(targ_coords)]
    else:
        nextRoomID = cw.generate_room(curr_room=room, direction=direction)
            
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

@csrf_exempt
@api_view(["POST"])
def say(request):
    # IMPLEMENT
    return JsonResponse({'error':"Not yet implemented"}, safe=True, status=500)

@csrf_exempt
@api_view(["GET"])
def get_map(request):
    player = request.user.player
    world = player.currentWorld
    
    x_min = 0
    y_min = 0
    x_max = 0
    y_max = 0

    for coord in world.coords:
        coord = eval(coord)
        x_min = coord[0] if coord[0] < x_min else x_min
        y_min = coord[1] if coord[1] < y_min else y_min
        x_max = coord[0] if coord[0] > x_max else x_max
        y_max = coord[1] if coord[1] > y_max else y_max

    map_grid = [list([0]*(x_max+1+abs(x_min))) for x in range(y_min,y_max+1)]

    for coord, value in world.coords.items():
        coord = eval(coord)
        value = Room.objects.get(id=int(value))
        value_data = {}
        value_data['title'] = value.title
        value_data['chests'] = list(eval(value.objects_in_room).values()).count(16)
        map_grid[coord[1]+abs(y_min)][coord[0]+abs(x_min)] = value_data

    map_grid.reverse()

    return JsonResponse({'map':map_grid}, safe=True)