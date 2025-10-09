import json

def get_test_data(context):

    with open(context["testdata"]) as json_file:
        json_data = json.load(json_file)
        env = context.get("env")
        if env in json_data:
            return json_data[env]
        
    return{}