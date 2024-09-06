
import os 
import sys
from abc import ABC, abstractmethod
from typing import List
import logging
from models.strategies import salesforce_strategy

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
    force=True
)
logger = logging.getLogger(__name__)

# Set up directory paths
current_dir = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(current_dir)
ABS_PATH = os.path.join(BASE_DIR, "{}")

class migrationGroup(ABC):
    """
    Abstract base class for migration groups.
    """
    
    def __init__(self, report_names: List[str]) -> None:
        """
        Initialize the MigrationGroup with the given report names.

        Args:
            report_names (List[str]): The names of the reports to be processed.
        
        Returns:
            None
        """
        self.report_names = report_names
        self.strategy = salesforce_strategy.SalesforceStrategy()  # Initialize the strategy in the base class
    
    @abstractmethod
    def process_data(self) -> None:
        """
        Abstract method to process data. Must be implemented by subclasses.

        Args:
            None

        Returns:
            None
        """
        pass



