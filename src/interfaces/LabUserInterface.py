from src.interfaces.Interface import Interface
from src.models.LabUser import LabUser
from src.models.Sample import Sample
from src.models.Doctor import Doctor
import src.utils as utils

class LabUserInterface(Interface):
    def __init__(self):
        labuser_id = 20
        self.labuser = LabUser(labuser_id)

    @property
    def options(self):
        return {
            "Submit Analysis": self.submit_analysis,   
        }
    
    def submit_analysis(self):
        print("View samples to analyze")
        
        samples = Sample.getSamplesForLabUser(self.labuser.id)

        options_str = "Available options:\n"

        for i, sample in enumerate(samples):
            options_str += str(i+1) + ": " + sample.sample_id + ((" " + sample.description) if sample.description is not None else "") + "\n"

        choice = utils.get_num_choice(len(samples)+1, options_str, "Enter the sample number: ")
        chosen_sample = samples[choice-1]

        while True:
            submit = input("Submit analysis? (y/n): ").lower()
            if submit == "y":
                chosen_sample.setResult(input("Enter result: "))
                break
            elif submit == "n":
                return
            
            print("Invalid input")

        doctor = Doctor(chosen_sample.doctor_id)
        doctor.addNotification(f"Sample {chosen_sample.sample_id} has been analyzed.", "AnalysisResult", chosen_sample.sample_id)
    