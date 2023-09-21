import glob
import os

project_id = 'mnes-sandbox-naito'  # replace with your GCP project ID
location = 'asia-northeast1'  # replace with the parent dataset's location
dataset_id = 'Mobile_healthcare'  # replace with the parent dataset's ID
dicom_store_id = 'dicomstore1'  # replace with the DICOM store ID
folder_path = './images'
dcm_files = glob.glob(os.path.join(folder_path, '**', '*.*'), recursive=True)  # replace with DICOM files

print(dcm_files)

def dicomweb_store_instance(project_id, location, dataset_id, dicom_store_id, dcm_files):
    from google.auth.transport import requests
    from google.oauth2 import service_account

    credentials = service_account.Credentials.from_service_account_file(
        "mnes-sandbox-naito-0ae10544389b.json"
    )
    scoped_credentials = credentials.with_scopes(
        ["https://www.googleapis.com/auth/cloud-platform"]
    )
    session = requests.AuthorizedSession(scoped_credentials)

    base_url = "https://healthcare.googleapis.com/v1"
    url = f"{base_url}/projects/{project_id}/locations/{location}"
    dicomweb_path = "{}/datasets/{}/dicomStores/{}/dicomWeb/studies".format(
        url, dataset_id, dicom_store_id
    )

    for dcm_file in dcm_files:
        with open(dcm_file, "rb") as dcm:
            dcm_content = dcm.read()
            print(dcm_file)

        headers = {"Content-Type": "application/dicom"}

        response = session.post(dicomweb_path, data=dcm_content, headers=headers)
        response.raise_for_status()
        print(f"Stored DICOM instance from {dcm_file}:")
        print(response.text)

dicomweb_store_instance(project_id, location, dataset_id, dicom_store_id, dcm_files)
