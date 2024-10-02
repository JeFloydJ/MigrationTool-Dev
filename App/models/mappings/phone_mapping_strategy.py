import csv
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from models.mappings.mapping_strategy import MappingStrategy
from typing import List, Dict

class PhoneStrategy(MappingStrategy):
    """
    A class used to represent an phones of organizations mapping strategy.
    """
    
    def __init__(self, input_csv: str) -> None:
        """
        Initialize the mapping strategy with the input CSV file.

        Args:
            organizations_phones_list (List[Dict]): data of the reports to be processed.
        Returns:
            None
        """
        super().__init__(input_csv)
        self.object_phones_list: List[Dict] = []

    def make_mapping(self) -> List[Dict]:
        """
        Processes the input CSV file and creates a mapping of phones of organizations data.
        
        This method reads the CSV file, processes each row according to the report name,
        and generates a list of dictionaries representing the phones of organizations mappings.
        
        Returns:
            List[Dict]: A list of dictionaries representing the phones of organizations mappings.
        """ 
        try:
            with open(self.input_csv, 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f, delimiter=';')
                counter = 0
                for counter, row in enumerate(reader, start=1):
                    lookup_id = row['Lookup ID']
                    organizations_phones_info = {
                        'vnfp__Type__c' : 'Phone',
                        'vnfp__value__c' : row['Phones\\Number'],
                        'vnfp__Account__r': {'Auctifera__Implementation_External_ID__c': lookup_id},
                        'vnfp__Implementation_External_ID__c' : str(str(counter)+ '-' + 'phone' + '-' + row['QUERYRECID']) 
                    }
                    self.object_phones_list.append(organizations_phones_info)
 
        except Exception:
            with open(self.input_csv, 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f, delimiter=',')
                counter = 0
                for counter, row in enumerate(reader, start=1):
                    lookup_id = row['Lookup ID']
                    organizations_phones_info = {
                        'vnfp__Type__c' : 'Phone',
                        'vnfp__value__c' : row['Phones\\Number'],
                        'vnfp__Account__r': {'Auctifera__Implementation_External_ID__c': lookup_id},
                        'vnfp__Implementation_External_ID__c' : str(str(counter)+ '-' + 'phone' + '-' + row['QUERYRECID']) 
                    }
                    self.object_phones_list.append(organizations_phones_info)

        return self.object_phones_list

class PhoneUpdateStrategy(MappingStrategy):
    """
    A class used to represent an update of phones of organizations mapping strategy.
    """
    
    def __init__(self, input_csv: str) -> None:
        """
        Initialize the mapping strategy with the input CSV file.

        Args:
            organizations_phones_list (List[Dict]): data of the reports to be processed.
        Returns:
            None
        """
        super().__init__(input_csv)
        self.object_phones_update_list: List[Dict] = []

    def make_mapping(self) -> List[Dict]:
        """
        Processes the input CSV file and creates a mapping of phones of organizations data.
        
        This method reads the CSV file, processes each row according to the report name,
        and generates a list of dictionaries representing the  update phones of organizations mappings.
        
        Returns:
            List[Dict]: A list of dictionaries representing the update phones of organizations mappings.
        """ 
        try:
            with open(self.input_csv, 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f, delimiter=';')
                for counter, row in enumerate(reader, start=1):
                    valid = bool(row['Phones\\Primary phone number'])
                    organizations_update_phones_info = {
                        'Auctifera__Implementation_External_ID__c': row['Lookup ID'], 
                        'Phone' : row['Phones\\Number']
                    }
                    if valid:
                        self.object_phones_update_list.append(organizations_update_phones_info)

        except Exception:
            with open(self.input_csv, 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f, delimiter=',')
                for counter, row in enumerate(reader, start=1):
                    valid = bool(row['Phones\\Primary phone number'])
                    organizations_update_phones_info = {
                        'Auctifera__Implementation_External_ID__c': row['Lookup ID'], 
                        'Phone' : row['Phones\\Number']
                    }
                    if valid:
                        self.object_phones_update_list.append(organizations_update_phones_info)

        return self.object_phones_update_list

