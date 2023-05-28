import src.utils as utils

class Patient:
    def __init__(self, patient_id, first_name, last_name, email, birthdate, sex, AMKA, doctor_id, symptoms, address=None, phone=None):
        self.patent_id  = patient_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.birthdate  = birthdate
        self.sex = sex
        self.AMKA = AMKA
        self.doctor_id = doctor_id
        self.symptoms = symptoms

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

        patient = Patient(c.lastrowid, first_name, last_name, email, birthdate, sex, AMKA, doctor_id, symptoms, address, phone)

        conn.commit()
        conn.close()

        return patient
    
    def __del__(self):
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
    