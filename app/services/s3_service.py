import boto3
from uuid import uuid4

s3 = boto3.client(
    "s3",
    aws_access_key_id="",
    aws_secret_access_key="",
    region_name="us-east-1"
)

BUCKET_NAME = "healthcare-claim-documents-dev"


def upload_claim_document(file):

    file_key = f"claims/{uuid4()}_{file.filename}"

    s3.upload_fileobj(
        file.file,
        BUCKET_NAME,
        file_key
    )

    return file_key
