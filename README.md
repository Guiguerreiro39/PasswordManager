# PasswordManager

## A Python program that helps people remember their passwords by storing them in a database. The passwords are heavily encrypted and is only possible to retrieve them by having the right secret, selected in the beggining as a form of password.

### Encryption schemes
This program uses several encryption algorithms to ensure the safety of the stored passwords.
- **PBKDF2HMAC**: In the beginning, for a person to access the manager, one must input a password. To use this password as the key of the encryption algorithm would affect the safety of the system since it is not big enough nor random enough. In order to deal with this issue, the key derivation function PBKDF2HMAC is used. This will take the password previously typed into consideration and create a much stronger and bigger key in order to be used in the encryption.
- **SHA256 HASH**: The main secret is stored as an hash that is then compared to the password that is typed in the beginning. The hash will authenticate the password and ensure that it remains a secret.
- **AES-GCM**: In order to safely store the passwords of each service, one must encrypt then and also ensure its integrity, meaning there were not changed. For this purpose the authentication encryption algorithm AES-GCM is used. This will not only heavily encrypt your passwords but also verify that it was not manipulated by an attacker.

### Files
- **conn.py**: This file will allow the program to connect to the database. In order to use your own database, some configurations must be changed.
- **crypt.py**: The encryption algorithm as well as the functions to use them are created in this file.
- **interface.py**: This program does not use any GUI for its interface. Instead it uses a command prompt based interface created using prints into the screen. This file manages all the available interfaces.
- **main.py**: The main file of the program that handles all the configurations of the system. It uses all the functions of the files above to structure the entire program.

### This program was created for personal use so it might have several flaws in its construction so please take that into consideration.


