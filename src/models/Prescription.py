import src.utils as utils

class Prescription:
    def __init__(self, prescription_id):
        """
        Constructor of Prescription
        medicine: list of tuples (medicine, quantity)
        """
        self.prescription_id = prescription_id

        conn = utils.get_db_connection()
        c = conn.cursor()
        c.execute("SELECT patient_id, doctor_id FROM Prescription WHERE prescription_id=?", (prescription_id,))
        row = c.fetchall()[0]
        conn.close()

        self.patient_id = row[0]
        self.doctor_id = row[1]

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

        prescription = Prescription(prescription_id)
        conn.commit()
        conn.close()

        return prescription
    
    def remove(self):
        """
        Destructor of Prescription
        Deletes the prescription from the database
        """
        conn = utils.get_db_connection()
        c = conn.cursor()
        c.execute("DELETE FROM Prescription WHERE prescription_id=?", (self.prescription_id,))
        conn.commit()
        conn.close()

    def getMedicine(self):
        """
        Returns list of tuples (medicine, amount_mg)
        """
        conn = utils.get_db_connection()
        c = conn.cursor()
        c.execute("SELECT Medicine.name, PrescriptionToMedicine.amount_mg FROM PrescriptionToMedicine INNER JOIN Medicine ON PrescriptionToMedicine.medicine_id=Medicine.medicine_id WHERE PrescriptionToMedicine.prescription_id=?", (self.prescription_id,))
        rows = c.fetchall()
        conn.close()

        return rows
        