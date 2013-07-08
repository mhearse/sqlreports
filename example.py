import sqlreports

rpt = sqlreports.sql({      \
    'ENGINE' : 'mysql',     \
    'HOST'   : 'localhost', \
    'USER'   : 'root',      \
    'PASSWD' : '',          \
    'NAME'   : 'matt',      \
    'PORT'   : 3306,        \
})

results = rpt.runQuery('select * from example')
xls = sqlreports.spreadsheet(results)
xls.createSpreadsheet()

html = sqlreports.html(results)

pdf = sqlreports.pdf(results)
