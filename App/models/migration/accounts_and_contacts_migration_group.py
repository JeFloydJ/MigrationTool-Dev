import os 
import sys
from typing import List
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from models.factories import mapping_strategy_factory
from models.mappings import contacts_mapping_strategy
from models.mappings import address_mapping_strategy
from models.migration.migration_group import migrationGroup

current_dir = os.path.dirname(os.path.abspath(__file__))
split_path = current_dir.split(os.sep)
app_index = split_path.index("App")
base_path = os.sep.join(split_path[:app_index + 1])
ABS_PATH = os.path.join(base_path, "{}")


accounts_report_names = [
            "Veevart Organizations Report test",
            "Veevart Organizations Relationships report test",
            "Veevart Organization Phones Report test",
            "Veevart Organization Addresses Report test",
            "Veevart HouseHolds Report test"
]

contacts_report_names = [
            "Veevart Contacts Report test",
            "Veevart Contacts Report Phones test",
            "Veevart Contacts Report Email test",
            "Veevart Contacts Relationships report test"
]

class AccountsAndContactsMigrationGroup(migrationGroup):
    """
    Adapter class for processing data and sending it to Salesforce using different strategies.
    """
    
    def __init__(self, report_names: List[str]) -> None:
        """
        Initialize the FundRaisingMigrationGroup with the given report names.

        Args:
            report_names (List[str]): The names of the reports to be processed.

        Returns:
            None
        """
        super().__init__(report_names)
        self.dic_households_ids = {}
        self.dic_accounts = {}
        self.dic_households = {}

    def process_data(self) -> None:
        """
        Processes data using the specified strategy and sends it to Salesforce.

        Args:
            None

        Returns:
            None
        """
        
        global dic_accounts

        mapping_factory = mapping_strategy_factory.MappingStrategyFactory()
        mapping_factory.called_factory(accounts_report_names, contacts_report_names)
        if mapping_factory.OrganizationMapping:
            self.strategy.send_data(mapping_factory.OrganizationMapping, 'Account', 'Organizations', 'Organizations', 'Auctifera__Implementation_External_ID__c')  
        if mapping_factory.organizationPhoneMapping:
            self.strategy.send_data(mapping_factory.organizationPhoneMapping, 'vnfp__Legacy_Data__c', 'Organizations', 'phones', 'vnfp__Implementation_External_ID__c')
        if mapping_factory.organizationUpdatePhoneMapping:
            self.strategy.send_data(mapping_factory.organizationUpdatePhoneMapping, 'Account', 'Organizations', 'phones_update', 'Auctifera__Implementation_External_ID__c')            
        if mapping_factory.organizationAddressMapping:
            self.strategy.send_data(mapping_factory.organizationAddressMapping, 'npsp__Address__c', 'Organizations', 'address', 'vnfp__Implementation_External_ID__c')
        if mapping_factory.HouseholdsMapping:
            self.strategy.send_data(mapping_factory.HouseholdsMapping, 'Account', 'Households', 'HouseHolds', 'Auctifera__Implementation_External_ID__c')
        if mapping_factory.ContactsMapping:
            results = self.strategy.send_data(mapping_factory.ContactsMapping, 'Contact', 'Contacts', 'Contacts', 'Auctifera__Implementation_External_ID__c')
            contacts_strategy = contacts_mapping_strategy.ContactsMappingStrategy(ABS_PATH.format('data/Veevart Contacts Report Address test'))
            dic_accounts = contacts_strategy.process_contacts_ids(results)
        if mapping_factory.ContactsPhoneMapping:
            self.strategy.send_data(mapping_factory.ContactsPhoneMapping, 'vnfp__Legacy_Data__c', 'Contacts', 'phones', 'vnfp__Implementation_External_ID__c')
        if mapping_factory.ContactsPhoneUpdateMapping:
            self.strategy.send_data(mapping_factory.ContactsPhoneUpdateMapping, 'Account', 'Contacts', 'phones_update', 'Auctifera__Implementation_External_ID__c')            
        if mapping_factory.ContactsEmailMapping:
            self.strategy.send_data(mapping_factory.ContactsEmailMapping, 'vnfp__Legacy_Data__c', 'Contacts', 'emails', 'vnfp__Implementation_External_ID__c')
        if mapping_factory.ContactsEmailUpdateMapping:
            self.strategy.send_data(mapping_factory.ContactsEmailUpdateMapping, 'Contact', 'Contacts', 'emails_update', 'Auctifera__Implementation_External_ID__c')
        AddressData = address_mapping_strategy.ContactsAddressStrategy(ABS_PATH.format('data/Veevart Contacts Report Address test.csv')).make_mapping(dic_accounts)
        if AddressData:
            self.strategy.send_data(AddressData, 'npsp__Address__c', 'Contacts', 'address', 'vnfp__Implementation_External_ID__c')

        if mapping_factory.organizationRelationMapping:
            self.strategy.send_data(mapping_factory.organizationRelationMapping, 'npe5__Affiliation__c', 'Contacts', 'relation', 'vnfp__Implementation_External_ID__c')
        
        if mapping_factory.ContactsRelationshipsMappingStrategy:
            self.strategy.send_data(mapping_factory.ContactsRelationshipsMappingStrategy, 'npe4__Relationship__c', 'Organizations', 'relation', 'vnfp__Implementation_External_ID__c')
