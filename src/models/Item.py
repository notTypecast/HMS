import src.utils as utils

class Item:
    def __init__(self, item_id):
        self.item_id = item_id

        conn = utils.get_db_connection()
        c = conn.cursor()
        c.execute("SELECT * FROM item WHERE item_id=?",(item_id,))
        row = c.fetchall()[0]

        self.name = row[1]
        self.description = row[2]

    @staticmethod
    def add(name, description):
        """
        Add a new Item to the database
        Returns Item object of newly created doctor
        """
        conn = utils.get_db_connection()
        c = conn.cursor()
        
        c.execute("INSERT INTO Item (name, description) VALUES (?, ?)", (name, description))

        item = Item(c.lastrowid, name, description)
        conn.commit()
        conn.close()

        return item

    def __del__(self):
        """
        Destructor of Item
        Deletes the item from the database
        """
        conn = utils.get_db_connection()
        c = conn.cursor()
        c.execute("DELETE FROM Item WHERE item_id=?", (self.item_id,))
        conn.commit()
        conn.close()

    def modify(self, name = None, description = None):
        """
        Modify the item
        """
        getarg = lambda new, old: new if new is not None else old
        
        conn = utils.get_db_connection()
        c = conn.cursor()
        c.execute("UPDATE Item SET name=?, description=? WHERE item_id=?", (getarg(name, self.name), getarg(description, self.description), self.item_id))
        conn.commit()
        conn.close()
        