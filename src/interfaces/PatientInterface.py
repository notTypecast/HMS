from src.interfaces.Interface import Interface
from datetime import datetime
import src.utils as utils

class PatientInterface(Interface):
    def __init__(self):
        self.patient_id = 0
    
    @property
    def options(self):
        return {
            "Set Appointment": self.setAppointment,
            "View Profile": self.viewProfile,
        }
    
    def viewProfile(self):
        print("Patient Profile")
        conn = utils.get_db_connection()
        c = conn.cursor()
        c.execute("""
        SELECT * 
        FROM Patient 
        INNER JOIN Address ON Patient.address_id=Address.address_id 
        INNER JOIN Staff ON Patient.doctor_id=Staff.staff_id
        WHERE patient_id=?
        """, 
        (self.patient_id,))
        res = c.fetchall()[0]

        print(f"Name: {res[1]} {res[2]}")
        print(f"Email: {res[3]}")
        print(f"Date of birth: {res[4]}")
        print(f"Sex: {res[5]}")
        print(f"AMKA: {res[6]}")
        if res[7] is not None:
            print(f"Address: {res[12]} {res[13]}, {res[14]}")
        if res[8] is not None:
            print(f"Phone: {res[8]}")
        if res[9] is not None:
            print(f"Doctor: {res[16]} {res[17]}")

        while True:
            choice = input("Would you like to view your visit history or your prescriptions? (h/p/n): ").lower()
            if choice not in ("h", "p", "n"):
                print("Invalid choice")
                continue

            break

        if choice == "h":
            c.execute("SELECT * FROM Appointment INNER JOIN Staff ON Appointment.doctor_id=Staff.staff_id WHERE patient_id=? AND completed='True'", (self.patient_id,))
            res = c.fetchall()

            if len(res) == 0:
                print("You have no completed visits")
                return
            
            print("Visit History")

            for row in res:
                print("=====================================")
                print(f"Appointment on {row[3]}")
                print(f"Doctor: {row[7]} {row[8]}")
                print(f"Notes: {row[4]}")
            
            print("=====================================")

        elif choice == "p":
            c.execute("""
            SELECT * 
            FROM Prescription 
            INNER JOIN PrescriptionToMedicine ON Prescription.prescription_id=PrescriptionToMedicine.prescription_id 
            WHERE patient_id=?""", 
            (self.patient_id,))
            res = c.fetchall()

            if len(res) == 0:
                print("You have no active prescriptions")
                return
            
            print("Active Prescriptions")

            prescriptions = {}

            for row in res:
                if row[0] not in prescriptions:
                    prescriptions[row[0]] = []
                prescriptions[row[0]].append((row[4], row[5]))

            for i, prescription in enumerate(prescriptions.keys()):
                print("=====================================")
                print(f"Prescription {i+1}")
                for medicine in prescriptions[prescription]:
                    print(f"{medicine[0]}: {medicine[1]}mg")
            
            print("=====================================")
    
    def setAppointment(self):
        print("Set Appointment")
        speciality = input("Required doctor specialization: ")
        date = input("Preferred date (YYYY-MM-DD): ")
        info = input("Additional information: ")
        
        # ensure specialization exists
        conn = utils.get_db_connection()
        c = conn.cursor()
        c.execute("SELECT * FROM Doctor WHERE specialization=? COLLATE NOCASE", (speciality,))
        res = c.fetchall()

        if len(res) == 0:
            print("No such specialization available")
            return
        
        # ensure doctor is available
        req_day = datetime.strptime(date, "%Y-%m-%d").weekday()

        c.execute("SELECT day_bitmask FROM Doctor INNER JOIN Staff ON Doctor.doctor_id=Staff.staff_id WHERE specialization=? COLLATE NOCASE", (speciality,))
        res = c.fetchall()

        for day_bitmask in res:
            if day_bitmask[req_day] == "1":
                break
        
        else:
            print("No doctor available on that day")
            return
        
        # send notification to some secretary
        c.execute("SELECT secretary_id FROM Secretary LIMIT 1")
        secretary_id = c.fetchall()[0][0]

        c.execute("""
        INSERT INTO StaffNotification (message, notification_type, patient_id, speciality, appointment_date, appointment_info, staff_id)
        VALUES (?, ?)
        """,
        (
        f"Patient {self.patient_id} wants to set an appointment with a doctor of specialization {speciality} on {date} with additional information {info}",
        "AppointmentRequest",
        self.patient_id,
        speciality,
        date,
        info,
        secretary_id)
        )

        conn.commit()
        conn.close()
        
        print("Appointment request sent to secretary")
