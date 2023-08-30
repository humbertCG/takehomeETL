#Author: Humberto Carrillo 
#Date 29/8/2023

import boto3 #This is the library for interacting with the simple queue service
from hashlib import sha256 #This library is used for masking sensible information
import json #This library is used for creating dictionaries from string and to execute other json related operations
from collections import Counter #import the counter data structure to compare the keys of the body of a message with the expected keys
import postgreFunctions as pgf #custom module for executing postgresSQL functions.

sqs_url = 'http://localhost:4566/000000000000/login-queue' #URL generated when running the docker compose command. In a production environment it would be recommended to access
#the URL using an environment variable but, since this app is run locally and not everyone has access to the sqs docker image that was used, no environment variables were used.


#Since the sqs is run on a docker file locally we can use 'dummy' credentials for testing the app however, it is a must to change this when deploying the app.
sqs_client = boto3.client(
        'sqs',
        endpoint_url = sqs_url,
        region_name = 'no-region-required-for-local-testing', 
        aws_access_key_id='no-credentials-for-local-testing', aws_secret_access_key='no-secret-access-key-for-local-testing', 
    )


#for detailed documentation on each function please check the stub sqsFunction.py


def get_approximate_number_of_messages() -> int:

    response = sqs_client.get_queue_attributes(
        QueueUrl = sqs_url,
        AttributeNames = ['ApproximateNumberOfMessages']
    )

    return int(response['Attributes']['ApproximateNumberOfMessages'])


def mask_sensible_info(info: str) -> str: 

    sha256_hash = sha256()

    sha256_hash.update(info.encode('utf-8'))

    hashed_info = sha256_hash.hexdigest()

    return hashed_info


def receive_messages() -> dict:

    response = sqs_client.receive_message(
        QueueUrl = sqs_url,
        MaxNumberOfMessages = 10
    )  


    return response['Messages']


def check_dictionary_keys(key_list: list) -> bool:

    expected_key_list = ['ip', 'device_type', 'app_version', 'user_id', 'locale', 'device_id']

    return Counter(key_list) == Counter(expected_key_list)


def format_app_version(version: str) -> str:

    version = version.replace('.', '')

    return version
        
        
        
def process_message_list(msg_list: list) -> list:

    for message in msg_list:

        body_dictionary = json.loads(message['Body']) #Convert the body to a dictionary because it is recovered as a string instead of dict
        
        body_dictionary_key_list = list(body_dictionary.keys())

        if check_dictionary_keys(body_dictionary_key_list):

            body_dictionary['app_version'] = format_app_version(body_dictionary['app_version'])

            masked_ip = mask_sensible_info(body_dictionary['ip'])
            body_dictionary.pop('ip')
            body_dictionary['masked_ip'] = masked_ip
            message['Body'] = body_dictionary

            masked_device_type = mask_sensible_info(body_dictionary['device_type'])
            body_dictionary.pop('device_id')
            body_dictionary['masked_device_id'] = masked_device_type
            message['Body'] = body_dictionary

        else:

            print('Found a message that does not contain either an ip address or a device_type it will not be inserted to the database')

            sqs_client.delete_message(QueueUrl = sqs_url, ReceiptHandle = message['ReceiptHandle']) #Delete useless message to avoid reading it again
            
            continue

        pgf.createTuple(body_dictionary)

        sqs_client.delete_message(QueueUrl = sqs_url, ReceiptHandle = message['ReceiptHandle']) #Delete processed message
