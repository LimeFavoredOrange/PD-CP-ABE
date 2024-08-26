import random
from collections import Counter
import json


original_list = [
    "((Female and ((Admin or Remote) and VIP)) or ((Remote or Regular) and (VIP and Student)))",
    "((HR and Guest) and Manager)",
    "((Engineer or Regular) or Admin)",
    "((((Manager or ((VIP and VIP) or HR)) or HR) or (Junior or Engineer)) and Admin)",
    "((Trusted and (VIP or (Friend or Senior))) or ((((Male and Regular) or Admin) or (Student and Trusted)) or Male))",
    "((Junior or Remote) or (Engineer and (Developer and Manager)))",
    "((Legal and ((Developer or Female) or (HR or Manager))) or (((Developer or Local) or Legal) and Remote))",
    "(((((Developer or Friend) or Admin) and Sales) or Admin) and ((VIP and HR) or Student))",
    "((Developer or ((HR and Junior) or Male)) and VIP)",
    "(((Admin or VIP) and Regular) or ((Engineer or (Remote or Trusted)) and HR))",
    "((Guest and Engineer) and (Senior or ((Admin or HR) and Female)))",
    "(((Admin or Legal) or ((Senior or Guest) and VIP)) and ((Female or ((Visitor or Developer) and Friend)) and Manager))",
    "(Regular and ((Engineer and Regular) and (Visitor or VIP)))",
    "((((Male and VIP) or (Legal or Local)) and ((Legal and Engineer) and Admin)) and (((Guest and Friend) or ((Visitor and Junior) or Local)) and Trusted))",
    "((Friend and (((Admin and Developer) or VIP) or (Trusted or Guest))) or (Senior and VIP))",
    "(((Remote and Friend) or Developer) or ((Local and ((Admin or Friend) and Trusted)) or (Student and Regular)))",
    "(Manager and Legal)",
    "Visitor",
    "((Admin and (((Male or Female) and Local) or Guest)) or ((((Visitor or Local) and Admin) and Admin) or Local))",
    "Engineer",
    "(((VIP and ((Remote or VIP) and Remote)) or Remote) or Male)",
    "(Local or (Engineer and ((HR or Manager) or VIP)))",
    "((((((Student or Junior) or Student) and Manager) or Remote) and Legal) and Visitor)",
    "((Female or (((Trusted or VIP) or Local) and Manager)) and VIP)",
    "(Manager and (((Visitor or Female) or Admin) and ((Developer and Admin) or Engineer)))",
    "(Trusted and ((Friend or Local) or ((Guest and Junior) and Guest)))",
    "(Regular and ((Remote or Sales) or (Manager or Regular)))",
    "((Admin and ((Visitor and Admin) or ((Female and Developer) or HR))) or Manager)",
    "Student",
    "((Student and Admin) and (Junior or HR))"
]


# Generate a new list containing 1500 elements, and each element appears as evenly as possible
new_list = random.choices(original_list, k=1500)

# Count the number of times each element appears
counts = Counter(new_list)
for item, count in counts.items():
    print(f"'{item}' appears {count} times.")

# Save it to the tile
with open("./twitter_access_policies_duplicate_1500.json", "w") as file:
    file.write(json.dumps(new_list))
