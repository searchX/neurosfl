# Improt ABC and create basic backend interface
from abc import ABC, abstractmethod

from neurosfl.frontend.structs import StartNode

class Backend(ABC):
    """Base class for backend
    """
    @abstractmethod
    def parse(self, node: StartNode, symbols: dict = {}):
        """Parse node into backend query

        :param node: Node to parse
        :param symbols: Dictionary of symbols to use for parsing
        :type node: :class:`StartNode`
        :type symbols: dict
        :return: output final code
        :rtype: Any
        """
        pass