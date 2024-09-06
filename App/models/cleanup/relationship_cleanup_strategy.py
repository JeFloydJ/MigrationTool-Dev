from models.cleanup.cleanup_strategy import CleanupStrategy
import csv

class OrganizationsRelationshipCleanupStrategy(CleanupStrategy):
    """
    Concrete implementation of CleanupStrategy for cleaning up organization relationship data.
    """
    def cleanup(self) -> None:
        """
        Clean up the data in the organization relationship CSV by converting 'Yes'/'No' to 'True'/'False'.

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
                relationship_index = headers.index('Relationships\\Is primary contact')
                
                for row in data:
                    if row[relationship_index] == 'Yes':
                        row[relationship_index] = 'True'
                    else:
                        row[relationship_index] = 'False'
                    
            with open(self.output_csv, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f, delimiter=';')
                writer.writerow(headers)
                writer.writerows(data)

        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

class ContactsRelationshipsCleanupStrategy(CleanupStrategy):
    """
    Concrete implementation of CleanupStrategy for cleaning up contact relationships data.
    """
    def cleanup(self) -> None:
        """
        Clean up the data in the contact relationships CSV by converting 'Yes'/'No' to 'True'/'False'.

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
                is_primary = headers.index('Relationships\\Is primary contact')
                
                for row in data:
                    if row[is_primary] == 'Yes':
                        row[is_primary] = 'True'
                    else:
                        row[is_primary] = 'False'

            with open(self.output_csv, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f, delimiter=';')
                writer.writerow(headers)
                writer.writerows(data)

        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}") 
            