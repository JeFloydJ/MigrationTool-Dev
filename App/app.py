# Import necessary modules
import zipfile
from flask import Flask, request, render_template, redirect, jsonify, send_file
import logging
import requests
import urllib.parse
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor
from auth.auth_altru import auth_altru
from auth.auth_salesforce import auth_salesforce
from util.event_report_data import ReportProcessor
import os
import glob
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

#absolute path of files
current_dir = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(current_dir)
ABS_PATH = os.path.join(BASE_DIR, "App", "{}")

# Set up logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
                    force=True)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(
    __name__, 
    static_folder=os.path.join('views', 'static'), 
    template_folder=os.path.join('views', 'templates')
)

# Define client IDs
client_ids = {
    'salesforce': os.getenv("CLIENT_ID_SALESFORCE"),
    'altru': os.getenv("CLIENT_ID_SKY_API")
}

# Define client secrets
client_secrets = {
    'salesforce': os.getenv("CLIENT_SECRET_SALESFORCE"),
    'altru': os.getenv("CLIENT_SECRET_SKY_API")
}

# Define redirect URIs
redirect_uris = {
    'skyapi': os.getenv("REDIRECT_URI_SKY_API"),
    'salesforce': os.getenv("REDIRECT_URI_SALESFORCE")
}

# Define token URLs
token_urls = {
    'salesforce': 'https://login.salesforce.com/services/oauth2/token',
    'altru': 'https://oauth2.sky.blackbaud.com/token'
}

# List of files with tokens
token_files = ['altru_token.txt', 'altru_refresh_token.txt', 'salesforce_token.txt', 'salesforce_refresh_token.txt', 'salesforce_instance.txt', 'data.txt', 'finish.txt']

#name of the transferred data report
reports_of_sent_data = [
    "Contacts_Contacts_response",            
    "Organizations_Organizations_response",
    "Contacts_address_response",             
    "Contacts_emails_response",              
    "Organizations_address_response",
    "Contacts_emails_update_response",       
    "Organizations_phones_response",
    "Contacts_phones_response",             
    "Organizations_phones_update_response",
    "Contacts_phones_update_response",      
    "Organizations_relation_response",
    "Contacts_relation_response",           
    "Households_HouseHolds_response",
]


# delete the content in each token file 
for filename in token_files:
    save_path_files = os.path.join(ABS_PATH.format(f'data/{filename}'))
    open(save_path_files, 'w').close()

def is_empty(file: str) -> bool:
    """
    Verifies if the given file is empty.

    This function reads the content of the file and checks if it is empty or not.

    Args:
        file (TextIO): A file-like object (e.g., from open() in text mode).

    Returns:
        bool: True if the file is empty, False otherwise.
    """
    return not bool(file.read())

 
@app.route('/generate-report', methods=['GET'])
def generate_report():
    """
    Generates a report of data submitted and returns a ZIP file containing CSV reports.

    This endpoint processes each report listed in `reports_of_sent_data`, converts associated
    text files to JSON, generates a report from the data, and collects CSV files. Finally, it
    creates a ZIP file containing all the CSV reports and returns it as an attachment.

    Returns:
        Response: A Flask response object with the ZIP file attached for download.
    """
    all_csv_paths = []

    for report in reports_of_sent_data:
        txt_path = ABS_PATH.format(f'logs/{report}.txt')
        json_path = ABS_PATH.format(f'logs/{report}.json')
        csv_path = ABS_PATH.format(f'reports/{report}.csv')
        
        processor = ReportProcessor(txt_path, json_path, csv_path)
        
        processor.convert_to_json()
        
        processor.generate_report_send_data(report)
        
        all_csv_paths.append(csv_path)

    zip_file_path = os.path.join(os.path.dirname(csv_path), 'reports.zip')
    with zipfile.ZipFile(zip_file_path, 'w') as zip_file:
        for csv_path in all_csv_paths:
            zip_file.write(csv_path, os.path.basename(csv_path))

    return send_file(zip_file_path, as_attachment=True)


@app.route('/validator') 
def validate_token():
    """
    Validates the status of a process based on the existence of specific files.

    This function checks if the process has completed, encountered an error, or is still in progress
    based on the presence of 'finish.txt' and 'error.txt' files in the specified directory.

    Returns:
        Response: A Flask response object with a JSON payload indicating the status of the process.
    """
    try:
        finish_path = ABS_PATH.format('data/finish.txt')
        if os.path.exists(finish_path):
            return jsonify({'status': 200})

        error_path = ABS_PATH.format('data/error.txt')
        if os.path.exists(error_path):
            with open(error_path, 'r') as f:
                error_message = f.read()
            return jsonify({'status': 'error', 'message': error_message})        
    
        return jsonify({'status': 'in_progress'})
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/upload', methods=["POST"])
def upload():
    """
    Handles the upload of CSV files and stores them in the project directory.

    This endpoint processes uploaded files, saving only CSV files to a specified directory.
    It also creates or updates a text file to indicate that data has been uploaded.

    Returns:
        Response: A Flask response object with a JSON payload indicating the success status of the operation,
                  or a redirect if the request method is not POST.
    """
    if request.method == 'POST':
        if request.files:
            uploaded_files = request.files.getlist("filename")
            for file in uploaded_files:
                save_filename = os.path.basename(file.filename)
                if file.filename.endswith('.csv'):
                    save_path = os.path.join(ABS_PATH.format('data'), f'{save_filename}')
                    file.save(save_path)
            try:
                save_data_path = os.path.join(ABS_PATH.format(f'data/data.txt'))
                with open(save_data_path, 'w') as f:
                    f.write('data subida')
            except Exception as e:
                logger.error(f"Error writing to file: {e}")

            return jsonify({'message': 'Successfully saved', 'success': True})

    return redirect('/')

@app.route('/delete', methods=["POST"])
def delete():
    """
    Deletes all CSV files from the specified directory.

    This endpoint searches for all CSV files in the 'data' directory and deletes them.

    Returns:
        Response: A Flask response object with a JSON payload indicating the success status of the deletion operation.
    """
    save_path = os.path.join(ABS_PATH.format('/data'), '*.csv')
    files = glob.glob(save_path)
    for file_name in files:
        os.remove(file_name)
    return jsonify({'message': 'files deleted', 'success': True})

@app.route('/')
def index():
    """
    Renders the index page with status information based on file contents.

    This endpoint checks the existence and content of several files to determine the status of various
    components, such as Salesforce login, AWS data availability, and data transfer completion.
    It then renders the 'index.html' template with relevant context variables.

    Returns:
        Response: A Flask response object with the rendered 'index.html' template, including context variables
                  indicating the status of Salesforce login, data availability, data transfer completion,
                  and whether the transfer page should be shown.
    """
    loggedSalesforce = False
    data = False
    transferData = False
    transferPage = False
    
    with open(ABS_PATH.format('data/salesforce_token.txt'), 'r') as f:
        if not is_empty(f):
            loggedSalesforce = True 

    # Si está conectado a Sky Api, la variable es True
    # with open(ABS_PATH.format('altru_token.txt'), 'r') as f:
    #     if not isEmpty(f):
    #         loggedSkyApi = True

    with open(ABS_PATH.format('data/data.txt'), 'r') as f:
        if not is_empty(f):
            data = True 

    with open(ABS_PATH.format('data/finish.txt'), 'r') as f:
        if not is_empty(f):
            transferData = True

    if loggedSalesforce and data:
        transferPage = True
 
    return render_template('index.html', transferPage=transferPage, loggedSalesforce=loggedSalesforce, transferData=transferData, data=data)

@app.route('/process', methods=['GET'])
def transfer_data():
    """
    Starts a background thread to execute a script for data transfer.

    This endpoint triggers the execution of a Python script in the background to handle data processing.
    The script is executed using `ThreadPoolExecutor` with the intention of running it asynchronously.

    Returns:
        dict: A dictionary with a status code indicating that the process has been started successfully.
    """
    executor = ThreadPoolExecutor(max_workers=2)

    executor.submit(os.system, f'python3 {ABS_PATH.format("controllers/process_controller.py")}')
    
    return {'status': 200}


@app.route('/salesforce/callback')
def get_salesforce_token():
    """
    Handles the Salesforce OAuth callback to obtain and store access tokens.

    This endpoint processes the callback from Salesforce after authorization,
    extracts the authorization code from the query parameters, and exchanges it
    for access and refresh tokens. The tokens and instance URL are then saved
    to files.

    Returns:
        Response: A Flask response object that redirects the user to the root URL
                  after processing the callback and saving the tokens.
    """
    # Define the service and API
    service = 'salesforce'
    api = 'salesforce'
    query = urllib.parse.urlparse(request.url).query
    query_components = dict(qc.split("=") for qc in query.split("&") if "=" in qc)

    if "code" in query_components:
        code = query_components["code"]
        access_token = query_components["code"]
        access_token = access_token.replace("%3D%3D", "==")

        with open(f'data/{service}_token.txt', 'w') as f:
            f.write(access_token)
        logger.info(access_token)
        token_url = "https://login.salesforce.com/services/oauth2/token"
        token_data = {
            "grant_type": "authorization_code",
            "code": access_token,
            "redirect_uri": redirect_uris[api],
            "client_id": client_ids[service],
            "client_secret": client_secrets[service]
        }
        token_response = requests.post(token_url, data=token_data)
        logger.info(token_response)
        if token_response.status_code == 200:
            access_token = token_response.json()["access_token"]
            refresh_token = token_response.json()["refresh_token"]
            instance = token_response.json()["instance_url"]
            logger.info(instance)
            try:
                save_path_access = os.path.join(ABS_PATH.format(f'data/{service}_token.txt'))
                with open(save_path_access, 'w') as f:
                    f.write(access_token)
                save_path_refresh = os.path.join(ABS_PATH.format(f'data/{service}_refresh_token.txt'))
                with open(save_path_refresh, 'w') as f:
                    f.write(refresh_token)
                save_path_instance = os.path.join(ABS_PATH.format(f'data/{service}_instance.txt'))
                with open(save_path_instance, 'w') as f:
                    f.write(instance)
            except Exception as e:
                logger.error(f"Error writing tokens to file: {e}")
        else:
            logger.warning(f"Token response error: {token_response.content}")
    return redirect('/')


@app.route('/auth/<service>', methods=['GET'])
def auth(service: str) -> str:
    """
    Redirects the user to the authorization URL for the specified service.

    This endpoint determines the appropriate authorization URL based on the provided
    service parameter. It then redirects the user to this URL for authentication.

    Args:
        service (str): The service for which the authorization URL is needed.
                       Expected values are 'altru' and 'salesforce'.

    Returns:
        Response: A Flask response object that redirects the user to the authorization URL.
    """
    if service == 'altru':
        auth_url = auth_altru()
    elif service == 'salesforce':
        auth_url = auth_salesforce()
    return redirect(auth_url)


#run the server in port 8000
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
