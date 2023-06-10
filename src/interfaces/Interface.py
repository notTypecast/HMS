from abc import ABC, abstractmethod
import src.utils as utils
from src.models.Doctor import Doctor

class Interface(ABC):
    """
    Interface abstract class
    Implements the option menu for each interface
    """
    
    # Abstract property: Options dictionary mapping option name to method
    @property
    @abstractmethod
    def options(self):
        pass

    def run(self):
        options_str = "Available options:\n"
        for i, option in enumerate(self.options):
            options_str += str(i+1) + ": " + option + "\n"

        while True:
            option = utils.get_num_choice(len(self.options), options_str, "Enter the option number: ", exit=True)
            if not option:
                return
            
            self.options[list(self.options.keys())[option-1]]()

    def doctorSearch(speciality=None):
        options_str = "Available options:\n"

        for i, option in enumerate(("Search Doctor","Choose Doctor")):
            options_str = str(i+1) + ": " + option + "\n"
        
        choice = utils.get_num_choice(2, options_str, "Enter the option number: ")

        if choice == 1:
            print("=====================================")
            firstNameToSearch = input("First name: ")
            lastNameToSearch = input("Last name: ")
            print("=====================================")
            get_doctors = lambda page_num: Doctor.searchDoctorsByName(firstNameToSearch, lastNameToSearch, page_num=page_num)

        else:
            get_doctors = lambda page_num: Doctor.getDoctorsBySpeciality(speciality, page_num=page_num)

        page = 0
        doctors = []
        while True:
            while len(doctors) == 0:
                page -= 1
                doctors = get_doctors(page)

            options_str = f"Available options, page {page+1}:\n"

            for i, doctor in enumerate(doctors):
                options_str += str(i+1) + ": " + doctor[0] + doctor[1] + ", " + doctor[2] + "\n"

            choice = utils.get_num_choice(len(doctors)+1, options_str, "Enter the doctor number: ", other=["next", "prev"])

            if choice == "next":
                page += 1
            elif choice == "prev":
                if page > 0:
                    page -= 1
            else:
                return Doctor(doctors[choice-1][3])
