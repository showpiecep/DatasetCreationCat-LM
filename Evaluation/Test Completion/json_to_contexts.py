import sys
import json
from tqdm import tqdm
import os

def get_file_text(file_path):
    with open(file_path, 'r') as f:
        file_contexts = f.read()
    return file_contexts

def json_to_contexts(json_list, contexts_dir):
    for item in tqdm(json_list):
        context = ''
        
        source_fp = item['source_file']
        test_fp = item['test_file']

        contexts_root = os.path.join(contexts_dir, str(item['id']))
        os.makedirs(contexts_root, exist_ok=True)

        code_context = get_file_text(source_fp)
        context += code_context
        test_context = get_file_text(test_fp)
        test_lines = test_context.split('\n')
        test_prev = test_lines[:int(item['line_number'])-1]
        test_context = "\n".join(test_prev)
        context += "\n<|codetestpair|>\n"
        context += test_context
        context += '\n<|end_prompt|>\n'

        context += test_context
        context += '\n<|end_prompt|>\n'

        test_fn = test_fp.split('/')[-1][:-5]
        code_fn = source_fp.split('/')[-1][:-5]
        context_fn = os.path.join(contexts_root, f"{test_fn}-{code_fn}_contexts.txt")
        test_fp_baseline = os.path.join(contexts_root, f"{test_fn}_baseline.java")

        os.system(f"cp {test_fp} {test_fp_baseline}")
        
        with open(context_fn, 'w') as f:
            f.write(context)
                

if __name__ == "__main__":
    test_json = sys.argv[1] if len(sys.argv) > 1 else "/code/teco/_work/setup/CSNm/split/test_model.json"
    contexts_dir = sys.argv[2] if len(sys.argv) > 2 else "/data/GitHubMining/TecoContexts"

    with open(test_json, 'r') as json_file:
        json_list = json.load(json_file)


    json_to_contexts(json_list, contexts_dir)