import csv
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from models.mappings.mapping_strategy import MappingStrategy
from models.strategies.salesforce_strategy import SalesforceStrategy
from typing import List, Dict

class HouseholdsMappingStrategy(MappingStrategy):
    """
    A class used to represent an households mapping strategy.
    """
    
    def __init__(self, input_csv: str) -> None:
        """
        Initialize the mapping strategy with the input CSV file.

        Args:
            households_list (List[Dict]): data of the reports to be processed.
            households_external_ids_list (List[str]): list of external ids of the households.
            salesforce_strategy (SalesforceStrategy): instance of SalesforceStrategy for get organization id.

        Returns:
            None
        """
        super().__init__(input_csv)
        self.households_list: List[Dict] = []
        self.houseHolds_external_ids_list: List[str] = []
        self.salesforce_strategy = SalesforceStrategy()  

    def make_mapping(self) -> List[Dict]:
        """
        Processes the input CSV file and creates a mapping of households data.
        
        This method reads the CSV file, processes each row according to the report name,
        and generates a list of dictionaries representing the households mappings.
        
        Returns:
            List[Dict]: A list of dictionaries representing the households mappings.
        """
        try:
            with open(self.input_csv, 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f, delimiter=';')
                households_id = self.salesforce_strategy.get_households_id() 
                counter = 0
                for counter, row in enumerate(reader, start=1):
                    external_id = f"{counter}-households-{row['QUERYRECID']}"
                    self.houseHolds_external_ids_list.append(external_id)
                    households_info = {
                        'RecordTypeId': households_id,
                        'Auctifera__Implementation_External_ID__c': external_id,
                        'Name': row["Name"]
                    }
                    self.households_list.append(households_info)
        
        except Exception:
            with open(self.input_csv, 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f, delimiter=',')
                households_id = self.salesforce_strategy.get_households_id() 
                counter = 0
                for counter, row in enumerate(reader, start=1):
                    external_id = f"{counter}-households-{row['QUERYRECID']}"
                    self.houseHolds_external_ids_list.append(external_id)
                    households_info = {
                        'RecordTypeId': households_id,
                        'Auctifera__Implementation_External_ID__c': external_id,
                        'Name': row["Name"]
                    }
                    self.households_list.append(households_info)

        return self.households_list, self.houseHolds_external_ids_list