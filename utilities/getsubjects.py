import json

# Load subjects into subject_list
with open("apidata/subjects.json", "r") as f:
    subject_list = json.load(f)
