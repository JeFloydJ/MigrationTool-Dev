import csv
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from models.mappings.mapping_strategy import MappingStrategy
from typing import List, Dict

class EmailStrategy(MappingStrategy):
    """
    A class used to represent an emails of contacts mapping strategy.
    """
    
    def __init__(self, input_csv: str) -> None:
        """
        Initialize the mapping strategy with the input CSV file.

        Args:
            input_csv (str): Path to the input CSV file.

        Returns:
            None
        """
        super().__init__(input_csv)
        self.object_emails_address_list: List[Dict] = []

    def make_mapping(self) -> List[Dict]:
        """
        Processes the input CSV file and creates a mapping of emails of contacts data.
        
        This method reads the CSV file, processes each row according to the report name,
        and generates a list of dictionaries representing the emails of contacts mappings.
        
        Returns:
            List[Dict]: A list of dictionaries representing the emails of contacts mappings.
        """ 
        try:
            with open(self.input_csv, 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f, delimiter=';')
                for counter, row in enumerate(reader, start=1):
                    lookup_id = row['Lookup ID']
                    contacts_emails_info = {
                    'vnfp__Type__c' : 'Email',
                    'vnfp__value__c' : row['Email Addresses\\Email address'],
                    'vnfp__Contact__r': {'Auctifera__Implementation_External_ID__c': lookup_id},
                    'vnfp__Implementation_External_ID__c' : str(str(counter)+ '-' + 'contacts-email' + '-' + row['QUERYRECID'])
                    }
                    self.object_emails_address_list.append(contacts_emails_info)

        except Exception:
            with open(self.input_csv, 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f, delimiter=',')
                for counter, row in enumerate(reader, start=1):
                    lookup_id = row['Lookup ID']
                    contacts_emails_info = {
                    'vnfp__Type__c' : 'Email',
                    'vnfp__value__c' : row['Email Addresses\\Email address'],
                    'vnfp__Contact__r': {'Auctifera__Implementation_External_ID__c': lookup_id},
                    'vnfp__Implementation_External_ID__c' : str(str(counter)+ '-' + 'contacts-email' + '-' + row['QUERYRECID'])
                    }
                    self.object_emails_address_list.append(contacts_emails_info)
        
        return self.object_emails_address_list
        
class EmailUpdateStrategy(MappingStrategy):
    """
    A class used to represent an update of emails of contacts mapping strategy.
    """
    
    def __init__(self, input_csv: str) -> None:
        """
        Initialize the mapping strategy with the input CSV file.

        Args:
            input_csv (str): Path to the input CSV file.
        
        Returns:
            None
        """
        super().__init__(input_csv)
        self.object_emails_update_address_list: List[Dict] = []

    def make_mapping(self) -> List[Dict]:
        """
        Processes the input CSV file and creates a mapping of updated email of contact data.
        
        This method reads the CSV file, processes each row according to the report name,
        and generates a list of dictionaries representing the update of emails of contacts mappings.
        
        Returns:
            List[Dict]: A list of dictionaries representing the update of emails of contacts mappings.
        """ 
        try:
            with open(self.input_csv, 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f, delimiter=';')
                for counter, row in enumerate(reader, start=1):
                    valid = bool(row['Email Addresses\\Primary email address'])
                    new_info = {
                        'Auctifera__Implementation_External_ID__c': row['Lookup ID'], 
                        'Email' : row['Email Addresses\\Email address']
                    }
                    if valid:
                        self.object_emails_update_address_list.append(new_info)      

        except Exception:
            with open(self.input_csv, 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f, delimiter=',')
                for counter, row in enumerate(reader, start=1):
                    valid = bool(row['Email Addresses\\Primary email address'])
                    new_info = {
                        'Auctifera__Implementation_External_ID__c': row['Lookup ID'], 
                        'Email' : row['Email Addresses\\Email address']
                    }
                    if valid:
                        self.object_emails_update_address_list.append(new_info)      

        return self.object_emails_update_address_list