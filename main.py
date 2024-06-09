import base64
from googleapiclient import discovery

def import_dicom_instance(event, context):
    """Triggered by a change to a Cloud Storage bucket.
    Args:
        event (dict): Event payload.
        context (google.cloud.functions.Context): Metadata for the event.
    """
    file = event
    print(f"Processing file: {file['name']}.")

    # Extract bucket and object data from the event
    bucket_name = file['bucket']
    file_name = file['name']

    # Cloud Healthcare API configuration
    project_id = "da-kalbe"
    location = "asia-southeast2" 
    dataset_id = "test1"
    dicom_store_id = "output-dicom"

    # Construct the GCS URI for the uploaded file
    content_uri = f"{bucket_name}/{file_name}"

    # Call the import function
    import_dicom_instance_to_healthcare(
        project_id, location, dataset_id, dicom_store_id, content_uri
    )

def import_dicom_instance_to_healthcare(
    project_id, location, dataset_id, dicom_store_id, content_uri
):
    """Imports data into the DICOM store."""
    api_version = "v1"
    service_name = "healthcare"
    client = discovery.build(service_name, api_version)

    dicom_store_parent = f"projects/{project_id}/locations/{location}/datasets/{dataset_id}"
    dicom_store_name = f"{dicom_store_parent}/dicomStores/{dicom_store_id}"

    body = {"gcsSource": {"uri": f"gs://{content_uri}"}}

    request = (
        client.projects()
        .locations()
        .datasets()
        .dicomStores()
        .import_(name=dicom_store_name, body=body)
    )
    response = request.execute()
    print(f"Import request submitted for: {content_uri}")

    return response