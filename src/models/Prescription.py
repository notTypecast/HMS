from abc import ABC
import src.utils as utils

class Prescription(ABC):
    def __init__(self, prescription_id, patient_id, doctor_id, medicine):
        """
        Constructor of Prescription
        medicine: list of tuples (medicine, quantity)
        """
        self.prescription_id = prescription_id
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.medicine = medicine

    @staticmethod
    def add(patient_id, doctor_id, medicine_ids):
        """
        Add a new Prescription to the database
        Returns Prescription object of newly created doctor
        medicine_ids: list of tuples (medicine_id, quantity)
        """
        conn = utils.get_db_connection()
        c = conn.cursor()
        
        c.execute("INSERT INTO Prescription (patient_id, doctor_id) VALUES (?, ?)", (patient_id, doctor_id))
        
        prescription_id = c.lastrowid

        for medicine in medicine_ids:
            c.execute("INSERT INTO PrescriptionToMedicine (prescription_id, medicine_id, amount_mg) VALUES (?, ?, ?)", (prescription_id, medicine[0], medicine[1]))

        prescription = Prescription(prescription_id, patient_id, doctor_id)
        conn.commit()
        conn.close()

        return prescription
    
    def __del__(self):
        """
        Destructor of Prescription
        Deletes the prescription from the database
        """
        conn = utils.get_db_connection()
        c = conn.cursor()
        c.execute("DELETE FROM Prescription WHERE prescription_id=?", (self.prescription_id,))
        conn.commit()
        conn.close()

    def modify(self, patient_id=None, doctor_id=None):
        """
        Modify the prescription
        """
        getarg = lambda new, old: new if new is not None else old
        
        conn = utils.get_db_connection()
        c = conn.cursor()
        c.execute("UPDATE Prescription SET patient_id=?, doctor_id=? WHERE prescription_id=?", (getarg(patient_id, self.patient_id), getarg(doctor_id, self.doctor_id), self.prescription_id))
        conn.commit()
        conn.close()
        