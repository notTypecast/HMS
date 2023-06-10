from src.interfaces.Interface import Interface
from datetime import datetime 
from src.models.Secretary import Secretary
from src.models.Patient import Patient
import src.utils as utils

class SecretaryInterface(Interface):
    def __init__(self):
        self.staff_id = 0
        self.secretary = Secretary(self.staff_id)

    @property
    def options(self):
        return {
            "Check Notifications": self.checkNotifications
        }

    def checkNotifications(self):
        notifications = self.secretary.getNotifications(self.staff_id)

        if len(notifications) == 0:
            print("There are no unread notifications")
            return

        print("Unread Notifications")

        options_str = "Available options:\n"
        for i, notification in enumerate(notifications):
            options_str += str(i+1) + ": " + notification.message + "\n"
        
        
        choice = utils.get_num_choice(len(notifications), options_str, "Enter the option number: ")
        notification = notifications[choice-1]

        if notification.notification_type == "AppointmentRequest":
            req_day = datetime.strptime(notification.appointment_date, "%Y-%m-%d").weekday() 

            doctorsAvailable = Secretary.getAvailabileDoctors(notification.speciality, req_day)

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


                patient = Patient(notification.patient_id)
                patient.addNotification(f"Your appointment request for {notification.appointment_date} was cancelled{cancellation_reason}")
                
                print("Notification sent to patient")

                return


            options_str = "The available doctors for this appointment are:\n"
            for i, doctor in enumerate(doctorsAvailable):
                options_str += str(i+1) + ":" + doctor.first_name + "," + doctor.last_name + "\n"


            choice = utils.get_num_choice(len(doctorsAvailable), options_str, "Enter the doctor's option number: ")
            chosenDoctor = notifications[choice-1]

            additional_info = "Additional information:\n" + input("Provide additional information for the patient: ")

            Secretary.setAppointment(notification.patient_id, doctor.doctor_id, notification.appointment_date)

            chosenDoctor.addNotification(f"An appointment has been scheduled for {notification.appointment_date}.", "Message", doctor.doctor_id)

            patient = Patient(notification.patient_id)
            patient.addNotification(f"Your appointment request was accepted! Your appointment is scheduled for {notification.appointment_date}.{additional_info}")

        elif notification.notification_type == "Symptoms":
            # TODO symptoms notification use case
            pass
