import conn, crypt, interface
from sys import exit
from msvcrt import getch

def handler(msg):
    if(msg == b'1'):
        new_pw = interface.secret_interface()
        print(new_pw)
    elif(msg == b'2'):
        (service, password) = interface.store_interface()
        print(service, password)
    elif(msg == b'3'):
        service = interface.retrieve_interface()
        print(service)
    elif(msg == b'4'):
        service = interface.change_interface()
    main()

def main():
    interface.main_interface()
    while True:
        new_input = getch()
        try:
            if(int(new_input) in range(1, 4)):
                break
        except:
            if(new_input == b'q'):
                exit()
    handler(new_input)

if __name__ == "__main__":
    main()