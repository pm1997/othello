import numpy as np


class Sum:
    _data = list()

    def init_database(self):
        csv = np.loadtxt("ml_moves.csv", delimiter=',')
        self._data = csv.reshape((17, 64, 2))

    #  ###################################################
    #  CAUTION: This will delete the learned factors! '  #
    #  ###################################################
    def _reset_database(self):
        """
        Reset stored played / won games
        """
        self._data = np.ones(shape=(17, 64, 2))
        self.store_database()

    def add_table(self, file):
        csv = np.loadtxt(file, delimiter=',')
        db = csv.reshape((17, 64, 2))
        r1 = 0
        for row in self._data:
            c1 = 0
            for column in row:
                column[0] += db[r1][c1][0]
                column[1] += db[r1][c1][1]
                c1 += 1
            r1 += 1
        print("finished")

    def store_database(self):
        with open("ml_moves.csv", 'w') as outfile:
            for row in self._data:
                np.savetxt(outfile, row, fmt='%-7.0f', delimiter=',')


sum1 = Sum()
sum1.init_database()
sum1.add_table("ml7.csv")
sum1.store_database()
