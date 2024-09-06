from abc import ABC, abstractmethod
from typing import List, Dict
import os

# Absolute path of the current file
current_dir = os.path.dirname(os.path.abspath(__file__))

# Search for the 'App' directory in the path and slice the path up to that directory
split_path = current_dir.split(os.sep)
app_index = split_path.index("App")
base_path = os.sep.join(split_path[:app_index + 1])

# Create the ABS_PATH with a placeholder for future formatting
ABS_PATH = os.path.join(base_path, "{}")

class MappingStrategy(ABC):
    """
    Abstract base class for creating mappings from a data set.
    """
    
    def __init__(self, input_csv: str) -> None:
        """
        Initialize the AbstractMapping with an empty data set and an input CSV file path.

        Args:
            input_csv (str): The path to the input CSV file.
        
        Returns:
            None
        """
        self.input_csv: str = input_csv

    @abstractmethod
    def make_mapping(self, row : str) -> List[Dict]:
        """
        Abstract method to create a mapping from the data set.

        This method should be implemented by the subclass. It is the method that will be
        called to create the mapping of some object to be submitted to Salesforce.

        Args:
            None

        Returns:
            List[Dict]: A list of dictionaries representing the mapping for some object.
        """
        pass