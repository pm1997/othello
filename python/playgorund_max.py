from database import Database

if __name__ == '__main__':
    d = Database()
    d.sum_databases("database_moves_max.csv")
    # d.train_db_multi_threaded(100000)
    # d.store_database()
