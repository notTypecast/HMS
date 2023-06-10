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
        self.sample_date = row[3]
        self.result = row[4]

    @staticmethod
    def add(labuser_id, patient_id, sample_date, result):
        """
        Add a new Sample to the database
        Returns Sample object of newly created sample
        """
        conn = utils.get_db_connection()
        c = conn.cursor()
        
        c.execute("INSERT INTO Sample (labuser_id, patient_id, sample_date, result) VALUES (?, ?, ?, ?)", (labuser_id, patient_id, sample_date, result))

        sample = Sample(c.lastrowid)
        conn.commit()
        conn.close()

        return sample
    
    def __del__(self):
        """
        Destructor of Sample
        Deletes the sample from the database
        """
        conn = utils.get_db_connection()
        c = conn.cursor()
        c.execute("DELETE FROM Sample WHERE sample_id=?", (self.sample_id,))
        conn.commit()
        conn.close()

    def modify(self, labuser_id=None, patient_id=None, sample_date=None, result=None):
        """
        Modify the sample
        """
        getarg = lambda new, old: new if new is not None else old
        
        conn = utils.get_db_connection()
        c = conn.cursor()
        c.execute("UPDATE Sample SET labuser_id=?, patient_id=?, sample_date=?, result=? WHERE sample_id=?", (getarg(labuser_id, self.labuser_id), getarg(patient_id, self.patient_id), getarg(sample_date, self.sample_date), getarg(result, self.result), self.sample_id))
        conn.commit()
        conn.close()
