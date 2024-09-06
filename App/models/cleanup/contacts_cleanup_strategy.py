from models.cleanup.cleanup_strategy import CleanupStrategy
import csv

class ContactsCleanupStrategy(CleanupStrategy):
    """
    Concrete implementation of CleanupStrategy for cleaning up contact data.
    """
    def cleanup(self) -> None:
        """
        Clean up the data in the contact CSV by converting 'Yes'/'No' to 'True'/'False'.

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
                primary_contact = headers.index('Households Belonging To\\Is primary contact')
                deceased = headers.index('Deceased')
                gives_anonymously = headers.index('Gives anonymously')
                
                for row in data:
                    if row[primary_contact] == 'Yes':
                        row[primary_contact] = 'True'
                    else:
                        row[primary_contact] = 'False'

                    if row[deceased] == 'Yes':
                        row[deceased] = 'True'
                    else:
                        row[deceased] = 'False'

                    if row[gives_anonymously] == 'Yes':
                        row[gives_anonymously] = 'True'
                    else:
                        row[gives_anonymously] = 'False'

            with open(self.output_csv, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f, delimiter=';')
                writer.writerow(headers)
                writer.writerows(data)

        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")