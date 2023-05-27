from src.models import Staff
import src.utils as utils

class Doctor(Staff):
    def __init__(self, doctor_id, first_name, last_name, email, birthdate, sex, monthly_salary, day_bitmask, start_time, end_time, speciality, address=None, phone=None):
        self.doctor_id = doctor_id
        self.speciality = speciality
        super().__init__(first_name, last_name, email, birthdate, sex, monthly_salary, day_bitmask, start_time, end_time, address, phone)

    @staticmethod
    def add(first_name, last_name, email, birthdate, sex, monthly_salary, day_bitmask, start_time, end_time, speciality, address=None, phone=None):
        """
        Add a new doctor to the database
        Returns Doctor object of newly created doctor
        """
        conn = utils.get_db_connection()
        c = conn.cursor()
        
        staff_id = utils.create_staff_member(first_name, last_name, email, birthdate, sex, monthly_salary, day_bitmask, start_time, end_time, address, phone)

        c.execute("INSERT INTO Doctor (doctor_id, speciality) VALUES (?, ?)", (staff_id, speciality))

        doctor = Doctor(c.lastrowid, first_name, last_name, email, birthdate, sex, monthly_salary, day_bitmask, start_time, end_time, speciality, address, phone)

        conn.commit()
        conn.close()

        return doctor

    def __del__(self):
        """
        Destructor of Doctor
        Deletes the doctor from the database
        """
        conn = utils.get_db_connection()
        c = conn.cursor()
        c.execute("DELETE FROM Doctor WHERE doctor_id=?", (self.doctor_id,))
        conn.commit()
        conn.close()

    def modify(self, first_name=None, last_name=None, email=None, birthdate=None, sex=None, monthly_salary=None, day_bitmask=None, start_time=None, end_time=None, speciality=None, address=None, phone=None):
        """
        Modify the doctor's information
        Any of the arguments can be None, in which case the corresponding field is not updated
        """
        getarg = lambda new, old: new if new is not None else old

        conn = utils.get_db_connection()
        c = conn.cursor()
        c.execute("UPDATE Staff SET first_name=?, last_name=?, email=?, birthdate=?, sex=?, monthly_salary=?, day_bitmask=?, start_time=?, end_time=? WHERE staff_id=?", (getarg(first_name, self.first_name), getarg(last_name, self.last_name), getarg(email, self.email), getarg(birthdate, self.birthdate), getarg(sex, self.sex), getarg(monthly_salary, self.monthly_salary), getarg(day_bitmask, self.day_bitmask), getarg(start_time, self.start_time), getarg(end_time, self.end_time), self.doctor_id))
        c.execute("UPDATE Doctor SET speciality=? WHERE doctor_id=?", (getarg(speciality, self.speciality), self.doctor_id))
        conn.commit()
        conn.close()
