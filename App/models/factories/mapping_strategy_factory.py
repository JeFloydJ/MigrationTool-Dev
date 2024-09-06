import os
import sys
from typing import List, Dict
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from models.mappings import organization_mapping_strategy
from models.mappings import phone_mapping_strategy
from models.mappings import address_mapping_strategy
from models.mappings import households_mapping_strategy
from models.mappings import relationships_mapping_strategy
from models.mappings import emails_mapping_strategy
from models.mappings import contacts_mapping_strategy
from models.entities import origin_platform
from entities import object

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
class MappingStrategyFactory:
    """
    Factory class for making mappings between Salesforce and Altru reports based on the provided entity type,
    data origin, and report name.
    """
    def __init__(self):
        self.OrganizationMapping: List[Dict] = []
        self.organizationRelationMapping: List[Dict] = []
        self.organizationPhoneMapping: List[Dict] = []
        self.organizationUpdatePhoneMapping: List[Dict] = []
        self.organizationAddressMapping: List[Dict] = []
        self.HouseholdsMapping: List[Dict] = []
        self.ContactsMapping: List[Dict] = []
        self.ContactsPhoneMapping: List[Dict] = []
        self.ContactsPhoneUpdateMapping: List[Dict] = []
        self.ContactsEmailMapping: List[Dict] = []
        self.ContactsEmailUpdateMapping: List[Dict] = []
        self.ContactAddressMapping: List[Dict] = []
        self.ContactsRelationshipsMappingStrategy: List[Dict] = []
        self.households_external_list: List[Dict] = []
        self.contacts_ids: List[str] = []

    def create_strategy(self, entity_type: str, data_origin: origin_platform, report_name: str, input_csv: str) -> None:
        """
        Method to create and assign the appropriate CleanupStrategy instance based on the
        provided entity type, data origin, and report name.
        """
        if entity_type == object.SalesforceObject.Account and data_origin == origin_platform.OriginPlatform.Altru and report_name == "Veevart Organizations Report test":
            self.OrganizationMapping = organization_mapping_strategy.OrganizationMappingStrategy(input_csv).make_mapping()
        elif entity_type == object.SalesforceObject.Account and data_origin == origin_platform.OriginPlatform.Altru and report_name == "Veevart Organizations Relationships report test":
            self.organizationRelationMapping = relationships_mapping_strategy.OrganizationAffilationStrategy(input_csv).make_mapping()
        elif entity_type == object.SalesforceObject.Account and data_origin == origin_platform.OriginPlatform.Altru and report_name == "Veevart Organization Phones Report test":
            self.organizationPhoneMapping = phone_mapping_strategy.OrganizationsPhoneStrategy(input_csv).make_mapping()
            self.organizationUpdatePhoneMapping = phone_mapping_strategy.OrganizationsPhoneUpdateStrategy(input_csv).make_mapping()
        elif entity_type == object.SalesforceObject.Account and data_origin == origin_platform.OriginPlatform.Altru and report_name == "Veevart Organization Addresses Report test":
            self.organizationAddressMapping = address_mapping_strategy.OrganizationsAddressStrategy(input_csv).make_mapping()
        elif entity_type == object.SalesforceObject.Account and data_origin == origin_platform.OriginPlatform.Altru and report_name == "Veevart HouseHolds Report test":
            self.HouseholdsMapping, self.households_external_list = households_mapping_strategy.HouseholdsMappingStrategy(input_csv).make_mapping()

        elif entity_type == object.SalesforceObject.Contact and data_origin == origin_platform.OriginPlatform.Altru and report_name == "Veevart Contacts Report test":
            self.ContactsMapping = contacts_mapping_strategy.ContactsMappingStrategy(input_csv).make_mapping(self.households_external_list)

        elif entity_type == object.SalesforceObject.Contact and data_origin == origin_platform.OriginPlatform.Altru and report_name == "Veevart Contacts Report Phones test":
            self.ContactsPhoneMapping = phone_mapping_strategy.ContactsPhoneStrategy(input_csv).make_mapping()
            self.ContactsPhoneUpdateMapping = phone_mapping_strategy.ContactsPhoneUpdateStrategy(input_csv).make_mapping()
        elif entity_type == object.SalesforceObject.Contact and data_origin == origin_platform.OriginPlatform.Altru and report_name == "Veevart Contacts Report Email test":
            self.ContactsEmailMapping = emails_mapping_strategy.EmailContactsStrategy(input_csv).make_mapping()
            self.ContactsEmailUpdateMapping = emails_mapping_strategy.EmailContactsUpdateStrategy(input_csv).make_mapping()
        elif entity_type == object.SalesforceObject.Contact and data_origin == origin_platform.OriginPlatform.Altru and report_name == "Veevart Contacts Relationships report test":
            self.ContactsRelationshipsMappingStrategy = relationships_mapping_strategy.ContactsRelationshipStrategy(input_csv).make_mapping()
        else: 
            raise ValueError(f"Unknown entity type: {entity_type} {data_origin} {report_name}")

    def called_factory(self, accounts_report_names: list, contacts_report_names: list) -> None:
        """
        Method to create strategies for both organizations and contacts based on provided report names.
        """
        for report_name in accounts_report_names:
            self.create_strategy(
                object.SalesforceObject.Account, 
                origin_platform.OriginPlatform.Altru, 
                report_name,
                ABS_PATH.format(f'data/{report_name}.csv')
            )

        for report_name in contacts_report_names:
            self.create_strategy(
                object.SalesforceObject.Contact, 
                origin_platform.OriginPlatform.Altru, 
                report_name,
                ABS_PATH.format(f'data/{report_name}.csv')
            )

