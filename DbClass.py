class DbClass:
    def __init__(self):
        import mysql.connector as connector

        self.__dsn = {
            "host": "localhost",
            "user": "baukeremote",
            "passwd": "remote",
            "db": "dbUnLockIT"
        }

        self.__connection = connector.connect(**self.__dsn)
        self.__cursor = self.__connection.cursor()

    def getUser(self, mail):
        # Query met parameters
        sqlQuery = "SELECT * FROM users WHERE Email = '{email}'"
        # Combineren van de query en parameter
        sqlCommand = sqlQuery.format(email=mail)

        self.__cursor.execute(sqlCommand)
        result = self.__cursor.fetchall()
        self.__cursor.close()
        return result

    def setNewUser(self, fName, lName, mail, Password):
        # Query met parameters
        sqlQuery = "INSERT INTO users (FirstName,Name,Email,Password) VALUES ('{fname}','{lname}','{mail}','{passw}')"
        # Combineren van de query en parameter
        sqlCommand = sqlQuery.format(fname=fName, lname=lName, mail=mail, passw=Password)

        self.__cursor.execute(sqlCommand)
        self.__connection.commit()
        self.__cursor.close()
