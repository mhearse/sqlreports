import xlwt

class spreadsheet:
    ##############################################
    def __init__(self, dataset):
    ##############################################
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
