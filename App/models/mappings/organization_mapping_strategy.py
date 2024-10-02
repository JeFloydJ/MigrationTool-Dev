import csv
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from models.mappings.mapping_strategy import MappingStrategy
from models.strategies.salesforce_strategy import SalesforceStrategy
from typing import List, Dict

class OrganizationMappingStrategy(MappingStrategy):
    """
    A class used to represent an organization mapping strategy.
    """
    
    def __init__(self, input_csv: str) -> None:
        """
        Initialize the mapping strategy with the input CSV file.

        Args:
            account_list (List[Dict]): data of the reports to be processed.
            salesforce_strategy (SalesforceStrategy): instance of SalesforceStrategy for get organization id.

        Returns:
            None
        """
        super().__init__(input_csv)
        self.account_list: List[Dict] = []
        self.salesforce_strategy = SalesforceStrategy()  

    def make_mapping(self) -> List[Dict]:
        """
        Processes the input CSV file and creates a mapping of organization data.
        
        This method reads the CSV file, processes each row according to the report name,
        and generates a list of dictionaries representing the organization mappings.
        
        Returns:
            List[Dict]: A list of dictionaries representing the organization mappings.
        """ 
        try: 
            with open(self.input_csv, 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f, delimiter=';')
                organization_id = self.salesforce_strategy.get_organization_id()
                for row in reader:
                    account_info = {
                        'RecordTypeId': organization_id,
                        'Auctifera__Implementation_External_ID__c': row['Lookup ID'],
                        'Name': row["Name"],
                        'Website': row['Web address'],
                    }
                    if row['Email Addresses\\Email address'] != '':
                        account_info['Auctifera__Email__c'] = row['Email Addresses\\Email address']

                    self.account_list.append(account_info)
        
        except Exception:
            with open(self.input_csv, 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f, delimiter=',')
                organization_id = self.salesforce_strategy.get_organization_id()
                for row in reader:
                    account_info = {
                        'RecordTypeId': organization_id,
                        'Auctifera__Implementation_External_ID__c': row['Lookup ID'],
                        'Name': row["Name"],
                        'Website': row['Web address'],
                    }
                    if row['Email Addresses\\Email address'] != '':
                        account_info['Auctifera__Email__c'] = row['Email Addresses\\Email address']

                    self.account_list.append(account_info)           
                   
        return self.account_list
