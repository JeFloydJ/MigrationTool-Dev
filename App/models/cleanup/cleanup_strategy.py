from abc import ABC, abstractmethod
import csv
from enum import Enum
import logging
import os
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
    force=True
)
logger = logging.getLogger(__name__)


class CleanupStrategy(ABC):
    """
    Abstract base class for cleanup strategies.
    """
    def __init__(self, input_csv: str, output_csv: str) -> None:
        """
        Initialize the CleanupStrategy with input and output CSV file paths.

        Args:
            input_csv (str): The path to the input CSV file.
            output_csv (str): The path to the output CSV file.
        
        Returns:
            None
        """
        self.input_csv = input_csv
        self.output_csv = output_csv
    
    @abstractmethod
    def cleanup(self) -> None:
        """
        Abstract method to perform the cleanup operation. Must be implemented by subclasses.

        Args:
            None

        Returns:
            None
        """
        pass
