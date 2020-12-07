import csv
import numpy as np


class KNMIData:

    def __init__(self):

        # Read txt file as list.
        txtList = list()
        with open('data/KNMI.txt', newline='') as inputfile:
            reader = csv.reader(inputfile)
            lastGoodRow = None
            for row in reader:

                # The first few rows are comments starting with a #.
                if row[0][0] == '#':
                    continue

                # During april 1945 a lot of data is not available. 31 march data is put over all days of april.
                elif len(row) > 10 and row[4] == '     ' and row[1][:6] == '194504':
                    if lastGoodRow is None:
                        lastGoodRow = txtList[-1:][0]
                    newlist = lastGoodRow
                    newlist[1] = row[1]
                    txtList.append(newlist)

                else:
                    txtList.append(row)

        self.array = np.asarray(txtList)

        # Remove the days of the first years until all data is available.
        for index, row in enumerate(self.array):

            year = int(row[1][:4])

            # Most data is available from 1904 and onwards.
            if year == 1906:
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
        self.minYearFile = int(dates[1][:4])
        self.maxYearFile = int(dates[-1][:4])
