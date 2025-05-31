"""input

"""
from utils_standard import contexts_to_standard
from context.context import Context
from inputoutput import InputOutput

class Input(InputOutput):
    """database class

    >>> i = Input()
    >>> i[10] = Context(value=1.0, cohorts=[1,2,3])
    >>> i[10].value
    1.0
    >>> i[20] # None will be returned
    >>> i.reset()
    """
    def __init__(self):
        self.dictionary = {}

if __name__ == "__main__":
    import doctest
    doctest.testmod()


