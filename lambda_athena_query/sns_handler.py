#!/usr/bin/env python3
import boto3

sns = boto3.client('sns')
def pubSNS(arn, message, subject):
    sns.publish(TopicArn=arn,
            Message=message,
            Subject=subject)
