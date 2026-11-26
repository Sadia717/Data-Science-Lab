#21-11-26
# Data types and variables
hospital = "City Care Clinic"
patients_today = 4
fee = 350.0
is_open = True
contact = None
reading = 3 + 4j

print("Patient Health Indicator System")
print("=" * 40)

for name, value in [
    ("hospital", hospital), ("patients_today", patients_today),
    ("fee", fee), ("is_open", is_open),
    ("contact", contact), ("reading", reading)
]:
    print(name, "=", value, "| type =", type(value).__name__)

# Expressions
print("\nTotal fee:", patients_today * fee)
print("17 // 5, 17 % 5, 2 ** 10:", 17 // 5, 17 % 5, 2**10)
print("Fee > 300 and clinic open:", fee > 300 and is_open)
print("Type conversion:", int("45") + 5)
print("Complex absolute value:", abs(reading))

# Functions
def bmi(weight, height):
    return round(weight / height**2, 2)

def bmi_category(b):
    if b < 18.5: return "Underweight"
    if b < 25: return "Normal"
    if b < 30: return "Overweight"
    return "Obese"

def bp_status(systolic, diastolic=80):
    if systolic >= 140 or diastolic >= 90: return "High"
    if systolic < 90 or diastolic < 60: return "Low"
    return "Normal"

def average(*values):
    return round(sum(values) / len(values), 2)

def summary(**details):
    return ", ".join(f"{k}={v}" for k, v in details.items())

risk_score = lambda age, b: round(0.03*age + 0.05*b, 2)

# Class and objects
class Patient:
    count = 0

    def __init__(self, name, age, weight, height, sys, dia):
        self.name, self.age = name, age
        self.weight, self.height = weight, height
        self.sys, self.dia = sys, dia
        Patient.count += 1

    def report(self):
        b = bmi(self.weight, self.height)
        return f"{self.name} Age {self.age} | BMI {b} ({bmi_category(b)}) | BP {self.sys}/{self.dia} ({bp_status(self.sys,self.dia)}) | Risk {risk_score(self.age,b)}"

    def __str__(self):
        return f"Patient({self.name}, {self.age})"

patients = [
    Patient("Arun", 52, 82, 1.70, 145, 92),
    Patient("Sneha", 28, 54, 1.62, 112, 74),
    Patient("Gopal", 65, 60, 1.68, 88, 58),
    Patient("Nisha", 41, 95, 1.60, 130, 85)
]

print("\nPatient reports:")
for p in patients:
    print(p.report())

print("\nObjects created:", Patient.count)
print("Object string:", patients[0])
print("isinstance:", isinstance(patients[0], Patient))
print("Average age:", average(*[p.age for p in patients]))
print("Summary:", summary(clinic=hospital, patients=Patient.count, fee=fee))
print("Default BP:", bp_status(120))
print("BMI function doc:", bmi.__doc__)
