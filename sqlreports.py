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
            'ENGINE' : '',          \
            'HOST'   : 'localhost', \
            'USER'   : '',          \
            'PASSWD' : '',          \
            'NAME'   : '',          \
            'PORT'   : 3306,        \
            'SID'    : '',          \
        }

        # Apply defaults.
        for key in defaults.keys():
            setattr(self, key, defaults[key])
    
        # Apply arguments passed by human.
        # They will clobber our defaults.
        for key in args.keys():
            setattr(self, key, args[key])

        if self.ENGINE == 'mysql':
            self.connectMySQL()
        else:
            sys.stderr.write('No known database engine defined\n')
            sys.exit(1)

    ##############################################
    def connectMySQL(self):
    ##############################################
        try:
            import MySQLdb
            global MySQLdb
        except ImportError, err:
            print "Error Importing module. %s" % (err)
            exit(2)
        try:
            self.db = MySQLdb.connect( \
                host   = self.HOST,    \
                user   = self.USER,    \
                passwd = self.PASSWD,  \
                db     = self.NAME,    \
                port   = self.PORT     \
            )
        except MySQLdb.Error, e:
            sys.stderr.write('[SQL ERROR] %d: %s\n' % (e.args[0], e.args[1]))
            sys.exit(3)

        self.cursor = self.db.cursor()

    ##############################################
    def runQuery(self, sql):
    ##############################################
        # Execute query and load results into 2d list.
        try:
            self.cursor.execute(sql)
        except MySQLdb.Error, e:
            sys.stderr.write('[SQL ERROR] %d: %s\n' % (e.args[0], e.args[1]))
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
        try:
            import xlwt
            global xlwt
        except ImportError, err:
            print "Error Importing module. %s" % (err)
            exit(5)
        self.dataset = dataset

    ##############################################
    def createSpreadsheet(self):
    ##############################################
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
    def __init__(self, dataset):
    ##############################################
        try:
            import reportlab
            global reportlab
        except ImportError, err:
            print "Error Importing module. %s" % (err)
            exit(6)

class html:
    ##############################################
    def __init__(self, dataset):
    ##############################################
        try:
            from Cheetah.Template import Template
            global Template
        except ImportError, err:
            print "Error Importing module. %s" % (err)
            exit(7)
