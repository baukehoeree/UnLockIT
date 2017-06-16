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

    def getLocks(self, mail):
        # Query met parameters
        sqlQuery = "SELECT * FROM system as s, users as u,system_has_rfid as r WHERE u.IDUser=r.rfid_users_IDUser AND u.Email = '{email}'"
        # Combineren van de query en parameter
        sqlCommand = sqlQuery.format(email=mail)

        self.__cursor.execute(sqlCommand)
        result = self.__cursor.fetchall()
        self.__cursor.close()
        return result

    def getDataAccess(self, lockID):
        # Query met parameters
        sqlQuery = "SELECT * FROM access WHERE system_IDSystem = '{idlock}'"
        # Combineren van de query en parameter
        sqlCommand = sqlQuery.format(idlock=lockID)

        self.__cursor.execute(sqlCommand)
        result = self.__cursor.fetchall()
        self.__cursor.close()
        return result

    def getDataMotion(self, lockID):
        # Query met parameters
        sqlQuery = "SELECT * FROM motion WHERE system_IDSystem = '{idlock}'"
        # Combineren van de query en parameter
        sqlCommand = sqlQuery.format(idlock=lockID)

        self.__cursor.execute(sqlCommand)
        result = self.__cursor.fetchall()
        self.__cursor.close()
        return result

    def getDataAccessDay(self, lockID):
        # Query met parameters
        sqlQuery = "SELECT * FROM access WHERE DATE=CURDATE() AND system_IDSystem = '{idlock}'"
        # Combineren van de query en parameter
        sqlCommand = sqlQuery.format(idlock=lockID)

        self.__cursor.execute(sqlCommand)
        result = self.__cursor.fetchall()
        self.__cursor.close()
        return result

    def setLog(self, opened):
        # Query met parameters
        sqlQuery = "INSERT INTO access(Openned, Date, Time, system_IDSystem, categories_IDCategory) VALUES('{open}',curdate(), CURTIME(),1,1)"
        # Combineren van de query en parameter
        sqlCommand = sqlQuery.format(open=opened)
        self.__cursor.execute(sqlCommand)
        self.__connection.commit()
        self.__cursor.close()

    def setContact(self, name, phone, mail, message):
        # Query met parameters
        sqlQuery = "INSERT INTO contact(fullname, telephone, mail, message) VALUES('{name}','{phone}','{mail}','{message}')"
        # Combineren van de query en parameter
        sqlCommand = sqlQuery.format(name=name, phone=phone, mail=mail, message=message)
        self.__cursor.execute(sqlCommand)
        self.__connection.commit()
        self.__cursor.close()
