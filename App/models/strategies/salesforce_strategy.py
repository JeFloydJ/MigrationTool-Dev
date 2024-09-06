from abc import ABC, abstractmethod
import csv
import io
import os
import logging
from simple_salesforce import Salesforce
from typing import Dict, List

current_dir = os.path.dirname(os.path.abspath(__file__))

# Search for the 'App' directory in the path and slice the path up to that directory
split_path = current_dir.split(os.sep)
app_index = split_path.index("App")
base_path = os.sep.join(split_path[:app_index + 1])

# Create the ABS_PATH with a placeholder for future formatting
ABS_PATH = os.path.join(base_path, "{}")

# Set up logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
                    force=True)

logger = logging.getLogger(__name__)


class DataStrategy(ABC):
    """
    Abstract base class for data strategies. Defines the interface that all data strategies must implement.
    """
    @abstractmethod
    def send_data(self, data: List[Dict[str, any]], object_name: str, principal_object: str, object : str, external_id: str) -> None:
        """
        Send data to Salesforce.

        Args:
            data (List[Dict[str, any]]): The data to be sent to Salesforce.
            object_name (str): The name of the Salesforce object to which data will be sent.
            principal_object (str): The name of the principal object (contact/organization/households) for report.
            object(str): name of the object to be sent to salesforce (ex: address of organization)
            external_id (str): The external ID field to be used for upserting the data.

        Returns:
            None
        """
        pass

class SalesforceStrategy(DataStrategy):
    """
    A data strategy implementation for sending data to Salesforce using the Bulk API.
    """
    def __init__(self) -> None:
        """
        Initialize the SalesforceStrategy instance. Reads the Salesforce token and initializes the Salesforce connection.
        """
        self.token: str = self._read_token()
        self.access_token: str = self._read_access_token()
        self.sf: Salesforce = self._initialize_salesforce()

    def _read_token(self) -> str:
        """
        Read the Salesforce instance token from a file.

        Returns:
            str: The Salesforce instance token.
        """
        with open(ABS_PATH.format('data/salesforce_instance.txt'), 'r') as f:
            instance: str = f.read().strip()

        if 'https://' in instance:
            instance = instance.split('https://')[1]

        return instance

    def _read_access_token(self) -> str:
        """
        Read the Salesforce access token from a file.

        Returns:
            str: The Salesforce access token.

        """
        with open(ABS_PATH.format('data/salesforce_token.txt'), 'r') as f:
            return f.read().strip()

    def _initialize_salesforce(self) -> Salesforce:
        """
        Initialize the Salesforce connection using the instance token and access token.

        Returns:
            Salesforce: An instance of the Salesforce class from the simple_salesforce library.

        """
        return Salesforce(instance=self.token, session_id=self.access_token)
        
    def get_organization_id(self) -> str:
        """
        Get the ID of the organization record type in Salesforce.

        Returns:
            str: The ID of the organization record type.
        """
        query = self.sf.query("SELECT Id FROM RecordType WHERE DeveloperName = 'organization' AND IsActive = true")
        Id = query['records'][0]['Id']
        return Id

    def get_households_id(self) -> str:
        """
        get AccountId for contacts in org

        Returns:
            str: The ID of the organization record type.
        """
        query = self.sf.query("SELECT Id FROM RecordType WHERE DeveloperName = 'HH_Account' AND IsActive = true")
        Id = query['records'][0]['Id']
        return Id

    def get_number_of_contacts(self) -> int:
        """
        Get numbers of contacts with implementation external id.

        Returns:
            dict : return hash table like: {'Auctifera__Implementation_External_ID__c': 'AccountId'}
        """
        ans = self.sf.query_all("SELECT COUNT(Id) FROM Contact WHERE Auctifera__Implementation_External_ID__c != '' ")
        return ans['records'][0]['expr0']
    
    def get_account_id(self) -> Dict[str, str]:
        """
        Get the ID of the household record type in Salesforce.

        Returns:
            dict : return hash table like: {'Auctifera__Implementation_External_ID__c': 'AccountId'}
        """
        query_result = {}
        query = "SELECT Id, AccountId, Auctifera__Implementation_External_ID__c FROM Contact WHERE Auctifera__Implementation_External_ID__c != null"
        max_records = self.get_number_of_contacts()
        try:
            results = self.sf.bulk2.Contact.query(query, max_records=max_records)
            csv_content = ''.join(results)
            csv_file = io.StringIO(csv_content)
            reader = csv.DictReader(csv_file)
            
            for row in reader:
                external_id = row['Auctifera__Implementation_External_ID__c']
                account_id = row['AccountId']
                query_result[external_id] = account_id

            logger.info("Datos obtenidos correctamente")

        except Exception as e:
            logger.info(f"Error al ejecutar la consulta: {e}")

        return query_result

    def send_data(self, data:list[dict[str, any]], object_name: str, principal_object: str, object: str ,external_id: str) -> List[Dict[str, str]]:
        """
        Send data to a specified Salesforce object using the bulk API.

        Args:
            data (List[Dict[str, any]]): The data to be sent to Salesforce.
            object_name (str): The name of the Salesforce object to which data will be sent.
            principal_object (str): The name of the principal object (contact/organization/households) for report.
            object(str): name of the object to be sent to salesforce (ex: address of organization)
            external_id (str): The external ID field to be used for upserting the data.
        Returns:
            None
        """
    
        results  = self.sf.bulk.__getattr__(object_name).upsert(
            data,
            external_id,
            batch_size='auto',
            use_serial=True
        )
        with open(ABS_PATH.format(f'logs/{principal_object}_{object}_response.txt'), 'w') as f:
            f.write(str(results))
            
        return results