from abc import ABC, abstractmethod
import src.utils as utils

class Interface(ABC):
    """
    Interface abstract class
    Implements the option menu for each interface
    """
    
    # Abstract property: Options dictionary mapping option name to method
    @property
    @abstractmethod
    def options(self):
        pass

    def run(self):
        options_str = "Available options:\n"
        for i, option in enumerate(self.options):
            options_str += str(i+1) + ": " + option + "\n"

        while True:
            option = utils.get_num_choice(len(self.options), options_str, "Enter the option number: ", exit=True)
            if not option:
                return
            
            self.options[list(self.options.keys())[option-1]]()
