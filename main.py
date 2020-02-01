import conn, crypt, interface
from os import urandom
from sys import exit
from msvcrt import getch
from getpass import getpass


def set_password(pw):
    salt = urandom(16)
    secret = crypt.derive_pbkdf2hmac(str.encode(pw), salt)

    cursor.execute("Delete from Secret_Hash;")
    cursor.execute(
        "insert into Secret_Hash(Secret, Salt) values(?,?);",
        (crypt.func_sha256(secret), salt),
    )

    cursor.commit()


def verify_pw(pw):
    cursor.execute("Select * from Secret_Hash;")

    for db_secret_hash in cursor:
        (sec_hash, salt) = db_secret_hash
        secret = crypt.derive_pbkdf2hmac(pw, salt)
        return sec_hash == crypt.func_sha256(secret)

def store_pw(service, new_pw, key, pw):
    cursor.execute(
        "Select * from Services where Services=?",
        service
    )

    if(cursor.rowcount == 0):
        (enc_pw, nonce) = crypt.enc_aesgcm(key, str.encode(new_pw), pw)

        cursor.execute(
            "Insert into Services(Services, Password, Nonce) values(?,?,?)",
            (service, enc_pw, nonce)
        )
        cursor.commit()
        print("Service successfully stored!")
    else:
        print(">> Service already exists!")

def retrieve_pw(service, key, pw):
    cursor.execute(
        "Select * from Services where Services=?",
        service
    )

    if(cursor.rowcount != 0):
        for row in cursor:
            nonce = row[2]
            ct = row[1]
            password = crypt.dec_aesgcm(key, pw, nonce, ct).decode("utf-8")
            print(
                ">> Stored password for service " 
                + service 
                + ": "
                + password
                + '\n'
            )
            print("Click any key to continue..")
            getch()
            
    else:
        print(">> Service does not exist")
    
def change_pw(service, key, pw, new_pw):
    cursor.execute(
        "Select * from Services where Services=?",
        service
    )

    if(cursor.rowcount != 0):
        (enc_pw, nonce) = crypt.enc_aesgcm(key, str.encode(new_pw), pw)

        cursor.execute('''
            Update Services
            Set Password=?, Nonce=?
            Where Services=?''',
            (enc_pw, nonce, service))
        cursor.commit()
        print("Password for Service " + service + " successfully changed!")
    else:
        print(">> Service does not exist")


def handler(msg, pw, key):
    try:
        if msg == b"1":
            new_pw = interface.secret_interface()
            set_password(new_pw)
        elif msg == b"2":
            (service, password) = interface.store_interface()
            store_pw(service, password, key, pw)
        elif msg == b"3":
            service = interface.retrieve_interface()
            retrieve_pw(service, key, pw)
        elif msg == b"4":
            (service, new_pw) = interface.change_interface()
            change_pw(service, key, pw, new_pw)
    except:
        print('Fatal Error! Ending connection.')
        quit()


def main(pw, key):
    for new_input in iter(lambda: getch(), b"q"):
        try:
            if int(new_input) in range(1, 5):
                handler(new_input, pw, key)
                interface.main_interface()
        except:
            pass


if __name__ == "__main__":
    conn = conn.connect()
    cursor = conn.cursor()

    cursor.execute(
        """
    select * from Secret_Hash;
    """
    )

    if cursor.rowcount == 0:
        print(">> You need to setup a password.")
        set_password(getpass())

    print(">> Please input Password Manager secret password")
    password = str.encode(getpass())

    if verify_pw(password):
        interface.main_interface()

        cursor.execute(
            "select Salt from Secret_Hash"
        )

        try:
            for row in cursor:
                salt = row[0]
                secret = crypt.derive_pbkdf2hmac(password, salt)
                main(password, secret)
        except:
            pass
    else:
        print("Wrong password! Ending connection.")
    cursor.close()
    conn.close()
