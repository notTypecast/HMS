from abc import ABC
import src.utils as utils

class Medicine(ABC):
    def __init__(self, medicine_id,name,description,route_of_administration):
        self.medicine_id = medicine_id
        self.name = name
        self.description = description
        self.route_of_administration = route_of_administration

    @staticmethod
    def add(name, description, route_of_administration):
        """
        Add a new Medicine to the database
        Returns Medicine object of newly created doctor
        """
        conn = utils.get_db_connection()
        c = conn.cursor()
    
        c.execute("INSERT INTO Medicine (name,desc, description, route_of_administration) VALUES (?, ?, ?)", (name , description , route_of_administration))

        medicine = Medicine(c.lastrowid, name, description , route_of_administration)

        conn.commit()
        conn.close()

        return medicine

    def __del__(self):
        """
        Destructor of Medicine
        Deletes the Medicine from the database
        """
        conn = utils.get_db_connection()
        c = conn.cursor()
        c.execute("DELETE FROM Medicine WHERE medicine_id=?", (self.medicine_id,))
        conn.commit()
        conn.close()

    def modify(self, name=None, description=None, route_of_administration=None):
        """
        Modify the Medicine's information
        Any of the arguments can be None, in which case the corresponding field is not updated
        """
        getarg = lambda new, old: new if new is not None else old

        conn = utils.get_db_connection()
        c = conn.cursor()        
        c.execute("UPDATE Medicine SET name=?, description=?, route_of_administration=? WHERE medicine_id=?", (getarg(name, self.name), getarg(description, self.description), getarg(route_of_administration, self.route_of_administration), self.secretary_id))
        conn.commit()
        conn.close()
