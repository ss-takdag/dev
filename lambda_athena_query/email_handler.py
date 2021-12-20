#!/usr/bin/env python3
from __future__ import print_function
import boto3
import logging
import time
import os
from botocore.exceptions import ClientError
import botocore
import datetime
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def send_notification_email(location, result_data):

    SENDER = os.environ['EMAIL_FROM_ADDRESS']
    RECIPIENT = os.environ['EMAIL_RECIPIENTS']
    # Specify a configuration set. If you do not want to use a configuration
    # set, comment the following variable, and the
    # ConfigurationSetName=CONFIGURATION_SET argument below.
    #CONFIGURATION_SET = "ConfigSet"
    AWS_REGION = os.environ['AWS_REGION']
    SUBJECT = "Daily Report "
    BODY_TEXT = location

    # The HTML body of the email.

    BODY_HTML = location
    #BODY_HTML = location
    # BODY_HTML = """<html>
    # <head></head>
    # <body>
    #   <h1>Daily Report </h1>
    #   <p>The location for the file is
    #     <a href='{}''>Download Link</a></p>
    # </body>
    # </html>
    #             """.format(location)

    # The character encoding for the email.
    CHARSET = "UTF-8"
    # Create a new SES resource and specify a region.
    client = boto3.client('ses',region_name=AWS_REGION)
    # Try to send the email.
    try:
        #Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
            # If you are not using a configuration set, comment or delete the
            # following line
            #ConfigurationSetName=CONFIGURATION_SET,
        )
    # Display an error if something goes wrong.
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])
