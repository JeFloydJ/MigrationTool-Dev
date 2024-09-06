from models.cleanup.cleanup_strategy import CleanupStrategy
import csv

class OrganizationsPhoneCleanupStrategy(CleanupStrategy):
    """
    Concrete implementation of CleanupStrategy for cleaning up organization phone data.
    """
    def cleanup(self) -> None:
        """
        Clean up the data in the organization phone CSV by converting 'Yes'/'No' to 'True'/'False'.

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
                phones_no_call = headers.index('Phones\\Do not call')
                primary_phone = headers.index('Phones\\Primary phone number')
                
                for row in data:
                    if row[phones_no_call] == 'Yes':
                        row[phones_no_call] = 'True'
                    else:
                        row[phones_no_call] = 'False'
                        
                    if row[primary_phone] == 'Yes':
                        row[primary_phone] = 'True'
                    else:
                        row[primary_phone] = 'False'
                
            with open(self.output_csv, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f, delimiter=';')
                writer.writerow(headers)
                writer.writerows(data)

        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

class ContactsPhoneCleanupStrategy(CleanupStrategy):
    """
    Concrete implementation of CleanupStrategy for cleaning up contact phone data.
    """
    def cleanup(self) -> None:
        """
        Clean up the data in the contact phone CSV by converting 'Yes'/'No' to 'True'/'False'.

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
                phone_no_call = headers.index('Phones\\Do not call')
                contact_primary_phone = headers.index('Phones\\Primary phone number')
                
                for row in data:
                    if row[phone_no_call] == 'Yes':
                        row[phone_no_call] = 'True'
                    else:
                        row[phone_no_call] = 'False'

                    if row[contact_primary_phone] == 'Yes':
                        row[contact_primary_phone] = 'True'
                    else:
                        row[contact_primary_phone] = 'False'

            with open(self.output_csv, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f, delimiter=';')
                writer.writerow(headers)
                writer.writerows(data)

        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

