import csv
import numpy as np


class CsvReader:

    def __init__(self):

        # Read txt file as list.
        csvList = list()
        with open('data/KNMI.txt', newline='') as inputfile:
            reader = csv.reader(inputfile)
            for row in reader:
                if row[0][0] == '#':
                    continue
                else:
                    csvList.append(row)

        self.csvArray = np.asarray(csvList)

        # Remove the days of the first year if it is not complete.
        yearToDelete = None
        for index, row in enumerate(self.csvArray):

            year = int(row[1][:4])
            if index == 0 and row[1][4:8] != '0101':
                yearToDelete = year
                continue

            if year == yearToDelete + 1:
                self.csvArray = self.csvArray[index:]
                break

        # Remove the days of the last year if it is not complete.
        yearToDelete = None
        for index, row in enumerate(reversed(self.csvArray)):

            year = int(row[1][:4])
            if index == 0 and row[1][4:8] != '1231':
                yearToDelete = year
                continue

            if year == yearToDelete - 1:
                self.csvArray = self.csvArray[:-index]
                break

        dates = self.csvArray[:, 1]
        self.minYearFile = dates[1][:4]
        self.maxYearFile = dates[-1][:4]
