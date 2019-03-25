from database import Database
# from start_tables import StartTables
# from othello import Othello

if __name__ == '__main__':
    db = Database()
    db.train_db_multi_threaded(100000)
    # Trigger garbage collection
    # call destructor => store database to file
    db.store_database()
    db = None
    # g = Othello()
    # g.init_game()
    # st = StartTables()
    # st.calculate_missing_start_moves()
    # print(st.get_available_start_tables(g))
