import boto3

textract_client = boto3.client(
    "textract",
    region_name="us-east-1"
)


def extract_text_from_s3(
    bucket_name: str,
    file_key: str
):

    response = textract_client.detect_document_text(
        Document={
            "S3Object": {
                "Bucket": bucket_name,
                "Name": file_key
            }
        }
    )

    extracted_text = []

    for block in response["Blocks"]:

        if block["BlockType"] == "LINE":

            extracted_text.append(
                block["Text"]
            )

    return "\n".join(extracted_text)