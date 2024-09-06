from models.cleanup.cleanup_strategy import CleanupStrategy
import csv

class ContactsEmailCleanupStrategy(CleanupStrategy):
    """
    Concrete implementation of CleanupStrategy for cleaning up contact email data.
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
                no_email = headers.index('Email Addresses\\Do not email')
                contact_primary_address = headers.index('Email Addresses\\Primary email address')
                
                for row in data:
                    if row[no_email] == 'Yes':
                        row[no_email] = 'True'
                    else:
                        row[no_email] = 'False'

                    if row[contact_primary_address] == 'Yes':
                        row[contact_primary_address] = 'True'
                    else:
                        row[contact_primary_address] = 'False'

            with open(self.output_csv, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f, delimiter=';')
                writer.writerow(headers)
                writer.writerows(data)

        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}") 