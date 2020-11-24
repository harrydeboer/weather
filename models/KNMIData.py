import csv
import numpy as np


class KNMIData:

    def __init__(self):

        # Read txt file as list.
        txtList = list()
        with open('data/KNMI.txt', newline='') as inputfile:
            reader = csv.reader(inputfile)
            for row in reader:
                if row[0][0] == '#':
                    continue
                # elif row[1] == '19450401':
                #     jan = 1
                elif len(row) > 10 and row[4] == '     ':
                    newlist = ['0'] * len(row)
                    newlist[0] = row[0]
                    newlist[1] = row[1]
                    txtList.append(newlist)
                else:
                    txtList.append(row)

        self.array = np.asarray(txtList)

        # Remove the days of the first year if it is not complete.
        yearToDelete = None
        for index, row in enumerate(self.array):

            year = int(row[1][:4])

            if year == 1904:
                self.array = self.array[index:]
                break

        # Remove the days of the last year if it is not complete.
        yearToDelete = None
        for index, row in enumerate(reversed(self.array)):

            year = int(row[1][:4])
            if index == 0 and row[1][4:8] != '1231':
                yearToDelete = year
                continue

            if year == yearToDelete - 1:
                self.array = self.array[:-index]
                break

        dates = self.array[:, 1]
        self.minYearFile = dates[1][:4]
        self.maxYearFile = dates[-1][:4]
