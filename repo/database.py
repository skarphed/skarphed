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


    def disconnect(self):
        if self.connection:
            self.connection.close()


    def query(self, statement, commit = False):
        if self.connection is None:
            raise DatabaseException('No Connection')
        cursor = self.connection.cursor()
        try:
            cursor.execute(statement)
            result = cursor.fetchallmap()
            if commit:
                self.connection.commit()
            cursor.close()
            return result
        except fdb.fbcore.DatabaseError, e:
            raise DatabaseException(str(e))


    def update(self, statement):
        if self.connection is None:
            raise DatabaseException('No Connection')
        cursor = self.connection.cursor()
        try:
            cursor.execute(statement)
            self.connection.commit()
            cursor.close()
        except fdb.fbcore.DatabaseError, e:
            raise DatabaseException(str(e))



    def get_sequence_next(self, sequence):
        result = self.query('SELECT NEXT VALUE FOR %s FROM RDB$DATABASE;' % sequence, commit = True)
        if result:
            return result[0]['gen_id']
        else:
            raise DatabaseException('No generator: %s' % sequence)
