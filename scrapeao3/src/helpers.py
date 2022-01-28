from botocore.client import ClientError
import os
from dotenv import dotenv_values

# HELPER FUNCTIONS
def most_common(lst):
    return max(set(lst), key=lst.count)

def flatten_list(x):
    result = []
    for el in x:
        if hasattr(el, "__iter__") and not isinstance(el, str):
            result.extend(flatten_list(el))
        else:
            result.append(el)
    return result

def _s3_file_exists(client, bucket, file_key):
    file_key = f"{file_key.strip('/')}"
    file_found = False
    try:
        client.head_object(Bucket=bucket, Key=file_key)
        file_found = True
    except ClientError as exc:
        if exc.response['Error']['Code'] != '404':
            raise
    return file_found

def set_aws_creds():
    if os.path.exists('.env'):
        config = dotenv_values(".env")
        for k, v in config.items():
            os.environ[k] = v
