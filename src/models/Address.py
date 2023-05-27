from src.utils import utils

class Address:
    def __init__(self, address_id, street_name, street_number, postal_code):
        self.address_id = address_id
        self.street_name = street_name
        self.street_number = street_number
        self.postal_code = postal_code

    @staticmethod
    def add(street_name, street_number, postal_code):
        """
        Add a new Address to the database
        Returns Address object of newly created address
        """
        conn = utils.get_db_connection()
        c = conn.cursor()
        
        c.execute("INSERT INTO Address (street_name, street_number, postal_code) VALUES (?, ?, ?)", (street_name, street_number, postal_code))

        address = Address(c.lastrowid, street_name, street_number, postal_code)
        conn.commit()
        conn.close()

        return address
    
    def __del__(self):
        """
        Destructor of Address
        Deletes the address from the database
        """
        conn = utils.get_db_connection()
        c = conn.cursor()
        c.execute("DELETE FROM Address WHERE address_id=?", (self.address_id,))
        conn.commit()
        conn.close()

    def modify(self, street_name=None, street_number=None, postal_code=None):
        """
        Modify the address
        """
        getarg = lambda new, old: new if new is not None else old
        
        conn = utils.get_db_connection()
        c = conn.cursor()
        c.execute("UPDATE Address SET street_name=?, street_number=?, postal_code=? WHERE address_id=?", (getarg(street_name, self.street_name), getarg(street_number, self.street_number), getarg(postal_code, self.postal_code), self.address_id))
        conn.commit()
        conn.close()
    