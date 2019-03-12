import numpy as np


class Analyse:

    # data of csv ml_moves.csv
    _data = list()

    # data as % of winning
    _data2 = list()

    def init(self):
        """
        import csv file and store in self._data
        """
        csv = np.loadtxt('ml_moves.csv', delimiter=',')
        self._data = csv.reshape((17, 64, 2))

    def analyse(self):
        """
        analyse self._data
        get highest probability of winning per turn row
        """
        # init result array
        self._data2 = np.ones(shape=(17, 8, 8))
        pos = 0
        for position in range(17):
            print(f"position: {position * 4}")
            r = 0
            for row in self._data[position]:
                # calculate change of winning
                a = row[0] / row[1] * 100
                if row[1] == 1:
                    a = 0.1
                self._data2[pos][r // 8][r % 8] = "{:.2f}".format(a)
                # print(a)
                r += 1

            s1 = np.sum(self._data2[pos])
            print(f"max: {np.max(self._data2[pos])}")
            r = 0
            for row in self._data[position]:
                if row[1] == 1:
                    a = 100
                    self._data2[pos][r // 8][r % 8] = "{:.2f}".format(a)
                r += 1
            print(f"min: {np.min(self._data2[pos])}")
            s2 = np.sum(self._data2[pos])
            s3 = (s1 + s2) / 128
            print(f"average: {s3}")

            r = 0
            for row in self._data[position]:
                if row[1] == 1:
                    a = s3
                    self._data2[pos][r // 8][r % 8] = "{:.2f}".format(a)
                r += 1
            print(f"var: {np.var(self._data2[pos], ddof=1)}")

            print(self._data2[pos])

            print("_______________________")
            pos += 1


an1 = Analyse()
an1.init()
an1.analyse()
