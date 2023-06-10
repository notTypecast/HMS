from src.interfaces.Interface import Interface
from datetime import datetime
from src.models.Patient import Patient
from src.models.Doctor import Doctor
from src.models.Secretary import Secretary

class PatientInterface(Interface):
    def __init__(self):
        patient_id = 0
        self.patient = Patient(patient_id)
    
    @property
    def options(self):
        return {
            "Set Appointment": self.setAppointment,
            "View Profile": self.viewProfile,
            "Set Symptoms": self.setSymptoms,
        }
    
    def setSymptomps(self):
        print("Set Symptoms")
        symptoms = input("Briefly describe your symptoms: ")

        self.patient.setSymptoms(symptoms)

        if self.patient.getDoctorName() is None:
            Secretary.addNotification(f"Patient {self.patient.first_name} {self.patient.last_name} has updated their symptoms, please assign a doctor to view them.", 
                                      "Symptoms", 
                                      self.patient.patient_id,
                                      symptoms)
        
        else:
            patient_doctor = Doctor(self.patient.doctor_id)
            patient_doctor.addNotification(f"Patient {self.patient.first_name} {self.patient.last_name} has updated their symptoms, please respond to them.",
                                           "Symptoms",
                                            self.patient.patient_id,
                                            symptoms)
            
        print("Symptoms updated successfully")
    
    def viewProfile(self):
        print("Patient Profile")

        print(f"Name: {self.patient.first_name} {self.patient.last_name}")
        print(f"Email: {self.patient.email}")
        print(f"Date of birth: {self.patient.birthdate}")
        print(f"Sex: {self.patient.sex}")
        print(f"AMKA: {self.patient.AMKA}")

        address = self.patient.getAddress()
        if address is not None:
            print(f"Address: {address.full()}")
        
        if self.patient.phone is not None:
            print(f"Phone: {self.patient.phone}")

        doctor_name = self.patient.getDoctorName()
        if doctor_name is not None:
            print(f"Doctor: {doctor_name}")

        while True:
            choice = input("Would you like to view your visit history or your prescriptions? (h/p/n): ").lower()
            if choice not in ("h", "p", "n"):
                print("Invalid choice")
                continue

            break

        if choice == "h":
            history = self.patient.getHistory()

            if len(history) == 0:
                print("You have no completed visits")
                return
            
            print("Visit History")

            for appointment in history:
                print("=====================================")
                print(f"Appointment on {appointment.appointment_time}")
                print(f"Doctor: {appointment.getDoctorName()}")
                print(f"Notes: {appointment.notes}")
            
            print("=====================================")

        elif choice == "p":
            prescriptions = self.patient.getPrescriptions()

            if len(prescriptions) == 0:
                print("You have no active prescriptions")
                return
            
            print("Active Prescriptions")

            for i, prescription in enumerate(prescriptions):
                print("=====================================")
                print(f"Prescription {i+1}")
                for medicine in prescription.getMedicine():
                    print(f"{medicine[0]}: {medicine[1]}mg")
            
            print("=====================================")
    
    def setAppointment(self):
        print("Set Appointment")
        speciality = input("Required doctor speciality: ")
        date = input("Preferred date (YYYY-MM-DD): ")
        info = input("Additional information: ")
        
        # ensure speciality exists
        if not Doctor.specialityExists(speciality):
            print("No such specialization available")
            return
        
        # ensure doctor is available
        req_day = datetime.strptime(date, "%Y-%m-%d").weekday()

        if not Doctor.doctorAvailable(speciality, req_day):
            print("No doctor available on that day")
            return
        
        # send notification to some secretary
        Secretary.addNotification(
        f"Patient {self.patient.first_name} {self.patient.last_name} wants to set an appointment with a doctor of speciality {speciality} on {date} with additional information {info}",
        "AppointmentRequest",
        self.patient_id,
        speciality,
        date,
        info)
        
        print("Appointment request sent to secretary")
