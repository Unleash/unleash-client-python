import mimesis
from random import getrandbits
from ipaddress import IPv4Address, IPv6Address

def generate_context():
    return {"userId": mimesis.Person('en').email()}


def generate_email_list(num: int) -> (str, dict):
    """
    Generates an unleash-style list of emails for testing.

    :param num:
    :return:
    """
    first_email = mimesis.Person('en').email()
    email_list_string = first_email

    context = {"userId": first_email}

    for _ in range(num - 1):
        email_list_string += "," + mimesis.Person('en').email()

    return (email_list_string, context)
