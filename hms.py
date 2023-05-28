from src.interfaces import *

ROLE = "Patient"
role_dict = {
    "Patient": PatientInterface,
}

if __name__ == "__main__":
    print("Welcome to the Hospital Management System")
    print(f"Logged in as: {ROLE}")

    interface = role_dict[ROLE]()
    interface.run()
