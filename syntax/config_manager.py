import abc
import os

class Layer(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def load(self):
        pass

    @property
    @abc.abstractmethod
    def all(self):
        pass


class YamlLayer:
    def __init__(self, fname):
        self.fname = fname
        self.data = None

    def load(self):
        with open(self.fname, "r") as g:
            self.data = yaml.load(f)

    @property
    def all(self):
        return list(self.data.keys())

    def __getattr__(self, v):
        return self.data[v]


class SaneDefaults(Layer):
    def __init__(self):
        self.data = {
            "cache_path": os.path.join(os.path.expanduser("~"), ".syntax", "cache"),
            "project_path": os.path.realpath(".")
        }

    def load(self):
        return

    @property
    def all(self):
        return list(self.data.keys())
        
    def __getattr__(self, v):
        return self.data[v]


class ConfigManager:

    _default = None

    def __init__(self, *layers):
        self.config = {}
        self.layers = layers
        for layer in layers:
            self.add_layer(layer)

    def add_layer(self, layer):
        self.layers.append(layer)
        layer.load()
        for key in layer.all:
            self.config[key] = self.layer[key]

    def __getattr__(self, v):
        return self.config[v]

    @classmethod
    def get_manager(cls):
        if cls._default is None:
            cls._default = ConfigManager(SaneDefaults())
        return cls._default
