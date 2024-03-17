def simulate_single_turn(grid, f_new_pair_group, f_check_stability):
    for layer_index in range(grid.layer_size):
        for x in range(grid.layer_size):
            for y in range(grid.layer_size):
                pair = grid.layers[layer_index][x][y]
                if pair is not None:
                    pair_group = f_new_pair_group(pair, x, y, grid)
                    update_magnitude(pair_group)
                    flip = update_stability(pair_group, f_check_stability)
                    flip_pair(flip, pair_group, grid)


def update_magnitude(pair_group):
        pair_group.current.magnitude += 0.1

def update_stability(pair_group, f_check_stablity):
    stability = 0
    pressure = 0
    if pair_group.current.stability == 1:
        stability += pair_group.current.magnitude
    else:
        pressure += pair_group.current.magnitude
    for direction in ["north", "south", "east", "west"]:
        neighbor = pair_group.get_neighbor(direction)
        if neighbor is None:
            pressure += 0.9
        elif f_check_stablity(neighbor.topType, pair_group.current.topType) == 1:
            stability += neighbor.magnitude
        else:
            pressure += neighbor.magnitude
    if pair_group.up is not None:
        if f_check_stablity(pair_group.up.bottomType, pair_group.current.topType) == 1:
            stability += pair_group.up.magnitude
        else:
            pressure += pair_group.up.magnitude
    if pair_group.down is not None:
        if f_check_stablity(pair_group.down.topType, pair_group.current.bottomType) == 1:
            stability += pair_group.down.magnitude
        else:
            pressure += pair_group.down.magnitude
    
    pair_group.current.pressure = pressure

    return stability < pressure

def flip_pair(flip, pair_group, grid):
    if flip:
        if pair_group.current.stability == 1:
            if pair_group.current.magnitude > pair_group.current.max_magnitude:
                if pair_group.current.layer + 1 < grid.layer_size and pair_group.up is None:
                    pair_group.up = pair_group.current.copy()
                    pair_group.up.layer = pair_group.current.layer + 1
                    pair_group.up.topType = pair_group.current.bottomType
                    pair_group.up.bottomType = pair_group.current.topType
                    grid.layers[pair_group.up.layer][pair_group.up.x][pair_group.up.y] = pair_group.up
                pair_group.up.magnitude = pair_group.current.magnitude / 2
                pair_group.current.magnitude = pair_group.current.magnitude / 2
        else:
            directions = ["up", "down", "north", "south", "east", "west"]
            neighbors = sum(1 for direction in directions if pair_group.get_neighbor(direction) is not None)
            for direction in directions:
                neighbor = pair_group.get_neighbor(direction)
                if neighbor is not None:
                    neighbor.magnitude += 0.1 / neighbors
            temp = pair_group.current.topType
            pair_group.current.topType = pair_group.current.bottomType
            pair_group.current.bottomType = temp
            pair_group.current.magnitude -= 1
            if pair_group.current.magnitude < 1 and pair_group.current.layer == 0:
                pair_group.current.magnitude = 1
            if pair_group.current.magnitude < 0:
                grid.layers[pair_group.current.layer][pair_group.current.x][pair_group.current.y] = None
    else:
        if pair_group.current.stability == 1:
            pair_group.current.magnitude += 0.1
        else:
            directions = ["up", "down", "north", "south", "east", "west"]
            neighbors = sum(1 for direction in directions if pair_group.get_neighbor(direction) is not None)
            for direction in directions:
                neighbor = pair_group.get_neighbor(direction)
                if neighbor is not None:
                    neighbor.magnitude += 0.1 / neighbors