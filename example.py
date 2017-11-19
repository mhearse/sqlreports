#!/usr/bin/env python

import sqlreports

rpt = sqlreports.sql({
    'ENGINE'   : 'sqlite',
    'HOST'     : 'localhost',
    'NAME'     : 'matt.db',
})

results = rpt.runQuery('select name, age from example')

# multi workbook spreadsheets will be represented as a 3 deminsional array
# workbook1, workbook2
xls = sqlreports.spreadsheet(results)
xls.column_names = rpt.column_names
xls.createSpreadsheet()

html = sqlreports.html(results)
html.column_names = rpt.column_names
zork = html.createHTML()

pdf = sqlreports.pdf(results)
pdf.column_names = rpt.column_names
pdf.createPDF()
