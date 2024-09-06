
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from models.cleanup import cleanup_strategy
from models.cleanup import organizations_cleanup_strategy
from models.cleanup import relationship_cleanup_strategy
from models.cleanup import phone_cleanup_strategy
from models.cleanup import email_cleanup_strategy
from models.cleanup import contacts_cleanup_strategy
from models.cleanup import address_cleanup_strategy
from models.entities import origin_platform
from entities import object

current_dir = os.path.dirname(os.path.abspath(__file__))
split_path = current_dir.split(os.sep)
app_index = split_path.index("App")
base_path = os.sep.join(split_path[:app_index + 1])
ABS_PATH = os.path.join(base_path, "{}")

organizations_report_names = [
            "Veevart Organizations Report test",
            "Veevart Organizations Relationships report test",
            "Veevart Organization Phones Report test",
            "Veevart Organization Addresses Report test"
]
        
contacts_report_names = [
            "Veevart Contacts Report test",
            "Veevart Contacts Report Phones test",
            "Veevart Contacts Report Email test",
            "Veevart Contacts Report Address test",
            "Veevart Contacts Relationships report test"
]

class CleanupStrategyFactory:
    """
    Factory class for creating instances of CleanupStrategy based on the provided entity type,
    data origin, and report name.
    """

    @staticmethod
    def create_strategy(entity_type: str, data_origin: origin_platform, report_name: str, input_csv: str, output_csv: str) -> cleanup_strategy:
        """
        Static method to create and return an appropriate CleanupStrategy instance based on the
        provided entity type, data origin, and report name.
        """
        if entity_type == object.SalesforceObject.Account and data_origin == origin_platform.OriginPlatform.Altru and report_name == "Veevart Organizations Report test":
            strategy = organizations_cleanup_strategy.OrganizationsCleanupStrategy(input_csv, output_csv)
            strategy.cleanup()
        elif entity_type == object.SalesforceObject.Account and data_origin == origin_platform.OriginPlatform.Altru and report_name == "Veevart Organizations Relationships report test":
            strategy = relationship_cleanup_strategy.OrganizationsRelationshipCleanupStrategy(input_csv, output_csv)
            strategy.cleanup()
        elif entity_type == object.SalesforceObject.Account and data_origin == origin_platform.OriginPlatform.Altru and report_name == "Veevart Organization Phones Report test":
            strategy = phone_cleanup_strategy.OrganizationsPhoneCleanupStrategy(input_csv, output_csv)
            strategy.cleanup()
        elif entity_type == object.SalesforceObject.Account and data_origin == origin_platform.OriginPlatform.Altru and report_name == "Veevart Organization Addresses Report test":
            strategy = address_cleanup_strategy.OrganizationsAddressCleanupStrategy(input_csv, output_csv)
            strategy.cleanup()
        elif entity_type == object.SalesforceObject.Contact and data_origin == origin_platform.OriginPlatform.Altru and report_name == "Veevart Contacts Report test":
            strategy = contacts_cleanup_strategy.ContactsCleanupStrategy(input_csv, output_csv)
            strategy.cleanup()
        elif entity_type == object.SalesforceObject.Contact and data_origin == origin_platform.OriginPlatform.Altru and report_name == "Veevart Contacts Report Phones test":
            strategy = phone_cleanup_strategy.ContactsPhoneCleanupStrategy(input_csv, output_csv)
            strategy.cleanup()
        elif entity_type == object.SalesforceObject.Contact and data_origin == origin_platform.OriginPlatform.Altru and report_name == "Veevart Contacts Report Email test":
            strategy = email_cleanup_strategy.ContactsEmailCleanupStrategy(input_csv, output_csv)
            strategy.cleanup()
        elif entity_type == object.SalesforceObject.Contact and data_origin == origin_platform.OriginPlatform.Altru and report_name == "Veevart Contacts Report Address test":
            strategy = address_cleanup_strategy.ContactsAddressCleanupStrategy(input_csv, output_csv)
            strategy.cleanup()            
        elif entity_type == object.SalesforceObject.Contact and data_origin == origin_platform.OriginPlatform.Altru and report_name == "Veevart Contacts Relationships report test":
            strategy = relationship_cleanup_strategy.ContactsRelationshipsCleanupStrategy(input_csv, output_csv)
            strategy.cleanup()
        else: 
            raise ValueError(f"Unknown entity type: {entity_type} {data_origin} {report_name}")

    def called_factory(self, organizations_report_names: list, contacts_report_names: list):
        """
        Method to create strategies for both organizations and contacts based on provided report names.

        Args:
            organizations_report_names (list): List of organization report names.
            contacts_report_names (list): List of contact report names.
        """
        for report_name in organizations_report_names:
            self.create_strategy(
                object.SalesforceObject.Account, 
                origin_platform.OriginPlatform.Altru, 
                report_name,
                ABS_PATH.format(f'data/{report_name}.csv'),
                ABS_PATH.format(f'data/{report_name}.csv')
            )

        for report_name in contacts_report_names:
            self.create_strategy(
                object.SalesforceObject.Contact, 
                origin_platform.OriginPlatform.Altru, 
                report_name,
                ABS_PATH.format(f'data/{report_name}.csv'),
                ABS_PATH.format(f'data/{report_name}.csv')
            )

