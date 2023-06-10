from src.interfaces.Interface import Interface
from src.models.Doctor import Doctor
from src.models.Patient import Patient
import src.utils as utils

class DoctorInterface(Interface):
    def __init__(self):
        doctor_id = 10
        self.doctor = Doctor(doctor_id)

    @property
    def options(self):
        return {
            "Check Notifications": self.check_notifications,
        }

    def check_notifications(self):
        notifications = self.doctor.get_notifications()

        if len(notifications) == 0:
            print("There are no unread notifications")
            return

        print("Unread Notifications")

        options_str = "Available options:\n"
        for i, notification in enumerate(notifications):
            options_str += str(i+1) + ": " + notification.message + "\n"
        
        
        choice = utils.get_num_choice(len(notifications), options_str, "Enter the option number: ")
        notification = notifications[choice-1]

        if notification.notification_type == "Symptoms":
            patient = Patient(notification.patient_id)
            print(f"Showing symptoms for patient {patient.first_name} {patient.last_name}")
            print(notification.symptoms)

            response = input("Reponse: ")
            patient.addNotification(f"Doctor {self.doctor.first_name} {self.doctor.last_name} responded to your symptoms: {response}")
    