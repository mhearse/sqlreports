import sys

class sql:
    ##############################################
    def __init__(self, args=None):
    ##############################################
        # Allow args to be optional.
        args = {} if args is None else args

        defaults = {                           \
            'DATABASE_ENGINE' : '',            \
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

        if self.DATABASE_ENGINE == 'mysql':
            self.connectMySQL()
        else:
            sys.stderr.write('No known database engine defined\n')
            sys.exit(1)

    ##############################################
    def connectMySQL(self):
    ##############################################
        import MySQLdb
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
            sys.exit(2)

        self.cursor = self.db.cursor()

    ##############################################
    def runQuery(self, sql):
    ##############################################
        # Execute query and load results into 2d list.
        self.sqloutput = []
        self.cursor.execute(sql)
        numrows = self.cursor.rowcount
        for i in range(0,numrows):
            row = self.cursor.fetchone()
            self.sqloutput.append(row)

        return self.sqloutput

class spreadsheet:
    ##############################################
    def __init__(self, dataset):
    ##############################################
        self.dataset = dataset

    ##############################################
    def createSpreadsheet(self):
    ##############################################
        import xlwt
        book = xlwt.Workbook()
        sheet = book.add_sheet('test')
        rowx = 0
        for row in self.dataset:
            rowx += 1
            for colx, value in enumerate(row):
                sheet.write(rowx, colx, value)
        book.save('/tmp/my.xls')

class pdf:
    ##############################################
    def __init__(self):
    ##############################################
        import reportlab
