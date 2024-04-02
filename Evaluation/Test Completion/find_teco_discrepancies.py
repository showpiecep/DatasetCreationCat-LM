import sys
import json

if __name__ == "__main__":
    test_json = sys.argv[1] if len(sys.argv) > 1 else "/code/teco/_work/setup/CSNm/split/test_model.json"
    with open(test_json, 'r') as json_file:
        json_list = json.load(json_file)


    num_cases = 0
    for item in json_list:
        if item['source_file'] == item['test_file']:
            num_cases += 1
    
    print(f"Number of cases: {num_cases}")