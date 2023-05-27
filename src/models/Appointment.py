from abc import ABC
import src.utils as utils

class Appointment(ABC):
    def __init__(self, visit_id, patient_id, doctor_id, appointment_time, completed):
        self.visit_id = visit_id
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.appointment_time = appointment_time
        self.completed = completed

    @staticmethod
    def add(patient_id, doctor_id, appointment_time):
        """
        Add a new Appointment to the database
        Returns Appointment object of newly created doctor
        """
        conn = utils.get_db_connection()
        c = conn.cursor()
        
        c.execute("INSERT INTO Appointment (patient_id, doctor_id, appointment_time, completed) VALUES (?, ?, ?, ?)", (patient_id, doctor_id, appointment_time, "False"))

        appointment = Appointment(c.lastrowid, patient_id, doctor_id, appointment_time, "False")
        conn.commit()
        conn.close()

        return appointment
    
    def __del__(self):
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