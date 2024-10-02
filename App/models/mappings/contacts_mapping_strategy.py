import csv
import os
import re
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from models.mappings.mapping_strategy import MappingStrategy
from models.strategies.salesforce_strategy import SalesforceStrategy
from typing import List, Dict

class ContactsMappingStrategy(MappingStrategy):
    """
    A class used to represent an Contacts mapping strategy.
    """
    
    def __init__(self, input_csv: str) -> None:
        """
        Initialize the mapping strategy with the input CSV file.

        Args:
            contact_list (List[Dict]): data of the reports to be processed.

        Returns:
            None
        """
        super().__init__(input_csv)
        self.contacts_list: List[Dict] = []
        self.contacts_id_list : List[str] = []
        self.contacts_accounts_id : Dict[str, str] = {}
        self.salesforce_strategy = SalesforceStrategy()
    
    def find_households_id(self, HouseHoldslist):
        """
        Method to create extract the id of the households from the list of reports
        ex:
        #-households-code
        extract the code

        Args:
            houseHoldslist (List): list of households codes
        returns:
            dic: dictionary with the id of the households
        """
        dic = {}
        for element in HouseHoldslist:
            match = re.search(r'(\d+)-households-(.*)', element)
            if match:
                id = match.group(2)
                dic[id] = element
        return dic
    
    def make_mapping(self, HouseHoldslist: List[str]) -> List[Dict]:
        """
        Processes the input CSV file and creates a mapping of contact data.
        
        This method reads the CSV file, processes each row according to the report name,
        and generates a list of dictionaries representing the contact mappings.
        
        Returns:
            List[Dict]: A list of dictionaries representing the contact mappings.
        """
        dic = self.find_households_id(HouseHoldslist) 
        try:
            with open(self.input_csv, 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f, delimiter=';')
                for row in reader:
                    account = row.get('Households Belonging To\\Household Record ID', '')
                    contacts_info = {
                        'Salutation' : row['Title'],
                        'FirstName' : row['First name'],
                        'LastName' : row['Last/Organization/Group/Household name'],
                        'Auctifera__Implementation_External_ID__c' : row['Lookup ID'],
                    }
                    if account and account in dic:
                        contacts_info['Account'] = {'Auctifera__Implementation_External_ID__c': dic[account]}

                    self.contacts_list.append(contacts_info)
 
        except Exception:
            with open(self.input_csv, 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f, delimiter=',')
                for row in reader:
                    account = row.get('Households Belonging To\\Household Record ID', '')
                    contacts_info = {
                        'Salutation' : row['Title'],
                        'FirstName' : row['First name'],
                        'LastName' : row['Last/Organization/Group/Household name'],
                        'Auctifera__Implementation_External_ID__c' : row['Lookup ID'],
                    }
                    if account and account in dic:
                        contacts_info['Account'] = {'Auctifera__Implementation_External_ID__c': dic[account]}

                    self.contacts_list.append(contacts_info)
 
        return self.contacts_list
    
    def process_contacts_ids(self, results) -> Dict[str, str]:
        """
        Processes the results of the contacts uploded and get id of accounts associates with contact            
            Returns:
                List[Dict]: A list of dictionaries representing the contact mappings.
        """
        for result in results:
            if result['success']:
                self.contacts_id_list.append(result['id'])

        self.contacts_accounts_id = self.salesforce_strategy.get_account_id()
        
        return self.contacts_accounts_id
        
