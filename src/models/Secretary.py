from src.models import Staff
import src.utils as utils

class Secretary(Staff):
    def __init__(self, secretary_id, first_name, last_name, email, birthdate, sex, monthly_salary, day_bitmask, start_time, end_time, office_number, address=None, phone=None):
        self.secretary_id = secretary_id
        self.office_number = office_number
        super().__init__(first_name, last_name, email, birthdate, sex, monthly_salary, day_bitmask, start_time, end_time, address, phone)


    @staticmethod
    def add(first_name, last_name, email, birthdate, sex, monthly_salary, day_bitmask, start_time, end_time, office_number, address=None, phone=None):
        """
        Add a new Secretary to the database
        Returns Secretary object of newly created doctor
        """
        conn = utils.get_db_connection()
        c = conn.cursor()
        
        staff_id = utils.create_staff_member(first_name, last_name, email, birthdate, sex, monthly_salary, day_bitmask, start_time, end_time, address, phone)

        c.execute("INSERT INTO Secretary (secretary_id, office_number) VALUES (?, ?)", (staff_id, office_number))

        secretary = Secretary(c.lastrowid, first_name, last_name, email, birthdate, sex, monthly_salary, day_bitmask, start_time, end_time, office_number, address, phone)

        conn.commit()
        conn.close()

        return secretary

    def __del__(self):
        """
        Destructor of Secretary
        Deletes the Secretary from the database
        """
        conn = utils.get_db_connection()
        c = conn.cursor()
        c.execute("DELETE FROM Secretary WHERE secretary=?", (self.secretary_id,))
        conn.commit()
        conn.close()

    def modify(self, first_name=None, last_name=None, email=None, birthdate=None, sex=None, monthly_salary=None, day_bitmask=None, start_time=None, end_time=None, office_number=None, address=None, phone=None):
        """
        Modify the secretary's information
        Any of the arguments can be None, in which case the corresponding field is not updated
        """
        getarg = lambda new, old: new if new is not None else old

        conn = utils.get_db_connection()
        c = conn.cursor()
        c.execute("""
        UPDATE Staff
        SET first_name=?, last_name=?, email=?, birthdate=?, sex=?, monthly_salary=?, day_bitmask=?, start_time=?, end_time=?
        WHERE staff_id=?
        """, 
        (
        getarg(first_name, self.first_name),
        getarg(last_name, self.last_name),
        getarg(email, self.email),
        getarg(birthdate, self.birthdate),
        getarg(sex, self.sex),
        getarg(monthly_salary, self.monthly_salary),
        getarg(day_bitmask, self.day_bitmask),
        getarg(start_time, self.start_time), 
        getarg(end_time, self.end_time),
        self.secretary_id)
        )
        c.execute("UPDATE Secretary SET office_number=? WHERE secretary_id=?", (getarg(office_number, self.office_number), self.secretary_id))
        
        conn.commit()
        conn.close()
