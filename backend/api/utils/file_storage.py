from google.cloud import storage
import os

GCS_BUCKET_NAME = "ccodel_tickets"  # Change this to your actual bucket name

def upload_to_gcs(file, ticket_id: str, expiration=3600):
    """Uploads a file to Google Cloud Storage and returns a signed URL (valid for 1 hour)."""
    client = storage.Client()
    bucket = client.bucket(GCS_BUCKET_NAME)
    blob = bucket.blob(f"tickets/{ticket_id}/{file.filename}")
    
    blob.upload_from_file(file.file, content_type=file.content_type)

    # Generate signed URL for private access
    signed_url = blob.generate_signed_url(expiration=expiration)

    return signed_url
