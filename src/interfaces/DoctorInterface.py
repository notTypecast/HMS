from src.interfaces.Interface import Interface
from src.models.Doctor import Doctor
from src.models.Patient import Patient
from src.models.Prescription import Prescription
from src.models.Medicine import Medicine
import src.utils as utils

class DoctorInterface(Interface):
    def __init__(self):
        doctor_id = 10
        self.doctor = Doctor(doctor_id)

    @property
    def options(self):
        return {
            "Check Notifications": self.check_notifications,
            "View Patients": self.view_patients,
        }

    def view_patients(self):
        options_str = "Available options:\n"

        for i, option in enumerate(("View personal patients", "Search patients by name", "View all patients")):
            option_str += str(i+1) + ":" + option + "\n"

        choice = utils.get_num_choice(3, options_str, "Enter option number or exit: ", exit=True)

        if choice == 1:
            get_patients = lambda page_num: Patient.searchPatiensByDoctor(self.doctor.id, page_num=page_num)

        elif choice == 2:
            print("=====================================")
            firstNameToSearch = input("First name: ")
            lastNameToSearch = input("Last name: ")
            print("=====================================")
            get_patients = lambda page_num: Patient.searchPatientsByName(firstNameToSearch, lastNameToSearch, page_num=page_num)

        elif choice == 3:
            get_patients = lambda page_num: Patient.getAllPatients(page_num=page_num)

        else:
            return

        page = 0
        patients = []
        while True:
            while len(patients) == 0:
                page -= 1
                doctors = get_patients(page)

            options_str = f"Available options, page {page+1}:\n"

            for i, patient in enumerate(patients):
                options_str += str(i+1) + ": " + patient[0] + patient[1] + "\n"

            choice = utils.get_num_choice(len(doctors)+1, options_str, "Enter the patient number: ", other=["next", "prev"])

            if choice == "next":
                page += 1
            elif choice == "prev":
                if page > 0:
                    page -= 1
            else:
                patient = Patient(patients[choice-1][2])
                break

        print("Showing patient info")
        print("First name:", patient.first_name)
        print("Last name:", patient.last_name)
        print("Email:", patient.email)
        print("Birthday:", patient.birthday)
        print("Sex", patient.sex)
        print("AMKA:", patient.AMKA)

        options_str = "Available options:\n"

        for i, option in enumerate(("View History", "View Prescriptions")):
            option_str += str(i+1) + ":" + option + "\n"

        choice = utils.get_num_choice(2, options_str, "Enter option number or exit: ", exit=True)

        if choice == 1:
            history = patient.getHistory()

            if len(history) == 0:
                print("Patient has no completed visits")
                return
            
            print("Patient's Visit History")

            for appointment in history:
                print("=====================================")
                print(f"Appointment on {appointment.appointment_time}")
                print(f"Doctor: {appointment.getDoctorName()}")
                print(f"Notes: {appointment.notes}")
            
            print("=====================================")

        elif choice == 2:
            while True:
                add = input("Would you like to add a new prescription? (y/n): ").lower()

                if add == "y" or add == "n":
                    add = add == "y"
                    break

                print("Invalid input")

            if add:
                page = 0
                selected = []
                medicine = []
                while True:
                    while len(medicine) == 0:
                        page -= 1
                        medicines = Medicine.getAllMedicine(page_num=page)

                    options_str = f"Available options, page {page+1}:\n"

                    for i, medicine in enumerate(medicines):
                        options_str += str(i+1) + ": " + medicine[0] + "\n"

                    choice = utils.get_num_choice(len(medicines)+1, options_str, "Enter the medicine number: ", other=["next", "prev", "done"])

                    if choice == "next":
                        page += 1
                    elif choice == "prev":
                        if page > 0:
                            page -= 1
                    elif choice == "done":
                        if len(selected) == 0:
                            print("You must select at least one medicine")
                            continue
                        break
                    else:
                        medicine_id = medicines[choice-1][1]
                        while True:
                            quantity = input("Enter the quantity (in mg): ")
                            try:
                                quantity = int(quantity)
                                if quantity <= 0:
                                    raise ValueError
                                break
                            except ValueError:
                                print("Invalid input")
                        selected.append((medicine_id, quantity))
                
                Prescription.add(patient.patent_id, self.doctor.doctor_id, selected)
                return

            prescriptions = patient.get_prescriptions()

            if len(prescriptions) == 0:
                print("Patient has no active prescriptions")
                return

            options_str = "Patient's Active Prescriptions"

            for i, prescription in enumerate(prescriptions):
                options_str += str(i+1) + ": "
                for medicine in prescription.getMedicine():
                    options_str += medicine[0] + ", "
                options_str = options_str[:-2] + "\n"

            choice = utils.get_num_choice(len(prescriptions), options_str, "Enter the prescription number: ", exit=True)
            prescription = prescriptions[choice-1]

            print("Showing prescription info")
            for medicine in prescription.getMedicine():
                print(f"Medicine: {medicine[0]}, {medicine[1]}mg")

            while True:
                delete = input("Would you like to delete the prescription? (y/n): ").lower()

                if delete == "y":
                    delete = True
                    break
                elif delete == "n":
                    return

                print("Invalid input")

            if delete:
                prescription.remove()
                
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
    