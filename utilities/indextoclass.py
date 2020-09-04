import json

# Load index class mapping into index_to_class
with open("apidata/indextoclass.json", "r") as f:
    index_to_class = json.load(f)
