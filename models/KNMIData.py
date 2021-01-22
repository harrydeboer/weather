import csv
import numpy as np


class KNMIData:

    def __init__(self):

        # Read txt file as list.
        txt_list = list()
        with open('data/KNMI.txt', newline='') as inputfile:
            reader = csv.reader(inputfile)
            last_good_row = None
            for row in reader:

                # The first few rows are comments starting with a #.
                if row[0][0] == '#':
                    continue

                # During april 1945 a lot of data is not available. 31 march 1945 data is put over all days of april.
                elif len(row) > 10 and row[4] == '     ' and row[1][:6] == '194504':
                    if last_good_row is None:
                        last_good_row = txt_list[-1:][0]
                    newlist = last_good_row
                    newlist[1] = row[1]
                    txt_list.append(newlist)

                else:
                    txt_list.append(row)

        self.array = np.asarray(txt_list)

        # Remove the days of the first years until most data is available.
        for index, row in enumerate(self.array):

            year = int(row[1][:4])

            # Most data is available from 1904 and onwards.
            if year == 1906:
                self.array = self.array[index:]
                break

        # Remove the days of the last year if it is not complete.
        year_to_delete = None
        for index, row in enumerate(reversed(self.array)):

            year = int(row[1][:4])
            if index == 0 and row[1][4:8] != '1231':
                year_to_delete = year
                continue

            if year_to_delete is not None:
                if year == year_to_delete - 1:
                    self.array = self.array[:-index]
                    break

        dates = self.array[:, 1]
        self.minYearFile = int(dates[1][:4])
        self.maxYearFile = int(dates[-1][:4])
