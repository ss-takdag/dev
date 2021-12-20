#!/usr/bin/env python3
import boto3
s3 = boto3.client('s3')
def read_scan_output(bucket, key):
    # These define the bucket and object to read
    bucketname = bucket
    file_to_read = key
    #Create a file object using the bucket and object key.
    fileobj = s3.get_object(
        Bucket=bucketname,
        Key=file_to_read
        )
        # open the file object and read it into the variable filedata.
    filedata = fileobj['Body'].read()
    s3_data = filedata.decode('utf-8')
    return s3_data
