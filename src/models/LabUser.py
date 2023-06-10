from src.models.Staff import Staff
import src.utils as utils

class LabUser(Staff):
    def __init__(self, labuser_id):
        self.labuser_id = labuser_id

        conn = utils.get_db_connection()
        c = conn.cursor()
        c.execute(
            """
                SELECT * 
                FROM ExecutiveUser
                WHERE labuser_id = ?
                INNER JOIN Staff ON labuser_id  = Staff.staff_id
            """
            ,(labuser_id)
        )
        row = c.fetchall()[0]
        self.speciality = row[1]
        super().__init__(row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12])

    @staticmethod
    def add(first_name, last_name, email, birthdate, sex, monthly_salary, day_bitmask, start_time, end_time, speciality, address=None, phone=None):
        """
        Add a new LabUser to the database
        Returns LabUser object of newly created doctor
        """
        conn = utils.get_db_connection()
        c = conn.cursor()
        
        staff_id = utils.create_staff_member(first_name, last_name, email, birthdate, sex, monthly_salary, day_bitmask, start_time, end_time, address, phone)

        c.execute("INSERT INTO LabUser (labuser_id, speciality) VALUES (?, ?)", (staff_id, speciality))

        labUser = LabUser(c.lastrowid)

        conn.commit()
        conn.close()

        return labUser

    def __del__(self):
        """
        Destructor of LabUser
        Deletes the LabUser from the database
        """
        conn = utils.get_db_connection()
        c = conn.cursor()
        c.execute("DELETE FROM LabUser WHERE labuser_id=?", (self.labuser_id,))
        conn.commit()
        conn.close()

    def modify(self, first_name=None, last_name=None, email=None, birthdate=None, sex=None, monthly_salary=None, day_bitmask=None, start_time=None, end_time=None, speciality=None, address=None, phone=None):
        """
        Modify the LabUser's information
        Any of the arguments can be None, in which case the corresponding field is not updated
        """
        getarg = lambda new, old: new if new is not None else old

        conn = utils.get_db_connection()
        c = conn.cursor()
        c.execute("UPDATE Staff SET first_name=?, last_name=?, email=?, birthdate=?, sex=?, monthly_salary=?, day_bitmask=?, start_time=?, end_time=? WHERE staff_id=?", (getarg(first_name, self.first_name), getarg(last_name, self.last_name), getarg(email, self.email), getarg(birthdate, self.birthdate), getarg(sex, self.sex), getarg(monthly_salary, self.monthly_salary), getarg(day_bitmask, self.day_bitmask), getarg(start_time, self.start_time), getarg(end_time, self.end_time), self.labuser_id))
        c.execute("UPDATE LabUser SET speciality=? WHERE labuser_id=?", (getarg(speciality, self.speciality), self.labuser_id))
        conn.commit()
        conn.close()
                