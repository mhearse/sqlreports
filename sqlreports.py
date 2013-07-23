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

        # Sanitize args.
        tmpdict = {}
        for key in args.keys():
            if key.upper() == 'ENGINE':
                tmpdict[key.upper()] = args[key].lower()
            else:
                tmpdict[key.upper()] = args[key]
        args = tmpdict

        # Default db server ports.
        ports = {                             \
            'mysql'      : 3306,              \
            'postgresql' : 5432,              \
            'oracle'     : 1521,              \
        }

        # Supported engine is required.
        if not ports.get(args.get('ENGINE')):
            sys.stderr.write('No known database engine defined\n')
            sys.exit(1)

        defaults = {                          \
            'ENGINE' : '',                    \
            'HOST'   : 'localhost',           \
            'USER'   : '',                    \
            'PASSWD' : '',                    \
            'NAME'   : '',                    \
            'PORT'   : ports[args['ENGINE']], \
            'SID'    : '',                    \
        }

        # Apply defaults.
        for key in defaults.keys():
            setattr(self, key, defaults[key])
    
        # Apply arguments passed by human.
        # They will clobber our defaults.
        for key in args.keys():
            setattr(self, key, args[key])

        # Attempt database connection.
        if self.ENGINE == 'mysql':
            self.connectMySQL()
        elif self.ENGINE == 'postgresql':
            self.connectPostgreSQL()
        elif self.ENGINE == 'oracle':
            self.connectOracle()

    ##############################################
    def connectMySQL(self):
    ##############################################
        try:
            import MySQLdb
            global MySQLdb
        except ImportError, err:
            print "Error Importing module. %s" % (err)
            sys.exit(2)

        try:
            self.db = MySQLdb.connect( \
                host   = self.HOST,    \
                user   = self.USER,    \
                passwd = self.PASSWD,  \
                db     = self.NAME,    \
                port   = self.PORT,    \
            )
        except MySQLdb.Error, e:
            sys.stderr.write('[SQL ERROR] %d: %s\n' % (e.args[0], e.args[1]))
            sys.exit(3)

        self.cursor = self.db.cursor()

    ##############################################
    def connectPostgreSQL(self):
    ##############################################
        try:
            import psycopg2
            global psycopg2
        except ImportError, err:
            print "Error Importing module. %s" % (err)
            sys.exit(4)

        try:
            dsn = "host='%s' port='%d' dbname='%s' user='%s' password='%s'" % (\
                self.HOST,    \
                self.PORT,    \
                self.NAME,    \
                self.USER,    \
                self.PASSWD,  \
            )
            self.db = psycopg2.connect(dsn)
        except psycopg2.Error, e:
            sys.stderr.write('[SQL ERROR] %d: %s\n' % (e.args[0], e.args[1]))
            sys.exit(5)
    
        self.cursor = self.db.cursor()

    ##############################################
    def connectOracle(self):
    ##############################################
        try:
            import cx_Oracle
            global cx_Oracle
        except ImportError, err:
            print "Error Importing module. %s" % (err)
            sys.exit(6)

        try:
            dsn = cx_Oracle.makedsn(     \
                self.HOST,               \
                self.PORT,               \
                self.SID,                \
            )

            self.db = cx_Oracle.connect( \
                self.USER,               \
                self.PASSWD,             \
                dsn,                     \
            )
        except cx_Oracle.DatabaseError, e:
            error, = e.args
            if error.code == 1017:
                sys.stderr.write('Please check your credentials.\n')
            else:
                sys.stderr.write('Database connection error: %s\n'.format(e))
            sys.exit(7)

        self.cursor = self.db.cursor()

    ##############################################
    def runQuery(self, sql):
    ##############################################
        # Execute query and load results into 2d list.
        try:
            self.cursor.execute(sql)
        except:
            sys.stderr.write('Error executing SQL query.\n')
            sys.exit(8)

        numrows = self.cursor.rowcount
        self.sqloutput = []
        for i in range(0,numrows):
            row = self.cursor.fetchone()
            self.sqloutput.append(row)

        # Get column names/aliases.
        self.column_names = []
        for i in self.cursor.description:
            try:
                self.column_names.append(i[0])
            except:
                continue

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
            sys.exit(9)
        self.dataset = dataset
        self.column_names = []

    ##############################################
    def createSpreadsheet(self):
    ##############################################
        book = xlwt.Workbook()
        sheet = book.add_sheet('test')
        rowx = 0

        # Apply optional headers.
        if self.column_names:
            heading_xf = xlwt.easyxf('font: bold on; align: wrap on, vert centre, horiz center')
            for colx, value in enumerate(self.column_names):
                sheet.write(rowx, colx, value, heading_xf)
            rowx += 1

        for row in self.dataset:
            for colx, value in enumerate(row):
                sheet.write(rowx, colx, value)
            rowx += 1
        book.save('/tmp/my.xls')

class pdf:
    ##############################################
    def __init__(self, dataset):
    ##############################################
        try:
            from reportlab.pdfgen import canvas
            from reportlab.lib.pagesizes import A4, cm
            from reportlab.lib.styles import getSampleStyleSheet
            from reportlab.platypus import Paragraph, Table, TableStyle
            from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER
            from reportlab.lib import colors
            global                   \
                canvas,              \
                A4,                  \
                cm,                  \
                getSampleStyleSheet, \
                Paragraph,           \
                Table,               \
                TableStyle,          \
                TA_JUSTIFY,          \
                TA_LEFT,             \
                TA_CENTER,           \
                colors
        except ImportError, err:
            print "Error Importing module. %s" % (err)
            sys.exit(10)
        self.dataset = dataset
        self.column_names = []

    ##############################################
    def createPDF(self):
    ##############################################
        width, height = A4
        styles = getSampleStyleSheet()
        styleN = styles["BodyText"]
        styleN.alignment = TA_LEFT
        styleBH = styles["Normal"]
        styleBH.alignment = TA_CENTER
        
        def coord(x, y, unit=1):
            x, y = x * unit, height -  y * unit
            return x, y
        
        # Headers

        # Apply optional headers.
        if self.column_names:
            headers = []
            for value in self.column_names:
                headers.append(Paragraph('<b>%s</b>' % str(value), styleBH))
            self.dataset.insert(0, headers)

        table = Table(     \
            self.dataset,  \
            colWidths = [  \
                2.05 * cm, \
                2.7  * cm, \
                5    * cm, \
                3    * cm, \
                3    * cm  \
            ]              \
        )
        
        table.setStyle(                                            \
            TableStyle([                                           \
                ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black), \
                ('BOX', (0,0), (-1,-1), 0.25, colors.black),       \
            ])                                                     \
        )
        
        c = canvas.Canvas("a.pdf", pagesize=A4)
        table.wrapOn(c, width, height)
        table.drawOn(c, *coord(1.8, 9.6, cm))
        c.save()

class html:
    ##############################################
    def __init__(self, dataset):
    ##############################################
        self.dataset = dataset
        self.column_names = []

    ##############################################
    def createHTML(self):
    ##############################################
        header = '<HTML><HEAD></HEAD><BODY><TABLE>'
        footer = '</TABLE></BODY></HTML>'
        output = ''
        for row in self.dataset:
            cell = ''
            for col in row:
                cell += str('<TD>%s</TD>' % col)
            output += str('<TR>%s</TR>' % cell)

        return "%s%s%s" % (header, output, footer)
