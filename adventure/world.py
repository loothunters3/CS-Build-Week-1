# Sample Python code that can be used to generate rooms in
# a zig-zag pattern.
#
# You can modify generate_rooms() to create your own
# procedural generation algorithm and use print_rooms()
# to see the world.

from .util import gen_room
from django.contrib.auth.models import User
from adventure.models import Player, Room
import random

# class Room:
#     def __init__(self, id, name, description, x, y, map, room_doors, terrain, objects_):
#         self.id = id
#         self.name = name
#         self.description = description
#         self.play_map = map
#         self.doors = room_doors
#         self.terrain=terrain
#         self.room_objs = objects_
#         self.x = x
#         self.y = y

#     def __repr__(self):
#         s = f"name={self.name}\ndesc={self.desc}\nterrain={self.terrain}\ndoors={self.doors}\ncoords=({self.x},{self.y})"
#         return f"({self.x}, {self.y})"


class World:
    def __init__(self, seed=None, limit=None):
        self.grid = {}
        self.seed = seed
        self.limit = limit if limit is not None else 501
        self.num_of_rooms = 1
        self.generate_starting_room()

    def generate_starting_room(self):
        targ_coords = [0,0]
        # generate the room from the seed and pervious doors
        room_map, room_doors, room_objs = gen_room(seed=self.seed, prev_doors=[])

        # Generate random room name/desc/terrain
        room_terrain = random.randint(1,4)
        room_name, room_desc = self.gen_name_description(room_terrain)

        new_room = Room(name=room_name, 
                        description=room_desc,
                        x=targ_coords[0],
                        y=targ_coords[1],
                        map=room_map,
                        room_doors=room_doors,
                        terrain=room_terrain,
                        objects_in_room=room_objs)

        # save the new room
        new_room.save()
        # add the new room to the grid at the target coords
        self.grid[targ_coords] = new_room

        return new_room

    def check_room(self, curr_room, direction):
        # Change coordinates to target room's coordinates
        targ_coords = self.change_coords(curr_room=curr_room, direction=direction)
        # Check if those coordinates are in the map grid
        # If they are, return true. Else return false
        if targ_coords in self.grid:
            return True
        else:
            return False

    def generate_room(self, curr_room, direction):
        if self.num_of_rooms + 1 >= self.limit:
            return curr_room
        targ_coords = self.change_coords(curr_room=curr_room, direction=direction)
        doors_to_coord = []

        # find coordinates of room to north
        coord_n = change_coords(direction='n', curr_coords=targ_coords)
        # Check if northern coords are in grid
        # (room is already generated)
        if coord_n in self.grid:
            # append the coordinates of the door going south in the play map
            # in the room to the north of the target coordinates
            doors_to_coord.append(self.grid[coord_n]['doors']['s'])

        # find coordinates of room to east
        coord_e = change_coords(direction='e', curr_coords=targ_coords)
        # Check if eastern coords are in grid
        # (room is already generated)
        if coord_e in self.grid:
            # append the coordinates of the door going west in the play map
            # in the room to the east of the target coordinates
            doors_to_coord.append(self.grid[coord_e]['doors']['w'])

        # find coordinates of room to south
        coord_s = change_coords(direction='s', curr_coords=targ_coords)
        # Check if southern coords are in grid
        # (room is already generated)
        if coord_s in self.grid:
            # append the coordinates of the door going north in the play map
            # in the room to the south of the target coordinates
            doors_to_coord.append(self.grid[coord_s]['doors']['n'])

        # find coordinates of room to west
        coord_w = change_coords(direction='w', curr_coords=targ_coords)
        # Check if western coords are in grid
        # (room is already generated)
        if coord_w in self.grid:
            # append the coordinates of the door going east in the play map
            # in the room to the west of the target coordinates
            doors_to_coord.append(self.grid[coord_w]['doors']['e'])


        # generate the room from the seed and pervious doors
        room_map, room_doors, room_objs = gen_room(seed=self.seed, prev_doors=doors_to_coord)

        # Generate random room name/desc/terrain
        room_terrain = random.randint(1,4)
        room_name, room_desc = self.gen_name_description(room_terrain)

        # Instantiate the new room with all the randomly generated stuff
        new_room = Room(name=room_name, 
                        description=room_desc,
                        x=targ_coords[0],
                        y=targ_coords[1],
                        map=room_map,
                        room_doors=room_doors,
                        terrain=room_terrain,
                        objects_=room_objs)

        # save the new room
        new_room.save()
        # add the new room to the grid at the target coords
        self.grid[targ_coords] = new_room

        # increment the num_of_rooms counter by 1
        self.num_of_rooms += 1

        # return the new room
        return new_room

    def change_coords(self, direction, curr_room=None, curr_coords=None):
        # If current room was passed, use that room's data
        if curr_room is not None:
            targ_coords = [curr_room.x, current_room.y]
        # Else if the current coordinates were passed, use those
        elif curr_coords is not None:
            targ_coords = curr_coords
        # Else return 
        else:
            return

        # Check the direction and modify the x,y coordinate accordingly
        if direction == 'n':
            targ_coords[1] += 1
        elif direction == 'e':
            targ_coords[0] += 1
        elif direction == 's':
            targ_coords[1] -= 1
        elif direction == 'w':
            targ_coords[0] -= 1

        # return the modified coordinates
        return targ_coords

    def gen_name_description(rooms):
        descriptions = []
        names = []
        for room in rooms:
            if room == 1:
                room_description = f"You are now in an {', '.join(random.sample(desert, 2))} {random.sample(desert_noun, 1)[0]}. Do you see any treasures or should you move on?"
                room_name = f'{random.same(desert_name)}'
            elif room == 2:
                room_description = f"You are now in an {', '.join(random.sample(spring, 2))} {random.sample(spring_noun, 1)[0]}. Do you see any treasures or should you move on?"
                room_name = f'{random.same(spring_name)}'
            elif room == 3:
                room_description = f"You are now in an {', '.join(random.sample(snowy, 2))} {random.sample(snowy_noun, 1)[0]}. Do you see any treasures or should you move on?"
                room_name = f'{random.same(snowy_name)}'
            else:
                room_description = f"You are now in an {', '.join(random.sample(grave_yard, 2))} {random.sample(grave_yard_noun, 1)[0]}. Do you see any treasures or should you move on?"
                room_name = f'{random.same(grave_yard_name)}'
            descriptions.append(room_description)
            names.append(room_name)
        return descriptions,names
    

w = World()
