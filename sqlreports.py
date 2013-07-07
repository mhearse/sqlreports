#!/usr/bin/env python

"""

Release under the terms of the GPL licence
You can get a copy of the license at http://www.gnu.org

Description: SQL to html, xls, graph and pdf

Written by: Matt Hersant (matt_hersant[at]yahoo[dot]com)

"""

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
            sys.exit(2)

    ##############################################
    def connectMySQL(self):
    ##############################################
        try:
            import MySQLdb
            global MySQLdb
        except ImportError, err:
            print "Error Importing module. %s" % (err)
            exit(1)
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
            sys.exit(3)

        self.cursor = self.db.cursor()

    ##############################################
    def runQuery(self, sql):
    ##############################################
        # Execute query and load results into 2d list.
        try:
            self.cursor.execute(sql)
        except MySQLdb.Error, e:
            sys.stderr.write('[ERROR] %d: %s\n' % (e.args[0], e.args[1]))
            sys.exit(4)

        numrows = self.cursor.rowcount
        self.sqloutput = []
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
        try:
            import xlwt
            global xlwt
        except ImportError, err:
            print "Error Importing module. %s" % (err)
            exit(1)
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
        try:
            import reportlab
            global reportlab
        except ImportError, err:
            print "Error Importing module. %s" % (err)
            exit(1)
