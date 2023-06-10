import src.utils as utils

class Appointment:
    def __init__(self, visit_id):
        self.visit_id = visit_id
        
        conn = utils.get_db_connection()
        c = conn.cursor()
        c.execute("SELECT * FROM Appointment WHERE visit_id = ?",(visit_id,))
        row = c.fetchall()[0]
        conn.close()

        self.patient_id = row[1]
        self.doctor_id = row[2]
        self.appointment_time = row[3]
        self.notes = row[4]
        self.completed = row[5]

    @staticmethod
    def add(patient_id, doctor_id, appointment_time):
        """
        Add a new Appointment to the database
        Returns Appointment object of newly created doctor
        """
        conn = utils.get_db_connection()
        c = conn.cursor()
        
        c.execute("INSERT INTO Appointment (patient_id, doctor_id, appointment_time, completed) VALUES (?, ?, ?, ?)", (patient_id, doctor_id, appointment_time, "False"))

        appointment = Appointment(c.lastrowid)
        conn.commit()
        conn.close()

        return appointment
    
    def remove(self):
        """
        Destructor of Appointment
        Deletes the appointment from the database
        """
        conn = utils.get_db_connection()
        c = conn.cursor()
        c.execute("DELETE FROM Appointment WHERE visit_id=?", (self.visit_id,))
        conn.commit()
        conn.close()

    def modify(self, patient_id=None, doctor_id=None, appointment_time=None, completed=None):
        """
        Modify the appointment
        """
        getarg = lambda new, old: new if new is not None else old
        
        conn = utils.get_db_connection()
        c = conn.cursor()
        c.execute("UPDATE Appointment SET patient_id=?, doctor_id=?, appointment_time=?, completed=? WHERE visit_id=?", (getarg(patient_id, self.patient_id), getarg(doctor_id, self.doctor_id), getarg(appointment_time, self.appointment_time), getarg(completed, self.completed), self.visit_id))
        conn.commit()
        conn.close()

    def getDoctorName(self):
        conn = utils.get_db_connection()
        c = conn.cursor()
        c.execute("SELECT first_name, last_name FROM Doctor WHERE doctor_id=?", (self.doctor_id,))
        row = c.fetchall()[0]
        conn.close()
        
        return row[0] + " " + row[1]
        