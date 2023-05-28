from src.interfaces.Interface import Interface
from datetime import datetime
import src.utils as utils 

class SecretaryInterface(Interface):
    def __init__(self):
        self.staff_id = 0

    @property
    def options(self):
        return {
            "Check Notifications": self.checkNotifications
        }

    def checkNotifications(self):
        conn = utils.get_db_connection()
        c = conn.cursor()
        c.execute("SELECT * FROM StaffNotification WHERE staff_id=?", (self.staff_id,))
        res = c.fetchall()

        if len(res) == 0:
            print("There are no unread notifications")
            return

        print("Unread Notifications")

        options_str = "Available options:\n"
        for i, option in enumerate(res):
            options_str += str(i+1) + ": " + option[1] + "\n"
        
        
        choice = utils.get_num_choice(len(res), options_str, "Enter the option number: ")
        notification = res[choice-1]

        if notification[2] == "AppointmentRequest":
            speciality = notification[4]
            req_day = datetime.strptime(notification[5], "%Y-%m-%d").weekday()
            c.execute(
                """
                    SELECT Staff.first_name, Staff.last_name, Doctor.speciality, Staff.days_available,Doctor.doctor_id
                    FROM Doctor 
                    INNER JOIN Staff ON Doctor.doctor_id = Staff.staff_id
                    WHERE Doctor.speciality = ? 
                        AND (Staff.days_available & (1 << ?)) > 0
                """
            ,(speciality, req_day,))
            doctorsAvailable = c.fetchall()

            while True:
                choice = input("Would you like to accept this request? (y/n)").lower()

                if choice in ("y", "n"):
                    break

                print("Invalid response")

            if choice == "y" or len(doctorsAvailable) == 0:
                if len(doctorsAvailable) == 0:
                    print("No available doctors found")
                    cancellation_reason = ", because no doctors were available."
                else:
                    reason = input("Provide a reason for the cancellation: ")
                    cancellation_reason = f". Cancellation reason: \n {reason}"

                c.execute("""
                    INSERT INTO PatientNotification (message, patient_id)
                    VALUES (?, ?)
                """, (
                    f"Your appointment request for {notification[5]} was cancelled{cancellation_reason}",
                    notification[3]
                ))

                print("Notification sent to patient")

                return


            options_str = "The available Doctors for this appointment are:\n"
            for i, option in enumerate(res):
                options_str += str(i+1) + ":" + option[0] + "," + option[1] + "\n"



            choice = utils.get_num_choice(len(doctorsAvailable), options_str, "Enter the doctor's option number: ")
            chosenDoctor = res[choice-1]

            additional_info = "Additional information:\n" + input("Provide additional information for the patient: ")

            # TODO: determine appointment time

            c.execute("""
                INSERT INTO Appointment(patient_id,doctor_id,appointment_time)
                VALUES(?,?,?)    
            """
            ,(notification[3], chosenDoctor[4], notification[5],))

            c.execute("""
                INSERT INTO StaffNotification (message, staff_id, notification_type)
                VALUES (?, ?, ?)
            """, (
                f"An appointment has been scheduled for {notification[5]}.",
                chosenDoctor[4],
                "Message"
            ))

            c.execute("""
                INSERT INTO PatientNotification (message, patient_id)
                VALUES (?, ?)
            """, (
                f"Your appointment request was accepted! Your appointment is scheduled for {notification[5]}.{additional_info}",
                notification[3]
            ))
