import sys
import os
import json
from file_utils import *
from concurrent.futures import ProcessPoolExecutor


MAX_WORKERS = 16

def run_project(org, proj, language, results_file, home_dir, data_dir, log_dir, lang_data_file, test_data_dir, image, filepairs_path):
    print(f"docker run --rm -it --mount type=bind,src={home_dir},dst=/code --mount type=bind,src={data_dir},dst=/data {image} python3 framework_filepairs.py {test_data_dir} {lang_data_file} {org} {proj} {language} {results_file} {image} {filepairs_path} 2>&1 | tee {log_dir}/{org}_{proj}.txt")
    os.system(f"docker run --rm -it --mount type=bind,src={home_dir},dst=/code --mount type=bind,src={data_dir},dst=/data {image} python3 framework_filepairs.py {test_data_dir} {lang_data_file} {org} {proj} {language} {results_file} {image} {filepairs_path} 2>&1 | tee {log_dir}/{org}_{proj}.txt")

def run_project_helper(args):
    run_project(*args)

def process_inputs(lang_data, lang_data_file, test_data_dir, language, fp_dir, home_dir, data_dir, log_dir):
    arguments = []
    for org in lang_data:
        for project in lang_data[org]:
            results_file = os.path.join(log_dir, language, "results", f"{org}____{project}.json")
            proj_log_dir = os.path.join(log_dir, language, "logs")
            image = lang_data[org][project]["image"]

            os.makedirs(os.path.dirname(results_file), exist_ok=True)
            os.makedirs(proj_log_dir, exist_ok=True)
                
            filepairs_path = os.path.join(fp_dir, language, 'FilePairs', 'filepairs_' + org + '__' + project + '.json')
            with open(filepairs_path, "r") as f:
                file_pairs = json.load(f)
            
            found_non_trivial = False
            for i in range(len(file_pairs["code_filename"])):
                source_fn = file_pairs["code_filename"][i]
                test_fn = file_pairs["test_filename"][i]
                
                if "/build/" in source_fn or "/build/" in test_fn or ".eggs" in source_fn or ".eggs" in test_fn:
                    continue
                code_non_trivial = filter_file_java(source_fn) if language == "java" else 3 # for python there can be files without methods still tested
                test_non_trivial = filter_file_java(test_fn) if language == "java" else filter_file_python(test_fn)

                if test_non_trivial > 0 and code_non_trivial > 0:
                    found_non_trivial = True
                    break
                
            if found_non_trivial:
                arguments.append((org, project, language, results_file, home_dir, data_dir, proj_log_dir, lang_data_file, test_data_dir, image, filepairs_path))
    
    with ProcessPoolExecutor(max_workers=MAX_WORKERS) as executor:
        for _ in executor.map(run_project_helper, arguments):
            pass



if __name__ == '__main__':
    test_filtered_output_dir = sys.argv[1] if len(sys.argv) > 1 else '/data/GitHubMining/'
    fp_dir = sys.argv[2] if len(sys.argv) > 2 else '/data/GitHubMining/RawDataSampleOutput/'
    log_dir = sys.argv[3] if len(sys.argv) > 3 else '/data/GitHubMining/TestFramework/TestingLLM/'
    home_dir = sys.argv[4] if len(sys.argv) > 4 else '/home/projects/SoftwareTesting/FileLevel/TestFramework'
    data_dir = sys.argv[5] if len(sys.argv) > 5 else '/data'

    proj_data_file = os.path.join(test_filtered_output_dir, "test_exec_filtered.json")
    with open(proj_data_file, "r") as f:
        proj_data = json.load(f)

    test_data_dir = os.path.join(test_filtered_output_dir, "RawDataSample")


    process_inputs(proj_data["java"], proj_data_file, test_data_dir, "java", fp_dir, home_dir, data_dir, log_dir)
    process_inputs(proj_data["python"], proj_data_file, test_data_dir, "python", fp_dir, home_dir, data_dir, log_dir)