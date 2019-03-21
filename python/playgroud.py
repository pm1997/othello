from database import Database

if __name__ == '__main__':
    db = Database()
    db.train_db_multi_threaded(100)
    # Trigger garbage collection
    # call destructor => store database to file
    db = None

