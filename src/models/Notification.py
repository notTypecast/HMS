import src.utils as utils

class Notification:
    def __init__(self, recipient, notification_id):
        if recipient not in ("patient", "staff"):
            raise ValueError("Invalid recipient")
        
        self.recipient = recipient

        if recipient == "patient":
            conn = utils.get_db_connection()
            c = conn.cursor()
            c.execute("SELECT message, patient_id FROM Notification WHERE notification_id=?", (notification_id,))

            row = c.fetchall()[0]
            conn.close()
            self.message = row[0]
            self.patient_id = row[1]

        elif recipient == "staff":
            conn = utils.get_db_connection()
            c = conn.cursor()
            c.execute("SELECT * FROM StaffNotification WHERE notification_id=?", (notification_id,))

            row = c.fetchall()[0]
            conn.close()
            
            self.message = row[1]
            self.notification_type = row[2]

            if self.notification_type == "AppointmentRequest":
                self.patient_id = row[3]
                self.speciality = row[4]
                self.appointment_date = row[5]
                self.appointment_info = row[6]
            elif self.notification_type == "Symptoms":
                self.patient_id = row[3]
                self.symptoms = row[7]

            self.staff_id = row[-1]

    @staticmethod
    def addNotification(recipient, *args):
        """
        Add a notification to patient or staff
        args: list of arguments to be inserted into the corresponding table
        """
        if recipient not in ("patient", "staff"):
            raise ValueError("Invalid recipient")

        conn = utils.get_db_connection()
        c = conn.cursor()

        if recipient == "patient":
            c.execute("INSERT INTO Notification (message, patient_id) VALUES (?, ?)", args)
        elif recipient == "staff":
            if args[1] == "AppointmentRequest":
                c.execute("""INSERT INTO StaffNotification (message, notification_type, patient_id, speciality, appointment_date, appointment_info, staff_id) VALUES (?, ?, ?, ?, ?, ?, ?)""", 
                args)
            elif args[1] == "Symptoms":
                c.execute("""INSERT INTO StaffNotification (message, notification_type, patient_id, symptoms, staff_id) VALUES (?, ?, ?, ?, ?)""",
                args)
            elif args[1] == "Message":
                c.execite("""INSERT INTO StaffNotification (message, notification_type, staff_id) VALUES (?, ?, ?)""",
                args)
            
        conn.commit()
        conn.close()
