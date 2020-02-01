from getpass import getpass


def main_interface():
    print(
        """ 
>>>>> Password Manager <<<<<
============================
1. Change Manager Secret
----------------------------
2. Store new Service Password
----------------------------
3. Retrieve Service Password
----------------------------
4. Change Service Password
============================
    """
    )


def change_interface():
    print(
        """
>>>>> Change Service Password <<<<<
===================================
__________ Enter Service __________
    """
    )
    service = input()

    print(
        """
____Enter new Service Password ____
    """
    )
    password = getpass()
    return (service, password)


def retrieve_interface():
    print(
        """
>>>>> Retrieve Service Password <<<<<
=====================================
___________ Enter Service ___________
    \n"""
    )
    return input()


def secret_interface():
    print(
        """
>>>>> Change Manager Secret <<<<<
=================================
______ Enter new password ______
    """
    )
    return getpass()


def store_interface():
    print(
        """
>>>>> Store new Service Password <<<<<
======================================
_________ Enter new Service _________
    """
    )
    service = input()

    print(
        """
________Enter Service Password _______
    """
    )
    password = getpass()

    return (service, password)
