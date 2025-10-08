import json

def get_test_data(context):

    with open(context["testdata"]) as json_file:
        json_data = json.load(json_file)
        for data in json_data:
            if data['env'] == context["env"]:
                return data["data"]
    return {}