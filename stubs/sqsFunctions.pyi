#Author: Humberto Carrillo 
#Date 29/8/2023

def get_approximate_number_of_messages() -> int:
    """Queries the SQS for determining how many messages are left on the queue."""
    ...


def mask_sensible_info(info: str) -> str: 

    """Receives a string that contains sensible info (PII) and masks it using the SHA256 algorithm, it encodes the provided info using UTF-8 because sha256 works with bytes not with 
     plain text and then it returns the Hexadecimal representation of the generated hash."""
    

    ...

def receive_messages() -> dict:

    """Retrieves 10 messages from the queue and partially flattens the JSON file by removing the outer 'messages' wrapper"""

    ...

def check_dictionary_keys(key_list: list) -> bool:

    """This is a helper function that allows the program to discard messages that are missing information.
    It Compares the expected key list (The information that every message should contain) with the actual key list and returns true if the key lists match and false otherwise"""
    ...

def format_app_version(version: str) -> str:

    """Helper funciton that removes the periods from the app_version (turns 0.2.3 into 23); this might seem a little bit odd and confusing but it was done to comply with 
    the schema of the database which only accepts integers for the app_version. The way of reading the version(hoping that version 10 never arrives because
    it will make things more complex), without periods would be: the leftmost number is the major version, the number in the middle the minor version and the rightmost 
    number is the patch version. e.g. If we have a major version of 0, a minor version of 2 and a patch number of 3, it would be displayed as 23 in the app_version field of the 
    database""" 
    ...

def process_message_list(msg_list: list) -> None:

    """This is the main, orchestrating function. All the other helper functions mentioned in this file are invoked here. 
    It retrieves the body of the message and then converts it into a dictionary using the json library then, if the keys of the message match the expected keys,
    it modifies the content of the app_version, and masks the PII (device_id, ip_address), it then inserts the new message body into the database and finally erases
    the processed message from the queue. If the message's keys did not match with the expected keys it notifies the user, and deletes it without inserting it to the db"""

