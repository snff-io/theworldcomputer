import random

class Grid():
    # Constants
    layer_size = 379
    max_magnitude = 50
    layers = []

    def __init__(self, layer_size):
        self.layer_size = layer_size
        

    def initialize_grid(self, factory_method, populated_layer_count):
        self.layers = []
        for layer_index in range(self.layer_size):
            if len(self.layers) >= self.layer_size:
                break
            if len(self.layers) <= populated_layer_count - 1:
                layer = []
                for x in range(self.layer_size):
                    col = []
                    layer.append(col)
                    for y in range(self.layer_size):
                        col.append(factory_method(x, y, len(self.layers)))
                self.layers.append(layer)
            else:
                empty_layer = [[None] * self.layer_size for _ in range(self.layer_size)]
                self.layers.append(empty_layer)
    
__all__ = { Grid }