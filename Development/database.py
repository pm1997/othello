import sqlite3


class Database:

    def test(self):
        conn = sqlite3.connect('othello.db')
        c = conn.cursor()

        c.execute("Drop TABLE if exists stocks")
        # Create table
        c.execute("CREATE TABLE if not exists stocks (date text, trans text, symbol text, qty real, price real)")

        # Insert a row of data
        c.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")

        # Save (commit) the changes
        conn.commit()

        # We can also close the connection if we are done with it.
        # Just be sure any changes have been committed or they will be lost.
        #conn.close()

        t = ('RHAT',)
        c.execute('SELECT * FROM stocks WHERE symbol=?', t)
        print(c.fetchone())

        # Larger example that inserts many records at a time
        purchases = [('2006-03-28', 'BUY', 'IBM', 1000, 45.00),
                     ('2006-04-05', 'BUY', 'MSFT', 1000, 72.00),
                     ('2006-04-06', 'SELL', 'IBM', 500, 53.00),
                    ]
        c.executemany('INSERT INTO stocks VALUES (?,?,?,?,?)', purchases)
        # Save (commit) the changes
        conn.commit()

        c.execute('SELECT * FROM stocks')
        results = c.fetchall()
        for result in results:
            print("Result : %s" % (result,))
        # We can also close the connection if we are done with it.
        # Just be sure any changes have been committed or they will be lost.
        conn.close()
