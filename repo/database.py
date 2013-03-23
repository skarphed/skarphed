import fdb

class DatabaseException(Exception):
    pass

class DatabaseConnection(object):
    def __init__(self, ip, dbname, user, password):
        self.ip = ip
        self.dbname = dbname
        self.user = user
        self.password = password
        self.connection = None

    def connect(self):
        try:
            self.connection = fdb.connect(
                        host = self.ip,
                        database = '/var/lib/firebird/2.5/data/' + self.dbname,
                        user = self.user,
                        password = self.password)
        except fdb.fbcore.DatabaseError, e:
            raise DatabaseException(str(e))
        return

    def execute(self, statement, commit = False):
        if self.connection is None:
            raise DatabaseException("No Connection")
        cursor = self.connection.cursor()
        try:
            cursor.execute(statement)
            if commit:
                self.connection.commit()
            return cursor.fetchallmap()
        except fdb.fbcore.DatabaseError, e:
            raise DatabaseException(str(e))

