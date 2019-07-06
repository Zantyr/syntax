import abc
import tempfile

class Serializable(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def serialize(self, root_folder):
        pass
        
    @abc.abstractstaticmethod
    def deserialize(filename):
        """
        Loads the item completely from the filename, creates a new instance
        May reference other Serializables in recursive fashion
        All data required to find necessary files is in filename
        All files required will be archived nevertheless
        """


def _serialize(thing, where=None):
    """
    Returns filename of the serialized file
    """
    if where is None:
        where = tempfile.mkdtemp()
    if isinstance(thing, Serializable):
        filename = thing.serialize(where)
        return filename
    try:
        with open():
            pass
    except TypeError:
        pass
