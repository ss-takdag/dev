#!/usr/bin/env python3
import boto3
import csv
import datetime
import secrets
import logging
import json
import os
#
import secret_manager
import athena_from_s3
import email_handler
import google_sheets_handler
import s3_handler
import sns_handler

logger = logging.getLogger()
logger.setLevel(logging.INFO)
bucket_name = os.environ['DESTINATION_BUCKET']
bucket_path = os.environ['BUCKET_PATH']
database_name = os.environ['ATHENA_DATABASE']
aws_region = os.environ['AWS_REGION']
random_hash = secrets.token_hex(nbytes=5)
timestamp = datetime.date.today()
sheet_name = "rfs3_athena_soc2_report_{}".format(timestamp)

def handler(event, context):
    #ATHENA QUERY (reads query.txt)
    query_file = open("query.txt", "r")
    all_lines_formatted = query_file.read()
    query_file.close()
    #print(all_lines_formatted)
    # params = {
    #     'region': aws_region,
    #     'database': database_name,
    #     'bucket': bucket_name,
    #     'path': bucket_path,
    #     'query': all_lines_formatted
    # }


    #SAMPLE QUERY
    params = {
        'region': aws_region,
        'database': database_name,
        'bucket': bucket_name,
        'path': bucket_path,
        'query': 'SELECT * FROM "default"."test" limit 10;'
    }

    #RUN ATHENA QUERY
    # ## Fucntion for obtaining query results and location
    logger.info('running query on amazon athena')
    location, data = athena_from_s3.query_results(params)
    key = location.rsplit('/', 1)
    key = key[1]
#    print(key)
    file_key = "{}/{}".format(bucket_path, key)

    #LOAD SECRETS
    json_creds = secret_manager.get_secret()
    json_creds = json.loads(json_creds)

    #SCRAPE CONTENTS OF QUERY RESULTS FROM S3
    logger.info('scraping s3')
    scan_output_contents = s3_handler.read_scan_output(bucket_name, file_key)

    # # # # #CREATE AND UPDATE GOOGLE SHEETS
    logger.info('Creating new daily google sheet report')
    google_sheets_handler.create_new_report(json_creds, sheet_name, scan_output_contents)
    #
    logger.info('Updating accumlative google sheet report')
    google_sheets_handler.update_existing_report(json_creds, scan_output_contents)

    # #SEND EMAIL NOTIFICATION TO ZENDENSK
#    logger.info('Sending SES Email')
    email_handler.send_notification_email(location, data)
