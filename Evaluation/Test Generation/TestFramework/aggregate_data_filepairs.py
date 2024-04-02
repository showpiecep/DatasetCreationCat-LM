import sys
import os
import json
import random

def compute_results(root_dir):
    results_dict = {}
    N = 10
    for filename in os.listdir(root_dir):
        org, proj = filename.split("____")[0], filename.split("____")[1].split(".json")[0]
        with open(os.path.join(root_dir, filename), "r") as f:
            proj_info = json.load(f)
            proj_results = []
            for log_key in proj_info:
                file_pair_data = proj_info[log_key]
                source_fn, test_fn = log_key.split("____")[0], log_key.split("____")[1]
                label = "base_coverage"
                results = file_pair_data[label]
                if results["status"] == "SUCCESS" and results["line_coverage"] != "NOT FOUND":
                    proj_results.append([source_fn, test_fn])                            
            random.shuffle(proj_results)
            first_n = proj_results[:N]
            if org not in results_dict and len(first_n) > 0:
                results_dict[org] = {}
            
            if len(first_n) > 0:
                results_dict[org][proj] = first_n

    return results_dict


if __name__ == '__main__':
    aggregation_dir = sys.argv[1] if len(sys.argv) > 1 else '/data/GitHubMining/TestFramework/'
    filepairs_dir = sys.argv[2] if len(sys.argv) > 2 else '/data/GitHubMining/TestFramework/TestingLLM/'


    python_dir = os.path.join(aggregation_dir, "python", "results")
    java_dir = os.path.join(aggregation_dir, "java", "results")

    python_results = compute_results(python_dir)
    java_results = compute_results(java_dir)

    with open(os.path.join(filepairs_dir, "python_filepairs.json"), "w") as f:
        json.dump(python_results, f)
    
    with open(os.path.join(filepairs_dir, "java_filepairs.json"), "w") as f:
        json.dump(java_results, f)

    