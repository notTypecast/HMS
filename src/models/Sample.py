import src.utils as utils

class Sample:
    def __init__(self, sample_id):
        self.sample_id = sample_id
        conn = utils.get_db_connection()
        c = conn.cursor()
        c.execute(
            """
                SELECT * FROM 
                Sample 
                WHERE sample_id = ?
                INNER JOIN LabUser ON Sample.labuser_id = LabUser.labuser_id
                INNER JOIN Patient ON Sample.patient_id = Patient.patient_id
            """
            , (sample_id,)
        )
        row = c.fetchall()[0]

        self.labuser_id = row[1]
        self.patient_id = row[2]
        self.doctor_id = row[3]
        self.description = row[4]
        self.result = row[5]

    @staticmethod
    def add(patient_id, doctor_id, description, result=None):
        """
        Add a new Sample to the database
        Returns Sample object of newly created sample
        """
        conn = utils.get_db_connection()
        c = conn.cursor()

        c.execute("SELECT labuser_id FROM LabUser LIMIT 1")
        labuser_id = c.fetchall()[0][0]
        
        c.execute("INSERT INTO Sample (labuser_id, patient_id, doctor_id, description, result) VALUES (?, ?, ?, ?)", (labuser_id, patient_id, doctor_id, description, result))

        sample = Sample(c.lastrowid)
        conn.commit()
        conn.close()

        return sample
    
    def setResult(self, result):
        """
        Set the result of the sample
        """
        conn = utils.get_db_connection()
        c = conn.cursor()
        c.execute("UPDATE Sample SET result=? WHERE sample_id=?", (result, self.sample_id))
        conn.commit()
        conn.close()
    
    @staticmethod
    def getSamplesForLabUser(labuser_id):
        conn = utils.get_db_connection()
        c = conn.cursor()
        c.execute("SELECT sample_id FROM Sample WHERE labuser_id = ?", (labuser_id,))
        rows = c.fetchall()
        conn.close()

        return [Sample(row[0]) for row in rows]
