import pyodbc


def read(conn):
    cursor = conn.cursor()
    cursor.execute("select * from Services")
    for row in cursor:
        print(row)


def write(conn):
    cursor = conn.cursor()
    cursor.execute(
        "insert into Services(Service, Password) values(?,?);", ("Facebook", "1234456")
    )
    conn.commit()

def connect():
    Driver = "ODBC Driver 17 for SQL Server"
    Server = r"DESKTOP-QJJ4U09\SQLEXPRESS"
    Database = "PassMng"

    try:
        conn = pyodbc.connect(
            "DRIVER="
            + Driver
            + ";SERVER="
            + Server
            + ";DATABASE="
            + Database
            + ";TRUSTED_CONNECTION=YES;"
        )

        print("Success! Connected to " + Database + " database.")
        return conn
    except Exception as error:
        print("Connection failed..\n")
        print(error)

