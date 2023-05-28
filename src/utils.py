import sqlite3

DB_NAME = "hms.db"

def get_db_connection():
    """
    Returns a connection to the database.
    """
    return sqlite3.connect(DB_NAME)

def create_staff_member(cursor, first_name, last_name, email, birthdate, sex, monthly_salary, day_bitmask, start_time, end_time, address=None, phone=None):
    """
    Adds a staff member to the database
    Returns ID of the staff member
    """
    if address is not None:
        address = address.address_id

    cursor.execute("INSERT INTO Staff (first_name, last_name, email, birthdate, sex, monthly_salary, days_available, start_time, end_time, address_id, phone) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (first_name, last_name, email, birthdate, sex, monthly_salary, day_bitmask, start_time, end_time, address, phone))
    
    return cursor.lastrowid

def get_num_choice(list_len, options_str, prompt, exit=False):
    while True:
        print(options_str)
        choice = input(prompt)

        if exit and choice.lower() == "exit":
            return False

        try:
            choice = int(choice)
            if choice < 1 or choice > list_len:
                raise ValueError
            
            return choice

        except ValueError:
            print("Invalid option number")
            continue
