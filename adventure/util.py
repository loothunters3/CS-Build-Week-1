import random

def gen_room(seed=None, prev_doors = []):
    x_size = 24
    y_size = 16
    map_ = [list(['.']*x_size) for x in range(0,y_size)]
    # Generate Edge Terrain
    for y in range(0,len(map_)):
        for x in range(0,len(map_[0])):
            # Top left corner
            if(y == 0 and x == 0):
                map_[y][x] = 1
            # Top right corner
            elif(y == 0 and x == x_size-1):
                map_[y][x] = 3
            # Top edge not corners
            elif(y == 0 and x != 0 and x != x_size-1):
                map_[y][x] = 2
            # Left edge not corners
            elif(y != 0 and y != y_size-1 and x == 0):
                map_[y][x] = 8
            # Right edge not corners
            elif(y != 0 and y != y_size-1 and x == x_size-1):
                map_[y][x] = 4
            # Bottom left corner
            elif(y == y_size-1 and x == 0):
                map_[y][x] = 7
            # Bottom right corner
            elif(y == y_size-1 and x == x_size-1):
                map_[y][x] = 5
            # Bottom edge not corners
            elif(y == y_size-1 and x != x_size-1 and x != 0):
                map_[y][x] = 6
    
    
    # Transfer the position of the previous door to its mirrored position in the new room

    current_doors = {}

    for door_coordinates in prev_doors.values():
        prev_door_x = door_coordinates[0]
        prev_door_y = door_coordinates[1]
        # left to right door
        if prev_door_x == 0:
            current_doors['e'] = [prev_door_y, prev_door_x + x_size-1]
            map_[prev_door_y][prev_door_x + x_size-1] = 10
        # Right to left door
        elif prev_door_x == x_size-1:
            current_doors['w'] = [prev_door_y, prev_door_x - x_size-1]
            map_[prev_door_y][prev_door_x - x_size-1] = 12
        # Top to bottom door
        elif prev_door_y == 0:
            current_doors['s'] = [prev_door_y + y_size - 1, prev_door_x]
            map_[prev_door_y + y_size - 1][prev_door_x] = 11
        # Bottom to top door
        elif prev_door_y == y_size-1:
            current_doors['n'] = [prev_door_y - y_size -1, prev_door_x]
            map_[prev_door_y - y_size -1][prev_door_x] = 9

    # Set the random modules seed
    random.seed(seed)

    num_new_doors = random.randint(0,4-len(current_doors))

    dirs = ['n','e','s','w']
    
    while num_new_doors > 0:
        target_dir = random.sample(dirs, 1)[0]
        if target_dir in current_doors:
            pass
        else:
            if target_dir == 'n':
                current_doors[target_dir] = [0, random.randint(1,x_size-2)]
                map_[current_doors[target_dir][0]][current_doors[target_dir][1]] = 9
            elif target_dir == 'e':
                current_doors[target_dir] = [random.randint(1,y_size-2), x_size-1]
                map_[current_doors[target_dir][0]][current_doors[target_dir][1]] = 10
            elif target_dir == 's':
                current_doors[target_dir] = [y_size-1, random.randint(1,x_size-2)]
                map_[current_doors[target_dir][0]][current_doors[target_dir][1]] = 11
            elif target_dir == 'w':
                current_doors[target_dir] = [random.randint(1,y_size-2), 0]
                map_[current_doors[target_dir][0]][current_doors[target_dir][1]] = 12
            num_new_doors -= 1

    # Generate positions of objects, 4 of each kind

    # Use a dict to store coords as its keys are a set
    object_coords = {}
    num_of_objects_to_gen = 12

    # Loop through 12 times
    for x in range(0, num_of_objects_to_gen+1):
        # Generate a random coordinate
        coord_obj = (random.randint(1,y_size-2), random.randint(1,x_size-2))

        # While the coordinate is in the keys of the dict, generate a new one
        while coord_obj in object_coords:
            coord_obj = (random.randint(1,y_size-2), random.randint(1,x_size-2))

        # Generate 4 of each kind of object
        if x % 3 == 0:
            object_coords[coord_obj] = 13
        elif x % 3 == 1:
            object_coords[coord_obj] = 14
        elif x % 3 == 2:
            object_coords[coord_obj] = 15
    
    # Generate initial chest coordinates
    chest_coords = (random.randint(1,y_size-2), random.randint(1,x_size-2))
    # while the chest_coords are in the keys of the dict, generate new coords
    while chest_coords in object_coords:
        chest_coords = (random.randint(1,y_size-2), random.randint(1,x_size-2))
    
    # Add chest coords to the dict
    object_coords[chest_coords] = 16

    # Test to see if a second chest will spawn (20% chance)
    if random.randint(0,100) >= 20:
        # Generate a second chest coordinates
        chest_coords = (random.randint(1,y_size-2), random.randint(1,x_size-2))
        # while the chest_coords are in the keys of the dict, generate new coords
        while chest_coords in object_coords:
            chest_coords = (random.randint(1,y_size-2), random.randint(1,x_size-2))

        # Add second chest coords to the dict
        object_coords[chest_coords] = 16

    # Change the map by adding object keys at coordinates in dict
    for key, value in object_coords.items():
        map_[key[0]][key[1]] = value


    # Print whole map in terminal
    for y in range(0,len(map_)):
        for x in range(0,len(map_[0])):
            print(map_[y][x], end='')

        print()

    return map_, current_doors, object_coords

class Descriptor:
    def __init__(self):
        self.desert = ['dry', 'hot', 'extreme', 'uninhabited', 'barren', 'bare', 'solitary', 'desolate', 'bleak', 'wanton',
            'bleak', 'unsmiling', 'sweltering', 'sterile', 'sandy', 'thorny', 'dismal', 'treeless', 'dried-up',
            'uncharted', 'flat', 'savage', 'empty', 'lifeless', 'lonesome', 'vast', 'windswept', 'hostile',
            'untouched', 'scorched', 'thirsty', 'dismal', 'sun-baked', 'unexplored', 'formidable', 'vacant',
            'inaccessible', 'harsh', 'uncomprimising']
        self.desert_noun = ['country', 'wilderness', 'flatland', 'sand dune', 'wasteland', 'badland', 'desert']
        spring = ['grassy', 'dewy', 'green', 'breezy', 'blooming', 'lush', 'welcome', 'natural', 'wonderful', 'charming',
                    'verdant', 'abundant', 'succulent', 'delectable', 'opulent', 'luscious', 'fresh', 'teeming', 'ripe',
                    'prolific', 'fresh', 'florishing']
        self.spring_noun = ['knoll', 'meadow', 'pasture', 'prairie', 'field', 'garden', 'plain']
        snowy = ['freezing', 'arctic', 'chilly', 'snowy', 'cold', 'snow-covered', 'formidable', 'powdery', 'endless', 'lonesome',
                'white', 'glacial', 'inaccessible', 'sparkingly', 'icy', 'vast', 'fresh', 'dazzling', 'crystalline', 'great', 'bitter',
                'unknown', 'pristine', 'quiescent', 'majestic', 'immense', 'half-melted', 'unrivaled', 'trechorous']
        self.snowy_noun = ['tundra', 'wonderland', 'glacier', 'pole']
        self.grave_yard = ['spooky', 'haunting', 'chilling', 'grim', 'gloomy', 'grotesque', 'gothic', 'silent', 'quiet',
                    'disused', 'unkempt', 'strange', 'scary', 'ancient', 'lonesome', 'ramsackle', 'old', 'abyssal',
                    'shabby', 'half-forgotten', 'eerie', 'wretched', 'obscure', 'dingy', 'bleak', 'deserted', 'vacant', 'torrid']
        self.grave_yard_noun = ['cemetery', 'gravesite', 'graveyard', 'resting place', 'city of the dead', 'eternal home']
        self.name = ['Magical', 'Mystical', 'Mysterious', 'Curious', 'Hidden', 'Impenetrable', 'Enchanted', 'Fascinating',
                'Unusual', 'Enchanted', 'Mighty', 'Supreme', 'Wicked', 'Spellbound', 'Spooky', 'Forbidden', 'Welcoming',
                'Enticing', 'Delightful', 'Magnetic', 'Chilling', 'Creepy', 'Eerie', "Looter's", 'Treasure', "Miguel's",
                "Dylan's", "Maggie's", "Hunter's", 'Secret', 'Verboten']
        self.phrases = ['Do you see any treasure chests?', 'Should you move on?', 'Where to next?', 'What would you like to do?',
                    'How much loot have you found?', 'Continue on to find the treasure room!', 'Onward!']

    def gen_name_description(self, rooms):
        descriptions = []
        names = []
        for room in rooms:
            if room == 1:
                room_description = f"You are now in an {', '.join(random.sample(desert, 2))} {random.sample(desert_noun, 1)[0]}. {random.sample(phrases, 1)[0]}"
                room_name = f'{random.sample(name, 1)[0]} Desert'
            elif room == 2:
                room_description = f"You are now in an {', '.join(random.sample(spring, 2))} {random.sample(spring_noun, 1)[0]}. {random.sample(phrases, 1)[0]}"
                room_name = f'{random.sample(name, 1)[0]} Field'
            elif room == 3:
                room_description = f"You are now in an {', '.join(random.sample(snowy, 2))} {random.sample(snowy_noun, 1)[0]}. {random.sample(phrases, 1)[0]}"
                room_name = f'{random.sample(name, 1)[0]} Winter Wonderland'
            else:
                room_description = f"You are now in an {', '.join(random.sample(grave_yard, 2))} {random.sample(grave_yard_noun, 1)[0]}. {random.sample(phrases, 1)[0]}"
                room_name = f"{random.sample(name, 1)[0]} Graveyard"
            descriptions.append(room_description)
            names.append(room_name)
        print(descriptions)
        print(names)