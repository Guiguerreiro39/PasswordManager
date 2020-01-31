import conn, crypt, interface
from os import urandom
from sys import exit
from msvcrt import getch
from getpass import getpass


def set_password(pw):
    cursor = conn.cursor()
    salt = urandom(16)
    secret = crypt.derive_pbkdf2hmac(str.encode(pw), salt)

    cursor.execute("Delete from Secret_Hash;")
    cursor.execute(
        "insert into Secret_Hash(Secret, Salt) values(?,?);",
        (crypt.func_sha256(secret), salt),
    )

    cursor.commit()
    cursor.close()


def verify_pw(pw):
    cursor = conn.cursor()
    cursor.execute("Select * from Secret_Hash;")

    for db_secret_hash in cursor:
        (sec_hash, salt) = db_secret_hash
        secret = crypt.derive_pbkdf2hmac(pw, salt)
        return sec_hash == crypt.func_sha256(secret)


def handler(msg):
    if msg == b"1":
        new_pw = interface.secret_interface()
        set_password(new_pw)
    elif msg == b"2":
        (service, password) = interface.store_interface()
        print(service, password)
    elif msg == b"3":
        service = interface.retrieve_interface()
        print(service)
    elif msg == b"4":
        service = interface.change_interface()


def main():
    for new_input in iter(lambda: getch(), b"q"):
        try:
            if int(new_input) in range(1, 4):
                handler(new_input)
                interface.main_interface()
        except:
            pass


if __name__ == "__main__":
    conn = conn.connect()
    cursor_main = conn.cursor()

    cursor_main.execute(
        """
    select * from Secret_Hash;
    """
    )

    if cursor_main.rowcount == 0:
        print(">> You need to setup a password.")
        set_password(getpass())

    print(">> Please input Password Manager secret password")
    password = getpass()

    if verify_pw(str.encode(password)):
        interface.main_interface()
        main()
    else:
        print("Wrong password! Ending connection.")
    cursor_main.close()
    conn.close()
