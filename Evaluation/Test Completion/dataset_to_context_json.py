import sys
import json
import os
import pathlib
import random

def open_jsonl(file_path):
    with open(file_path, 'r') as json_file:
        json_list = list(json_file)
    return json_list


N = 1000
def dataset_to_context(sampled_json, data_dir, downloads_dir, model_json, teco_json):
    context = []
    teco_ids = []
    test_method_keys = open_jsonl(os.path.join(data_dir, "test_mkey.jsonl"))
    test_method_projects = open_jsonl(os.path.join(data_dir, "proj_name.jsonl"))
    test_method_statements = open_jsonl(os.path.join(data_dir, "test_stmts.jsonl"))
    source_method_keys = open_jsonl(os.path.join(data_dir, "focal_mkey.jsonl"))
    
    id = 0
    for i in range(len(sampled_json)):
        index = int(sampled_json[i].split("csn-")[1])
        test_method_key = test_method_keys[index].replace('"', '').split("#")[0].strip()
        test_method_project = test_method_projects[index].replace('"', '').strip()
        test_method_statement = json.loads(test_method_statements[index])
        source_method_key = source_method_keys[index].replace('"', '').split("#")[0].strip()
        project_dir = os.path.join(downloads_dir, test_method_project)
        source_files = sorted(pathlib.Path(downloads_dir).glob(f"**/{source_method_key}.java"))
        test_files = sorted(pathlib.Path(downloads_dir).glob(f"**/{test_method_key}.java"))
        if len(source_files) == 0 or len(test_files) == 0:
            continue

        source_file = source_files[0]
        test_file = test_files[0]
        print(source_file)
        print(test_file)
        statement_ind = random.randint(0, len(test_method_statement) - 1)
        first_line = statement_ind == 0
        last_line = statement_ind == len(test_method_statement) - 1
        print(test_method_statement[statement_ind][1].split("-")[0])
        curr_context = {
            "id": id,
            "index": index,
            "source_file": str(source_file),
            "test_file": str(test_file),
            "statement_ind": statement_ind,
            "first_line": first_line,
            "last_line": last_line,
            "line_number": test_method_statement[statement_ind][1].split("-")[0]
        }
        context.append(curr_context)
        teco_ids.append(f"csn-{index}")
        id += 1

        if len(context) == N:
            break
        
    with open(model_json, "w") as f:
        json.dump(context, f, indent=4)
    
    with open(teco_json, "w") as f:
        json.dump(teco_ids, f)

if __name__ == "__main__":
    test_json = sys.argv[1] if len(sys.argv) > 1 else "/code/teco/_work/setup/CSNm/split/test.json"
    data_dir = sys.argv[2] if len(sys.argv) > 2 else "/code/teco/_work/data"
    downloads_dir = sys.argv[3] if len(sys.argv) > 3 else "/code/teco/_work/downloads"
    model_json = sys.argv[4] if len(sys.argv) > 4 else "/code/teco/_work/setup/CSNm/split/test_model.json"
    teco_json = sys.argv[5] if len(sys.argv) > 5 else "/code/teco/_work/setup/CSNm/split/test_teco.json"

    with open(test_json, 'r') as json_file:
        json_list = json.load(json_file)

    random.shuffle(json_list)
    context = dataset_to_context(json_list, data_dir, downloads_dir, model_json, teco_json)