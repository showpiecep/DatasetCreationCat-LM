import sys
import os
import json
from file_utils import *
from concurrent.futures import ProcessPoolExecutor


MAX_WORKERS = 16

def run_project(org, proj, language, results_file, home_dir, data_dir, log_dir, lang_data_file, test_data_dir, image, fp_data_file, proj_completions_dir):
    print(f"docker run --rm -it --mount type=bind,src={home_dir},dst=/code --mount type=bind,src={data_dir},dst=/data {image} python3 framework.py {test_data_dir} {lang_data_file} {org} {proj} {language} {results_file} {image} {fp_data_file} {proj_completions_dir} 2>&1 | tee {log_dir}/{org}_{proj}_full.txt")
    os.system(f"docker run --rm -it --mount type=bind,src={home_dir},dst=/code --mount type=bind,src={data_dir},dst=/data {image} python3 framework.py {test_data_dir} {lang_data_file} {org} {proj} {language} {results_file} {image} {fp_data_file} {proj_completions_dir} 2>&1 | tee {log_dir}/{org}_{proj}_full.txt")


def run_project_helper(args):
    run_project(*args)

def process_inputs(lang_data, lang_data_file, fp_data, fp_data_file, test_data_dir, language, home_dir, data_dir, log_dir, completions_dir):
    arguments = []
    for org in fp_data:
        for project in fp_data[org]:
            results_file = os.path.join(log_dir, language, "results", f"{org}____{project}_v2.json")
            proj_log_dir = os.path.join(log_dir, language, "logs")
            proj_completions_dir = os.path.join(completions_dir, language, org, project)
            image = lang_data[org][project]["image"]

            os.makedirs(os.path.dirname(results_file), exist_ok=True)
            os.makedirs(proj_log_dir, exist_ok=True)
                
            arguments.append((org, project, language, results_file, home_dir, data_dir, proj_log_dir, lang_data_file, test_data_dir, image, fp_data_file, proj_completions_dir))
    
    with ProcessPoolExecutor(max_workers=MAX_WORKERS) as executor:
        for _ in executor.map(run_project_helper, arguments):
            pass
    


if __name__ == '__main__':
    test_filtered_output_dir = sys.argv[1] if len(sys.argv) > 1 else '/data/GitHubMining/'
    log_dir = sys.argv[2] if len(sys.argv) > 2 else '/data/GitHubMining/TestFramework/TestingLLM/'
    home_dir = sys.argv[3] if len(sys.argv) > 3 else '/home/projects/SoftwareTesting/FileLevel/TestFramework'
    data_dir = sys.argv[4] if len(sys.argv) > 4 else '/data'
    completions_dir = sys.argv[5] if len(sys.argv) > 5 else '/data/GitHubMining/Generated_TestOutputs'
    framework_dir = sys.argv[6] if len(sys.argv) > 6 else '/data/GitHubMining/TestFramework/'

    proj_data_file = os.path.join(test_filtered_output_dir, "test_exec_filtered.json")
    with open(proj_data_file, "r") as f:
        proj_data = json.load(f)

    test_data_dir = os.path.join(test_filtered_output_dir, "RawDataSample")

    java_fp_path = os.path.join(framework_dir, "java_filepairs.json")
    python_fp_path = os.path.join(framework_dir, "python_filepairs.json")

    with open(java_fp_path, "r") as f:
       java_data = json.load(f)

    with open(python_fp_path, "r") as f:
        python_data = json.load(f)

    process_inputs(proj_data["java"], proj_data_file, java_data, java_fp_path, test_data_dir, "java", home_dir, data_dir, log_dir, completions_dir)
    process_inputs(proj_data["python"], proj_data_file, python_data, python_fp_path, test_data_dir, "python", home_dir, data_dir, log_dir, completions_dir)