from models.cleanup.cleanup_strategy import CleanupStrategy
import csv

class OrganizationsAddressCleanupStrategy(CleanupStrategy):
    """
    Concrete implementation of CleanupStrategy for cleaning up organization address data.
    """
    def cleanup(self) -> None:
        """
        Clean up the data in the organization address CSV by converting 'Yes'/'No' to 'True'/'False'.

        Args:
            None

        Returns:
            None
        """
        try:
            with open(self.input_csv, 'r', encoding='utf-8-sig') as f:
                reader = csv.reader(f, delimiter=';')
                headers = next(reader)
                
                if not headers:
                    raise ValueError("The file is empty or the delimiter is incorrect.")
                
                data = list(reader)
                primary_address = headers.index('Addresses\\Primary address')
                address_no_mail = headers.index('Addresses\\Do not mail')
                for row in data:
                    if row[primary_address] == 'Yes':
                        row[primary_address] = 'True'
                    else:
                        row[primary_address] = 'False'

                    if row[address_no_mail] == 'Yes':
                        row[address_no_mail] = 'True'
                    else:
                        row[address_no_mail] = 'False'

            with open(self.output_csv, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f, delimiter=';')
                writer.writerow(headers)
                writer.writerows(data)
        
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

class ContactsAddressCleanupStrategy(CleanupStrategy):
    """
    Concrete implementation of CleanupStrategy for cleaning up contact address data.
    """
    def cleanup(self) -> None:
        """
        Clean up the data in the contact email CSV by converting 'Yes'/'No' to 'True'/'False'.

        Args:
            None

        Returns:
            None
        """
        try:
            with open(self.input_csv, 'r', encoding='utf-8-sig') as f:
                reader = csv.reader(f, delimiter=';')
                headers = next(reader)
                
                if not headers:
                    raise ValueError("The file is empty or the delimiter is incorrect.")
                
                data = list(reader)
                primary_address = headers.index('Addresses\\Primary address')
                do_not_mail = headers.index('Addresses\\Do not mail')
                for row in data:
                    if row[primary_address] == 'Yes':
                        row[primary_address] = 'True'
                    else:
                        row[primary_address] = 'False'

                    if row[do_not_mail] == 'Yes':
                        row[do_not_mail] = 'True'
                    else:
                        row[do_not_mail] = 'False'

            with open(self.output_csv, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f, delimiter=';')
                writer.writerow(headers)
                writer.writerows(data)
        
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")