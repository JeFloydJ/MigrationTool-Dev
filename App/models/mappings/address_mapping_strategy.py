import csv
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from models.mappings.mapping_strategy import MappingStrategy
from typing import List, Dict

class OrganizationsAddressStrategy(MappingStrategy):
    """
    A class used to represent an address of organizations mapping strategy.
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
        self.organizations_address_list: List[Dict] = []

    def make_mapping(self) -> List[Dict]:
        """
        Processes the input CSV file and creates a mapping of address of organizations data.
        
        This method reads the CSV file, processes each row according to the report name,
        and generates a list of dictionaries representing the address of organizations mappings.
        
        Returns:
            List[Dict]: A list of dictionaries representing the address of organizations mappings.
        """ 
        try:
            with open(self.input_csv, 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f, delimiter=';')
                for counter, row in enumerate(reader, start=1):
                    lookup_id = row['Lookup ID']
                    organizations_address_info = {
                        'npsp__MailingStreet__c': row['Addresses\\Address'],
                        'npsp__MailingCity__c': row['Addresses\\City'],
                        'npsp__MailingState__c': row['Addresses\\State'],
                        'npsp__MailingPostalCode__c': row['Addresses\\ZIP'],
                        'npsp__MailingCountry__c': row['Addresses\\Country'],
                        'npsp__Default_Address__c': bool(row['Addresses\\Primary address']),
                        'vnfp__Implementation_External_ID__c': str(counter) + '-' + 'address' + '-' + 'organization' + '-' + row['QUERYRECID'],
                        'npsp__Household_Account__r': {'Auctifera__Implementation_External_ID__c': lookup_id}
                    }
                    self.organizations_address_list.append(organizations_address_info)

        except FileNotFoundError as e:
            print(f"Error: {e}")
        except KeyError as e:
            print(f"Missing key in CSV file: {e}")
        except IOError as e:
            print(f"Error reading or writing file: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

        return self.organizations_address_list
        
 
class ContactsAddressStrategy(MappingStrategy):
    """
    A class used to represent an address of contacts mapping strategy.
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
        self.contacts_address_list: List[Dict] = []

    def make_mapping(self, dic_accounts: Dict[str, str]) -> List[Dict]:
        """
        Processes the input CSV file and creates a mapping of address of contacts data.
        
        This method reads the CSV file, processes each row according to the report name,
        and generates a list of dictionaries representing the address of contacts mappings.
        
        Returns:
            List[Dict]: A list of dictionaries representing the address of contacts mappings.
        """ 
        try:
            with open(self.input_csv, 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f, delimiter=';')
                for counter, row in enumerate(reader, start=1):
                    lookup_id = row['Lookup ID']
                    contacts_addresses_info = {
                        'npsp__MailingStreet__c': row['Addresses\\Address'],
                        'npsp__MailingCity__c': row['Addresses\\City'],
                        'npsp__MailingState__c': row['Addresses\\State'],
                        'npsp__MailingPostalCode__c': row['Addresses\\ZIP'],
                        'npsp__MailingCountry__c': row['Addresses\\Country'],
                        'npsp__Household_Account__c': dic_accounts[lookup_id],
                        'npsp__Default_Address__c' : bool(row['Addresses\\Primary address']),
                        'vnfp__Implementation_External_ID__c' : str(str(counter)+ '-' + 'contacts-address' + '-' + 'contacts' +row['QUERYRECID'])
                    }
                    # if lookup_id in dic_accounts:
                    #     contacts_addresses_info['npsp__Household_Account__c'] = dic_accounts[lookup_id]
    
                    self.contacts_address_list.append(contacts_addresses_info)


        except FileNotFoundError as e:
            print(f"Error: {e}")
        except KeyError as e:
            print(f"Missing key in CSV file: {e}")
        except IOError as e:
            print(f"Error reading or writing file: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

        return self.contacts_address_list