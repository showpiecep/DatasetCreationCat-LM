import pandas as pd
import json
import subprocess
import sys
import os
from file_utils import *
from framework_utils import *


if __name__ == '__main__':
    repo_dir = sys.argv[1] if len(sys.argv) > 1 else '/data/GitHubMining/RawTestData/'
    test_exec_file = sys.argv[2] if len(sys.argv) > 2 else '/data/GitHubMining/test_exec_filtered.json'
    org = sys.argv[3]
    proj = sys.argv[4]
    language = sys.argv[5]
    log_file = sys.argv[6]
    image = sys.argv[7]
    filepairs_path = sys.argv[8]

    with open(test_exec_file, "r") as f:
        proj_data = json.load(f)
    
    proj_info = proj_data[language][org][proj]


    log_res = {}
    if os.path.exists(log_file):
        with open(log_file, "r") as f:
            log_res = json.load(f)    

    cwd = os.getcwd()
    os.chdir(os.path.join(repo_dir, language, org, proj))
    clean_proj()
    setup_project(proj_info, language, image)

    with open(filepairs_path, "r") as f:
        file_pairs = json.load(f)

    for i in range(len(file_pairs["code_filename"])):
        source_fn = file_pairs["code_filename"][i]
        test_fn = file_pairs["test_filename"][i]
        
        if "/build/" in source_fn or "/build/" in test_fn or ".eggs" in source_fn or ".eggs" in test_fn:
            continue

        log_key = f"{source_fn}____{test_fn}"
        
        code_non_trivial = filter_file_java(source_fn) if language == "java" else 3 # for python there can be files without methods still tested
        test_non_trivial = filter_file_java(test_fn) if language == "java" else filter_file_python(test_fn)

        if test_non_trivial > 0 and code_non_trivial > 0:
            curr_res = log_res[log_key] if log_key in log_res else {}
            if "base_coverage" not in curr_res:
                clean_proj(proj_info["clean_cmd"])
                status, coverage = run_tests(proj_info, source_fn, test_fn, language, image)
                curr_res["base_coverage"] = {"status": status, "line_coverage": coverage}


            log_res[log_key] = curr_res
            
    with open(log_file, "w") as f:
        json.dump(log_res, f)

    clean_proj()
    os.chdir(cwd)

