from src.models.Staff import Staff
from src.models.Notification import Notification
import src.utils as utils

class Secretary(Staff):
    def __init__(self, secretary_id):
        self.secretary_id = secretary_id
        
        conn = utils.get_db_connection()
        c = conn.cursor()
        c.execute(
            """ 
                SELECT * 
                FROM Secretary 
                WHERE secretary_id = ?
                INNER JOIN Staff ON secretary_id = Staff.staff_id
            """
            , (secretary_id,)
        )
        row =  c.fetchall()[0]
        self.office_number = row[1]
        super().__init__(row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12])


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

        secretary = Secretary(c.lastrowid)

        conn.commit()
        conn.close()

        return secretary

    def remove(self):
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

    def getNotifications(self):
        """
        Get all notifications for this secretary
        """
        conn = utils.get_db_connection()
        c = conn.cursor()
        c.execute("SELECT notification_id FROM StaffNotification WHERE staff_id=?", (self.secretary_id,))
        res = c.fetchall()
        conn.close()
        
        return [Notification(notification_id) for notification_id in res]

    @staticmethod
    def addNotification(*args):
        """
        Add a notification to some secretary
        args: list of arguments to be inserted into the StaffNotification table, dependent on the notification type
        """
        conn = utils.get_db_connection()
        c = conn.cursor()

        c.execute("SELECT secretary_id FROM Secretary LIMIT 1")
        secretary_id = c.fetchall()[0][0]

        conn.close()

        Notification.addNotification("staff", *args, secretary_id)

    @staticmethod
    def setAppointment(patient_id, doctor_id, appointment_time):
        conn = utils.get_db_connection()
        c = conn.cursor()
        c.execute("""
                INSERT INTO Appointment(patient_id, doctor_id, appointment_time)
                VALUES(?, ?, ?)    
            """
            , (patient_id, doctor_id, appointment_time)
        )
        conn.close()

