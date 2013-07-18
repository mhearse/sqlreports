import sqlreports

rpt = sqlreports.sql({      \
    'ENGINE' : 'mysql',     \
    'HOST'   : 'localhost', \
    'USER'   : 'root',      \
    'NAME'   : 'matt',      \
})

results = rpt.runQuery('select id, name, age from example')

xls = sqlreports.spreadsheet(results)
xls.column_names = rpt.column_names
xls.createSpreadsheet()

pdf = sqlreports.pdf(results)
pdf.createPDF()

html = sqlreports.html(results)