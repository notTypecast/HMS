from abc import ABC
import src.utils as utils

class Staff(ABC):
    def __init__(self, staff_id, first_name, last_name, email, birthdate, sex, monthly_salary, day_bitmask, start_time, end_time, address=None, phone=None):
        self.staff_id = staff_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.birthdate = birthdate
        self.sex = sex
        self.monthly_salary = monthly_salary
        self.day_bitmask = day_bitmask
        self.start_time = start_time
        self.end_time = end_time
        self.address = address
        self.phone = phone

    def addNotification(self, message):
        """
        Add a notification to the staff member's notification list.
        """
        conn = utils.get_db_connection()
        c = conn.cursor()
        c.execute("INSERT INTO StaffNotification (message, staff_id) VALUES (?, ?)", (message, self.staff_id))
        conn.commit()
        conn.close()
        