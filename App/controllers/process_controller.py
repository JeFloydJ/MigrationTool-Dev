import os
import sys
from typing import List
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from models.migration.accounts_and_contacts_migration_group import AccountsAndContactsMigrationGroup
from models.factories.cleanup_strategy_factory import CleanupStrategyFactory

current_dir = os.path.dirname(os.path.abspath(__file__))

# Search for the 'App' directory in the path and slice the path up to that directory
split_path = current_dir.split(os.sep)
app_index = split_path.index("App")
base_path = os.sep.join(split_path[:app_index + 1])
ABS_PATH = os.path.join(base_path, "{}")


# Paths to 'finish.txt' and 'error.txt'
finish_path = ABS_PATH.format('data/finish.txt')
error_path = ABS_PATH.format('data/error.txt')

# Delete the 'finish.txt' file if it exists
if os.path.exists(finish_path):
    os.remove(finish_path)

# Delete the 'error.txt' file if it exists
if os.path.exists(error_path):
    os.remove(error_path)

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

class ProcessController:
    """
    Controller class for processing data and sending it to Salesforce.
    """

    def __init__(self, report_names: List[str]) -> None:
        """
        Initialize the ProcessController with the given report names.

        Args:
            report_names (List[str]): The names of the reports to be processed.

        Returns:
            None
        """
        self.report_names = report_names

    def sent_data(self) -> None:
        """
        Processes data using the specified strategy and sends it to Salesforce.

        Args:
            None

        Returns:
            None
        """
        try:
            # Process the data
            accounts_and_contacts_factory = CleanupStrategyFactory()
            accounts_and_contacts_factory.called_factory(organizations_report_names, contacts_report_names)
            contacts_accounts = AccountsAndContactsMigrationGroup(self.report_names)
            contacts_accounts.process_data()

            # Write 'finish' to the 'finish.txt' file
            with open(finish_path, 'w') as f:
                f.write('finish')

        except Exception as e:
            with open(error_path, 'w') as f:
                f.write(str(e))

report_names = organizations_report_names + contacts_report_names
controller = ProcessController(report_names)
controller.sent_data()