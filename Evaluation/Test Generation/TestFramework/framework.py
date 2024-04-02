import pandas as pd
import json
import subprocess
import sys
import os
from framework_utils import *


def get_baseline_coverages(proj_info, fp_dir, base_fn, extension, source_fn, test_fn, language, image, curr_res, is_java=False):
    if "base_coverage" not in curr_res:
        status, coverage = run_tests(proj_info, source_fn, test_fn, language, image)
        curr_res["base_coverage"] = {"status": status, "line_coverage": coverage}

    if "preamble" not in curr_res:
        curr_res["preamble"] = {"status": "SUCCESS", "line_coverage": 0.0}

    if os.path.exists(f"{fp_dir}/{base_fn}_without_last_test_baseline.{extension}") and "all_but_one" not in curr_res:
        clean_proj(proj_info["clean_cmd"], is_java=is_java)
        os.system(f"cp {fp_dir}/{base_fn}_without_last_test_baseline.{extension} {test_fn}")
        status, coverage = run_tests(proj_info, source_fn, test_fn, language, image)
        curr_res["all_but_one"] = {"status": status, "line_coverage": coverage}

    if os.path.exists(f"{fp_dir}/{base_fn}_first_test_baseline.{extension}") and "first_test" not in curr_res:
        clean_proj(proj_info["clean_cmd"], is_java=is_java)
        os.system(f"cp {fp_dir}/{base_fn}_first_test_baseline.{extension} {test_fn}")
        status, coverage = run_tests(proj_info, source_fn, test_fn, language, image)
        curr_res["first_test"] = {"status": status, "line_coverage": coverage}


def get_tests_coverage(proj_info, fp_dir, extension, source_fn, test_fn, language, image, curr_res, is_java=False):
    tests_dir = os.path.join(fp_dir, "incremental_test_files")
    num_files = len(os.listdir(tests_dir))
    for i in range(num_files):
        test_filename = test_fn.split('/')[-1][:-5] if language == "java" else test_fn.split('/')[-1][:-3]
        label = f"tests{i}"
        if label not in curr_res:
            clean_proj(proj_info["clean_cmd"], is_java=is_java)
            os.system(f"cp {tests_dir}/{test_filename}_{i+1}.{extension} {test_fn}")
            status, coverage = run_tests(proj_info, source_fn, test_fn, language, image)
            curr_res[f"tests{i}"] = {"status": status, "line_coverage": coverage}


def lm_testing(proj_info, fp_dir, completions_arr, source_fn, test_fn, language, image, curr_res, is_java=False):
    base_fn, extension = test_fn.split("/")[-1].split(".")
    get_baseline_coverages(proj_info, fp_dir, base_fn, extension, source_fn, test_fn, language, image, curr_res, is_java=is_java)
    get_tests_coverage(proj_info, fp_dir, extension, source_fn, test_fn, language, image, curr_res, is_java=is_java)

    for prefix, num_completions_per_file in completions_arr:
        fp_completions_dir = os.path.join(fp_dir, prefix)

        if os.path.exists(fp_completions_dir):

            for i in range(num_completions_per_file):
                key = f"{prefix}_{i}"
                if key not in curr_res:
                    completion_fn = f"{base_fn}__n{i}.{extension}"
                    if os.path.exists(f"{fp_completions_dir}/{completion_fn}"):
                        clean_proj(proj_info["clean_cmd"], is_java=is_java)
                        os.system(f"cp {fp_completions_dir}/{completion_fn} {test_fn}")
                        status, coverage = run_tests(proj_info, source_fn, test_fn, language, image)
                        curr_res[key] = {"status": status, "line_coverage": coverage}
    os.system(f"git checkout {test_fn}")
    return curr_res

if __name__ == '__main__':
    repo_dir = sys.argv[1] if len(sys.argv) > 1 else '/data/GitHubMining/RawTestData/'
    test_exec_file = sys.argv[2] if len(sys.argv) > 2 else '/data/GitHubMining/test_exec_filtered.json'
    org = sys.argv[3]
    proj = sys.argv[4]
    language = sys.argv[5]
    log_file = sys.argv[6]
    image = sys.argv[7]
    filepairs_path = sys.argv[8]
    proj_completions_dir = sys.argv[9]

    with open(test_exec_file, "r") as f:
        proj_data = json.load(f)
    
    proj_info = proj_data[language][org][proj]


    log_res = {}
    if os.path.exists(log_file):
        with open(log_file, "r") as f:
            log_res = json.load(f)    

    cwd = os.getcwd()
    os.chdir(os.path.join(repo_dir, language, org, proj))
    is_java = ""
    if language == "java":
        is_java = "maven" if "maven" in image else "gradle"
    clean_proj(is_java=is_java)
    setup_project(proj_info, language, image)

    with open(filepairs_path, "r") as f:
        file_pairs = json.load(f)
    
    proj_filepairs = file_pairs[org][proj]
    for i, (source_fn, test_fn) in enumerate(proj_filepairs):
        log_key = f"{source_fn}____{test_fn}"
        curr_res = log_res[log_key] if log_key in log_res else {}
        completions_arr = [
            ("t0.2_n10", 60),
            # ("t0.8_n10", 60),
            ("codegen-16B-multi_t0.2_n10", 30),
            ("codegen-2B-multi_t0.2_n10", 30),
            ("codegen-2B-multi_t0.2_n10_v2", 30),
            ("codegen-16B-mono_t0.2_n10", 30),
            ("codegen-2B-mono_t0.2_n10", 30),
        ]
        fp_dir = os.path.join(proj_completions_dir, f"filepair{i}")
        print(fp_dir)
        curr_res = lm_testing(proj_info, fp_dir, completions_arr, source_fn, test_fn, language, image, curr_res, is_java=is_java)

        log_res[log_key] = curr_res
            
    with open(log_file, "w") as f:
        json.dump(log_res, f)

    clean_proj(is_java=is_java)
    os.chdir(cwd)

