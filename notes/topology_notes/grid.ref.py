import random

# Constants
gridSize = 18  # Size of each layer in the grid
numLayers = 18  # Total number of layers
maxMagnitude = 50
WEB_GL = True
vp = 1024

stability_table = [
    [-1, 1, 2, 3, 4, 5, 6, 7, 8],
    [1, 1, 0, 0, 0, 0, 0, 0, 0],
    [2, 1, 1, 1, 0, 1, 1, 1, 1],
    [3, 1, 0, 1, 1, 1, 1, 0, 0],
    [4, 1, 0, 0, 1, 1, 1, 0, 0],
    [5, 1, 0, 0, 0, 1, 0, 0, 0],
    [6, 1, 0, 0, 0, 1, 1, 0, 0],
    [7, 1, 0, 0, 0, 1, 1, 1, 1],
    [8, 1, 0, 0, 1, 1, 1, 0, 1]
]

# Functions
def check_stability(top_type, bottom_type):
    return stability_table[bottom_type][top_type]

def random_individual(x, y, layer=0):
    top_type = random.randint(1, 8)
    bottom_type = random.randint(1, 8)
    magnitude = 1
    pressure = 0
    return Pair(x, y, top_type, bottom_type, magnitude, pressure, layer)

def initialize_grid(size, layer_size, pop_layers=0):
    grid = []
    for layer_index in range(layer_size):
        if len(grid) >= size:
            break
        if len(grid) <= pop_layers:
            layer = []
            for x in range(size):
                col = []
                layer.append(col)
                for y in range(size):
                    col.append(random_individual(x, y, len(grid)))
            grid.append(layer)
        else:
            empty_layer = [[None] * size for _ in range(size)]
            grid.append(empty_layer)
    return grid

def simulate_single_turn(grid):
    for layer_index in range(numLayers):
        for x in range(gridSize):
            for y in range(gridSize):
                pair = grid[layer_index][x][y]
                if pair is not None:
                    pair_group = get_pair_group(pair, x, y, grid)
                    update_magnitude(pair_group)
                    flip = update_stability(pair_group)
                    flip_pair(flip, pair_group, grid)

def get_pair_group(pair, x, y, grid):
    pair_group = {}
    pair_group["current"] = pair
    pair_group["north"] = grid[pair.layer][x][y + 1] if y + 1 < gridSize else None
    pair_group["south"] = grid[pair.layer][x][y - 1] if y - 1 >= 0 else None
    pair_group["east"] = grid[pair.layer][x + 1][y] if x + 1 < gridSize else None
    pair_group["west"] = grid[pair.layer][x - 1][y] if x - 1 >= 0 else None
    pair_group["up"] = grid[pair.layer + 1][x][y] if pair.layer + 1 < numLayers else None
    pair_group["down"] = grid[pair.layer - 1][x][y] if pair.layer > 0 else None
    return pair_group

def update_magnitude(pair_group):
    pair_group["current"].magnitude += 0.1

def update_stability(pair_group):
    stability = 0
    pressure = 0
    if pair_group["current"].stability == 1:
        stability += pair_group["current"].magnitude
    else:
        pressure += pair_group["current"].magnitude
    for direction in ["north", "south", "east", "west"]:
        neighbor = pair_group.get_neighbor(direction)
        if neighbor is None:
            pressure += 0.9
        elif check_stability(neighbor.topType, pair_group["current"].topType) == 1:
            stability += neighbor.magnitude
        else:
            pressure += neighbor.magnitude
    if pair_group["up"] is not None:
        if check_stability(pair_group["up"].bottomType, pair_group["current"].topType) == 1:
            stability += pair_group["up"].magnitude
        else:
            pressure += pair_group["up"].magnitude
    if pair_group["down"] is not None:
        if check_stability(pair_group["down"].topType, pair_group["current"].bottomType) == 1:
            stability += pair_group["down"].magnitude
        else:
            pressure += pair_group["down"].magnitude
    return stability < pressure

def flip_pair(flip, pair_group, grid):
    if flip:
        if pair_group["current"].stability == 1:
            if pair_group["current"].magnitude > maxMagnitude:
                if pair_group["current"].layer + 1 < numLayers and pair_group["up"] is None:
                    pair_group["up"] = pair_group["current"].copy()
                    pair_group["up"].layer = pair_group["current"].layer + 1
                    pair_group["up"].topType = pair_group["current"].bottomType
                    pair_group["up"].bottomType = pair_group["current"].topType
                    grid[pair_group["up"].layer][pair_group["up"].x][pair_group["up"].y] = pair_group["up"]
                pair_group["up"].magnitude = pair_group["current"].magnitude / 2
                pair_group["current"].magnitude = pair_group["current"].magnitude / 2
        else:
            directions = ["up", "down", "north", "south", "east", "west"]
            neighbors = sum(1 for direction in directions if pair_group.get_neighbor(direction) is not None)
            for direction in directions:
                neighbor = pair_group.get_neighbor(direction)
                if neighbor is not None:
                    neighbor.magnitude += 0.1 / neighbors
            temp = pair_group["current"].topType
            pair_group["current"].topType = pair_group["current"].bottomType
            pair_group["current"].bottomType = temp
            pair_group["current"].magnitude -= 1
            if pair_group["current"].magnitude < 1 and pair_group["current"].layer == 0:
                pair_group["current"].magnitude = 1
            if pair_group["current"].magnitude < 0:
                grid[pair_group["current"].layer][pair_group["current"].x][pair_group["current"].y] = None
    else:
        if pair_group["current"].stability == 1:
            pair_group["current"].magnitude += 0.1
        else:
            directions = ["up", "down", "north", "south", "east", "west"]
            neighbors = sum(1 for direction in directions if pair_group.get_neighbor(direction) is not None)
            for direction in directions:
                neighbor = pair_group.get_neighbor(direction)
                if neighbor is not None:
                    neighbor.magnitude += 0.1 / neighbors

# Classes
class Pair:
    def __init__(self, x, y, top_type, bottom_type, magnitude=1, pressure=0, layer=0):
        self.x = x
        self.y = y
        self.topType = top_type
        self.bottomType = bottom_type
        self.magnitude = magnitude
        self.pressure = pressure
        self.layer = layer

    @property
    def stability(self):
        return stability_table[self.bottomType][self.topType]

    def copy(self):
        return Pair(self.x, self.y, self.topType, self.bottomType, self.magnitude, self.pressure, self.layer)

    def __str__(self):
        return f"{self.stability}{self.topType}{self.bottomType};{self.magnitude:.2f};{self.pressure:.2f};{self.layer}:{self.x}:{self.y}"

# Setup
def setup():
    global grid
    cam_step = 200
    if WEB_GL:
        createCanvas(vp, vp, WEBGL)
        frameRate(100)
    else:
        createCanvas(1024, 1024)
        frameRate(1000)
    grid = initialize_grid(gridSize, numLayers)
    textFont(font)

# Draw
def draw():
    global grid
    camera(cam["x"], cam["y"], cam["z"], cam["cx"], cam["cy"], cam["cz"])
    background(255)
    if WEB_GL:
        angleMode(DEGREES)
        rotateX(cam["xr"])
        rotateY(cam["yr"])
    display_grid()
    simulate_single_turn(grid)

# Display Grid
def display_grid():
    cell_size = width / gridSize
    spacing = 0.1 * cell_size
    shrunk_size = 0.8 * cell_size
    for layer_index in range(numLayers):
        for x in range(gridSize):
            for y in range(gridSize):
                pair = grid[layer_index][x][y]
                if pair is not None:
                    x_pos = x * (cell_size + spacing) + cell_size / 2
                    y_pos = y * (cell_size + spacing) + cell_size / 2
                    z_pos = layer_index * (cell_size + spacing) + cell_size / 2
                    s = not pair.stability
                    fill(s * 255, pair.bottomType * 10, pair.bottomType * 10, 80)
                    if WEB_GL:
                        push()
                        translate(x_pos, y_pos, z_pos * 1.3)
                        box(shrunk_size, shrunk_size, -shrunk_size)
                        pop()
                    else:
                        fill(pair.bottomType * 10, pair.bottomType * 10, pair.stability * 255, 100)
                        rect(x_pos, y_pos, cell_size, cell_size)
                    if pair.stability == 0:
                        fill(255, 0, 0)
                    else:
                        fill(0, 255, 0)
                    if WEB_GL:
                        textStyle(NORMAL)
                    else:
                        textAlign(TOP, CENTER)
                        text(f"{pair.topType}-{pair.bottomType}", x_pos + cell_size / 4, y_pos + cell_size / 4)
                        textAlign(BOTTOM, CENTER)
                        text(f"{pair.magnitude:.2f}", x_pos + cell_size / 4, y_pos + cell_size / 2)

# Camera
cam = {
    "x": vp / 2,
    "y": -vp / 2,
    "z": -vp / 4,
    "cx": vp / 2,
    "cy": vp / 2,
    "cz": vp,
    "xr": 180,
    "yr": 0,
}

# Utility function
def sign(x):
    return 1 if x > 0 else -1 if x < 0 else 0

# Other
def preload():
    loadFont("CourierPrime-Regular.ttf")

# Key event handler (for WebGL)
def key_event_handler(event):
    global cam
    print('Key pressed:', event.key)
    cam_step = 200
    if event.key == "e":
        cam["z"] += cam_step
    elif event.key == "d":
        cam["z"] -= cam_step
    elif event.key == "f":
        cam["x"] += cam_step
    elif event.key == "s":
        cam["x"] -= cam_step
    elif event.key == "q":
        cam["y"] -= cam_step
    elif event.key == "a":
        cam["y"] += cam_step
    elif event.key == "w":
        cam["xr"] -= 1
    elif event.key == "r":
        cam["xr"] += 1
    elif event.key == "t":
        cam["yr"] -= 1
    elif event.key == "g":
        cam["yr"] += 1

# Event listener for key events
if WEB_GL:
    document.addEventListener('keydown', key_event_handler)
