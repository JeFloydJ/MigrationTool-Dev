import csv
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from models.mappings.mapping_strategy import MappingStrategy
from typing import List, Dict

class OrganizationAffilationStrategy(MappingStrategy):
    """
    A class used to represent an Relationship of organizations mapping strategy.
    """
    
    def __init__(self, input_csv: str) -> None:
        """
        Initialize the mapping strategy with the input CSV file.

        Args:
            organizations_relationship_list (List[Dict]): data of the reports to be processed.
        Returns:
            None
        """
        super().__init__(input_csv)
        self.organizations_relationship_list: List[Dict] = []

    def make_mapping(self) -> List[Dict]:
        """
        Processes the input CSV file and creates a mapping of Relationship of organizations data.
        
        This method reads the CSV file, processes each row according to the report name,
        and generates a list of dictionaries representing the Relationship of organizations mappings.
        
        Returns:
            List[Dict]: A list of dictionaries representing the Relationship of organizations mappings.
        """ 
        try:
            with open(self.input_csv, 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f, delimiter=';')
                for counter, row in enumerate(reader, start=1):
                    contact_lookup_id = row['Lookup ID']
                    organization_lookup_id = row['Relationships\\Related Constituent\\Lookup ID']
                    organizations_relationship_info = {
                        'npe5__Contact__r' : {'Auctifera__Implementation_External_ID__c': contact_lookup_id},
                        'npe5__Organization__r' : {'Auctifera__Implementation_External_ID__c': organization_lookup_id},
                        'npe5__Primary__c' : False if row['Relationships\\Is primary contact'] != 'Yes' else True,
                        'npe5__Role__c' : row['Relationships\\Reciprocal relationship type'],
                        'vnfp__Implementation_External_ID__c' : row['QUERYRECID']
                    }
                    self.organizations_relationship_list.append(organizations_relationship_info)

        except Exception:
            with open(self.input_csv, 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f, delimiter=',')
                for counter, row in enumerate(reader, start=1):
                    contact_lookup_id = row['Lookup ID']
                    organization_lookup_id = row['Relationships\\Related Constituent\\Lookup ID']
                    organizations_relationship_info = {
                        'npe5__Contact__r' : {'Auctifera__Implementation_External_ID__c': contact_lookup_id},
                        'npe5__Organization__r' : {'Auctifera__Implementation_External_ID__c': organization_lookup_id},
                        'npe5__Primary__c' : False if row['Relationships\\Is primary contact'] != 'Yes' else True,
                        'npe5__Role__c' : row['Relationships\\Reciprocal relationship type'],
                        'vnfp__Implementation_External_ID__c' : row['QUERYRECID']
                    }
                    self.organizations_relationship_list.append(organizations_relationship_info)

        return self.organizations_relationship_list
        

class ContactsRelationshipStrategy(MappingStrategy):
    """
    A class used to represent an Relationship of contacts mapping strategy.
    """
    
    def __init__(self, input_csv: str) -> None:
        """
        Initialize the mapping strategy with the input CSV file.

        Args:
            organizations_relationship_list (List[Dict]): data of the reports to be processed.
        Returns:
            None
        """
        super().__init__(input_csv)
        self.contacts_relationship_list: List[Dict] = []

    def make_mapping(self) -> List[Dict]:
        """
        Processes the input CSV file and creates a mapping of Relationship of contacts data.
        
        This method reads the CSV file, processes each row according to the report name,
        and generates a list of dictionaries representing the Relationship of contacts mappings.
        
        Returns:
            List[Dict]: A list of dictionaries representing the Relationship of contacts mappings.
        """ 
        try: 
            with open(self.input_csv, 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f, delimiter=';')
                for counter, row in enumerate(reader, start=1):
                    lookup_id = row['Lookup ID']
                    contacts_relationship_info = {
                        'npe4__Contact__r': {'Auctifera__Implementation_External_ID__c': lookup_id},
                        'npe4__RelatedContact__r': {'Auctifera__Implementation_External_ID__c': lookup_id},
                        'npe4__Type__c' : row['Relationships\\Reciprocal relationship type'],
                        'vnfp__Implementation_External_ID__c' : row['QUERYRECID']
                    }
                    self.contacts_relationship_list.append(contacts_relationship_info)

        except Exception:
            with open(self.input_csv, 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f, delimiter=',')
                for counter, row in enumerate(reader, start=1):
                    lookup_id = row['Lookup ID']
                    contacts_relationship_info = {
                        'npe4__Contact__r': {'Auctifera__Implementation_External_ID__c': lookup_id},
                        'npe4__RelatedContact__r': {'Auctifera__Implementation_External_ID__c': lookup_id},
                        'npe4__Type__c' : row['Relationships\\Reciprocal relationship type'],
                        'vnfp__Implementation_External_ID__c' : row['QUERYRECID']
                    }
                    self.contacts_relationship_list.append(contacts_relationship_info)
            
        return self.contacts_relationship_list
        
