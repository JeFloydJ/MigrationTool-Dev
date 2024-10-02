import csv
import os
import json

class ReportProcessor:
    """
    fix logs of salesforce, generate json files and generate reports of sent data

    Args:
        txt_path (str): The path to the text file.
        json_path (str): The path to the JSON file.
        csv_path (str): The path to the
        
    Returns:
        None
    """
    
    def __init__(self, txt_path, json_path, csv_path):
        self.txt_path = txt_path
        self.json_path = json_path
        self.csv_path = csv_path

    def convert_to_json(self) -> None:
        """
        Convert a text file to JSON format by fixing logs from Salesforce and generating a JSON file.

        Args:
            None

        Returns:
            None
        """
        try:
            with open(self.txt_path, 'r') as file, open(self.json_path, 'w') as file_json:
                for line in file:
                    new_line = line.replace("'", '"').replace("True", 'true').replace("False", 'false').replace("None", 'null')
                    file_json.write(new_line)
        except FileNotFoundError as e:
            print(f"Error: {e}")
        except IOError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def generate_report_send_data(self, report_name: str) -> None:
        """
        Generate a report of submitted data from the JSON file and save it to a CSV file.

        Args:
            report_name (str): The name of the report.

        Returns:
            None
        """
        try:
            json_path = os.path.join(os.path.dirname(self.json_path), f"{report_name}.json")
            with open(json_path) as json_file:
                data = json.load(json_file)
                success_true = 0
                success_false = 0
                created_true = 0
                created_false = 0
                success_ids_true = []
                success_ids_false = []
                created_ids_true = []
                created_ids_false = []
                errors_list = []

                for item in data:
                    if item['success']:
                        success_true += 1
                        success_ids_true.append(item['id'])
                    else:
                        success_false += 1
                        success_ids_false.append(item['id'])
                    
                    if item['created']:
                        created_true += 1
                        created_ids_true.append(item['id'])
                    else:
                        created_false += 1
                        created_ids_false.append(item['id'])
                    
                    if item['errors']:
                        for error in item['errors']:
                            errors_list.append({'id': item['id'], 'error': error})

            csv_file_path = os.path.join(os.path.dirname(self.csv_path), f"{report_name}.csv")
            
            with open(csv_file_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                
                writer.writerow(['Operation', 'True', 'False', 'Id', 'Error', 'Message Error'])

                writer.writerow(['Success', success_true, success_false, '', '', ''])
                for id in success_ids_true:
                    writer.writerow(['', '', '', id, '', ''])
                for id in success_ids_false:
                    writer.writerow(['', '', '', id, '', ''])
                
                writer.writerow(['Created', created_true, created_false, '', '', ''])
                for id in created_ids_true:
                    writer.writerow(['', '', '', id, '', ''])
                for id in created_ids_false:
                    writer.writerow(['', '', '', id, '', ''])

                writer.writerow(['Error', '', '', '', len(errors_list), ''])
                for error in errors_list:
                    writer.writerow(['', '', '', error['id'], 1, json.dumps(error['error'])])

        except FileNotFoundError as e:
            print(f"Error: {e}")
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")
        except IOError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")