import sys
import MySQLdb

class sql:
    ##############################################
    def __init__(self, args=None):
    ##############################################
        # Allow args to be optional.
        args = {} if args is None else args

        defaults = {                           \
            'DATABASE_HOST'   : 'localhost',   \
            'DATABASE_USER'   : '',            \
            'DATABASE_PASSWD' : '',            \
            'DATABASE_NAME'   : '',            \
            'DATABASE_PORT'   : 3306,          \
        }

        # Apply defaults.
        for key in defaults.keys():
            setattr(self, key, defaults[key])
    
        # Apply arguments passed by human.
        # They will clobber our defaults.
        for key in args.keys():
            setattr(self, key, args[key])

        try:
            self.db = MySQLdb.connect(         \
                host   = self.DATABASE_HOST,   \
                user   = self.DATABASE_USER,   \
                passwd = self.DATABASE_PASSWD, \
                db     = self.DATABASE_NAME,   \
                port   = self.DATABASE_PORT    \
            )
        except MySQLdb.Error, e:
            sys.stderr.write('[ERROR] %d: %s\n' % (e.args[0], e.args[1]))
            sys.exit(1)

        self.cursor = self.db.cursor()

    ##############################################
    def runQuery(self, sql):
    ##############################################
        # Execute query and load results into 2d list.
        try:
            self.sqloutput = []
            self.cursor.execute(sql)
            numrows = self.cursor.rowcount
            for i in range(0,numrows):
                row = self.cursor.fetchone()
                self.sqloutput.append(row)
        except MySQLdb.Error, e:
            sys.stderr.write('[ERROR] %d: %s\n' % (e.args[0], e.args[1]))

        return self.sqloutput
