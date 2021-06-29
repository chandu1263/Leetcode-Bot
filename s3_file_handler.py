import os
import boto3

from secret import *

class S3_file_handler:

    def __init__(self):
        """
            Creating a client connection to s3 bucket
        """
        self.client_s3 = boto3.client(
            's3',
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_access_key
        )

    def upload_file(self, filepath, filename):
        """
            Upload file to S3
            filepath - location of the file to be uploaded
            filename - key
        """
        result = {}
        try:
            self.client_s3.upload_file(
                filepath,
                s3_bucket_name,
                filename
            )
            result["status"] = "success"
            return result
        except Exception as e:
            result["status"] = "failure"
            result["reason"] = e
            return result

    def download_file(self, filename, filepath):
        """
            Download file from s3
            key : filename
            filepath : file saving location
        """
        result = {}
        try:
            self.client_s3.download_file(s3_bucket_name, filename, filepath)
            result["status"] = "success"
            return result
        except Exception as e:
            result["status"] = "failure"
            result["reason"] = e
            return result

