import sys
import json
import os


def test_stmts_to_indices(id_jsonl, id_line, order):
    test_stmts_indices_map = {}
    
    with open(id_jsonl, 'r') as id_file:
        id_list = list(id_file)
        
    curr_id = ""
    curr_ind = 0
    for i in range(len(id_list)):
        new_id = id_list[i].replace('"', '').strip()

        if new_id != curr_id:
            curr_id = new_id
            curr_ind = 0
        
        if curr_id in id_line:
            statement_ind = id_line[curr_id]
            if statement_ind == curr_ind:
                test_stmts_indices_map[curr_id] = i

        curr_ind += 1
    
    test_stmts_indices = [test_stmts_indices_map[id] for id in order]
    return test_stmts_indices

def file_to_sampled_file(teco_exp_old_dir, teco_exp_dir, file_name, sampled_indices):
    old_file = os.path.join(teco_exp_old_dir, "test", file_name)
    new_file = os.path.join(teco_exp_dir, "test", file_name)
    with open(old_file, 'r') as old_file:
        old_list = list(old_file)
    new_list = [old_list[i] for i in sampled_indices]
    with open(new_file, 'w') as new_file:
        new_file.writelines(new_list)

def sample_copy_dir(json_list, teco_exp_old_dir, teco_exp_dir):
    id_line = {f"csn-{e['index']}": e['statement_ind'] for e in json_list}
    order = [f"csn-{e['index']}" for e in json_list]

    test_dir = os.path.join(teco_exp_old_dir, "test")
    id_line_jsonl = os.path.join(test_dir, "id.jsonl")
    indices = test_stmts_to_indices(id_line_jsonl, id_line, order)

    for file_name in os.listdir(test_dir):
        if file_name.endswith(".jsonl"):
            print(file_name)
            file_to_sampled_file(teco_exp_old_dir, teco_exp_dir, file_name, indices)

if __name__ == "__main__":
    test_json = sys.argv[1] if len(sys.argv) > 1 else "/code/teco/_work/setup/CSNm/split/test_model.json"
    teco_exp_old_dir = sys.argv[2] if len(sys.argv) > 2 else "/code/teco/_work/setup/CSNm/eval-any-stmt_actual"
    teco_exp_dir = sys.argv[3] if len(sys.argv) > 3 else "/code/teco/_work/setup/CSNm/eval-any-stmt"

    with open(test_json, 'r') as json_file:
        json_list = json.load(json_file)

    os.makedirs(teco_exp_dir, exist_ok=True)
    os.system(f"cp -r {teco_exp_old_dir}/* {teco_exp_dir}")
    sample_copy_dir(json_list, teco_exp_old_dir, teco_exp_dir)