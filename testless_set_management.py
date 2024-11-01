import json
import os

def create_testless_set(file_name):
    with open(f".\\data\\mbpp\\full\\{file_name}.json", 'r') as file:
        data = json.load(file)

    for item in data['list']:
        item.pop('test_list', None)
        item.pop('test_setup_code', None)
        item.pop('challenge_test_list', None)
    
    testless_file_name = f"{file_name}-no-tests"
    with open(f".\\data\\mbpp\\testless\\{testless_file_name}.json", 'w') as file:
        json.dump(data, file, indent=4)
    
    return testless_file_name


def remove_testless_set(file_name):
    os.remove(f".\\data\\mbpp\\testless\\{file_name}-no-tests.json")

create_testless_set('test-00000-of-00001')
create_testless_set('prompt-00000-of-00001')
create_testless_set('train-00000-of-00001')
create_testless_set('validation-00000-of-00001')