import src.utils as utils
from src.models.Address import Address
from src.models.Appointment import Appointment
from src.models.Prescription import Prescription
from src.models.Notification import Notification

class Patient:
    def __init__(self, patient_id):
        self.patent_id  = patient_id

        conn = utils.get_db_connection()
        c = conn.cursor()
        c.execute("SELECT * FROM Patient WHERE patient_id=?", (patient_id,))
        row = c.fetchall()[0]
        conn.close()

        self.first_name = row[1]
        self.last_name = row[2]
        self.email = row[3]
        self.birthdate = row[4]
        self.sex = row[5]
        self.AMKA = row[6]
        self.address_id = row[7]
        self.phone = row[8]
        self.doctor_id = row[9]
        self.symptoms = row[10]

    @staticmethod
    def add(first_name, last_name, email, birthdate, sex, AMKA, doctor_id, symptoms, address=None, phone=None):
        """
        Add a new patient to the database
        Returns Patient object of newly created patient
        """
        if address is not None:
            address = address.address_id

        conn = utils.get_db_connection()
        c = conn.cursor()
        c.execute("""
        INSERT INTO Patient (first_name, last_name, email, birthdate, sex, AMKA, address_id, phone, doctor_id, symptoms) 
        VALUES (?, ?)
        """, (first_name, last_name, email, birthdate, sex, AMKA, doctor_id, symptoms))

        patient = Patient(c.lastrowid)

        conn.commit()
        conn.close()

        return patient
    
    def remove(self):
        """
        Destructor of Patient
        Deletes the patient from the database
        """
        conn = utils.get_db_connection()
        c = conn.cursor()
        c.execute("DELETE FROM Patient WHERE patient_id=?", (self.patent_id,))
        conn.commit()
        conn.close()
    
    def modify(self, first_name=None, last_name=None, email=None, birthdate=None, sex=None, AMKA=None, doctor_id=None, symptoms=None, address=None, phone=None):
        """
        Modify the patient's information
        Any of the arguments can be None, in which case the corresponding field is not updated
        """
        getarg = lambda new, old: new if new is not None else old

        if address is not None:
            address = address.address_id

        conn = utils.get_db_connection()
        c = conn.cursor()

        c.execute("""
        UPDATE Patient 
        SET first_name=?, last_name=?, email=?, birthdate=?, sex=?, AMKA=?, doctor_id=?, symptoms=?, address=?, phone=? 
        WHERE patient_id=?
        """, 
        (
        getarg(first_name, self.first_name), 
        getarg(last_name, self.last_name),
        getarg(email, self.email),
        getarg(birthdate, self.birthdate),
        getarg(sex, self.sex),
        getarg(AMKA, self.AMKA),
        getarg(doctor_id, self.doctor_id),
        getarg(symptoms, self.symtoms),
        getarg(address, self.address),
        getarg(phone, self.phone), self.patient_id)
        )

        conn.commit()
        conn.close()

    def addNotification(self, message):
        """
        Add a notification to the patient
        """
        Notification.addNotification("patient", message, self.patient_id)

    def getAddress(self):
        """
        Returns the address of the patient
        """
        if self.address_id is None:
            return None
        
        return Address(self.address_id)
    
    def getDoctorName(self):
        """
        Returns the name of the patient's doctor
        """
        if self.doctor_id is None:
            return None

        conn = utils.get_db_connection()
        c = conn.cursor()
        c.execute("SELECT first_name, last_name FROM Doctor WHERE doctor_id=?", (self.doctor_id,))
        row = c.fetchall()[0]
        conn.close()

        return row[0] + " " + row[1]
    
    def getHistory(self):
        """
        Returns a list of all the patient's appointments
        """
        conn = utils.get_db_connection()
        c = conn.cursor()
        c.execute("SELECT appointment_id FROM Appointment WHERE patient_id=?", (self.patient_id,))
        rows = c.fetchall()
        conn.close()

        return [Appointment(row[0]) for row in rows]
    
    def getPrescriptions(self):
        """
        Returns a list of all the patient's prescriptions
        """
        conn = utils.get_db_connection()
        c = conn.cursor()
        c.execute("SELECT prescription_id FROM Prescription WHERE patient_id=?", (self.patient_id,))
        rows = c.fetchall()
        conn.close()

        return [Prescription(row[0]) for row in rows]
    
    def setSympotms(self, symptoms):
        """
        Sets the patient's symptoms
        """
        self.symptoms = symptoms
        self.modify(symptoms=symptoms)
    
    