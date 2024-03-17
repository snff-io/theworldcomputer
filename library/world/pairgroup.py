class PairGroup:
    def __init__(self, pair, x, y, grid):
        self.current = pair
        self.north = grid.layers[pair.layer][x][y + 1] if y + 1 < grid.layer_size else None
        self.south = grid.layers[pair.layer][x][y - 1] if y - 1 >= 0 else None
        self.east = grid.layers[pair.layer][x + 1][y] if x + 1 < grid.layer_size else None
        self.west = grid.layers[pair.layer][x - 1][y] if x - 1 >= 0 else None
        self.up = grid.layers[pair.layer + 1][x][y] if pair.layer + 1 < grid.layer_size else None
        self.down = grid.layers[pair.layer - 1][x][y] if pair.layer > 0 else None

    def get_neighbor(self, direction):
        return getattr(self, direction, None)
