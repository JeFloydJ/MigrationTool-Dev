from models.cleanup.cleanup_strategy import CleanupStrategy
import csv

class OrganizationsCleanupStrategy(CleanupStrategy):
    """
    Concrete implementation of CleanupStrategy for cleaning up organization data.
    """

    def cleanup(self) -> None:
        """
        Clean up the data in the organization CSV by converting 'Yes'/'No' to 'True'/'False'.

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
                email_index = headers.index('Email Addresses\\Do not email')
                
                for row in data:
                    if row[email_index] == 'Yes':
                        row[email_index] = 'True'
                    else:
                        row[email_index] = 'False'
                    
            with open(self.output_csv, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f, delimiter=';')
                writer.writerow(headers)
                writer.writerows(data)

        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")



