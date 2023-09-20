def dicomweb_store_instance(project_id, location, dataset_id, dicom_store_id, dcm_file):
    """Handles the POST requests specified in the DICOMweb standard.

    See https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/healthcare/api-client/v1/dicom
    before running the sample."""
    # Imports Python's built-in "os" module
    import os

    # Imports the google.auth.transport.requests transport
    from google.auth.transport import requests

    # Imports a module to allow authentication using a service account
    from google.oauth2 import service_account

    # Gets credentials from the environment.
    credentials = service_account.Credentials.from_service_account_file(
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
    )
    scoped_credentials = credentials.with_scopes(
        ["https://www.googleapis.com/auth/cloud-platform"]
    )
    # Creates a requests Session object with the credentials.
    session = requests.AuthorizedSession(scoped_credentials)

    # URL to the Cloud Healthcare API endpoint and version
    base_url = "https://healthcare.googleapis.com/v1"

    import glob

    # TODO(developer): Uncomment these lines and replace with your values.
    project_id = 'mnes-sandbox-naito'  # replace with your GCP project ID
    location = 'asia-northeast1'  # replace with the parent dataset's location
    dataset_id = 'Mobile_healthcare'  # replace with the parent dataset's ID
    dicom_store_id = 'dicomstore1' # replace with the DICOM store ID
    folder_path = './images'
    dcm_file = glob.glob(os.path.join(folder_path, '**', '*.dcm'), recursive=True)  # replace with a DICOM file
    url = f"{base_url}/projects/{project_id}/locations/{location}"

    dicomweb_path = "{}/datasets/{}/dicomStores/{}/dicomWeb/studies".format(
        url, dataset_id, dicom_store_id
    )

    with open(dcm_file, "rb") as dcm:
        dcm_content = dcm.read()

    # Sets required "application/dicom" header on the request
    headers = {"Content-Type": "application/dicom"}

    response = session.post(dicomweb_path, data=dcm_content, headers=headers)
    response.raise_for_status()
    print("Stored DICOM instance:")
    print(response.text)
    return response
