import sys
import os
import json
import random

def compute_results(root_dir, old_fps):
    results_dict = {}
    N = 10
    unique_projs = 0
    unique_filepairs = 0

    for filename in os.listdir(root_dir):
        print(filename)
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
            
            old_fps_arr = old_fps[org][proj] if org in old_fps and proj in old_fps[org] else []
            new_results = []
            for fp in old_fps_arr:
                if fp in proj_results:
                    new_results.append(fp)

            new_proj_results = []
            for fp in proj_results:
                if fp not in old_fps_arr:
                    new_proj_results.append(fp)
            
            first_n = new_proj_results[:N-len(new_results)]
            new_results += first_n
            if org not in results_dict and len(new_results) > 0:
                unique_projs += 1
                results_dict[org] = {}
            
            if len(new_results) > 0:
                unique_filepairs += len(new_results)
                results_dict[org][proj] = new_results

    return results_dict


def fp_diff(old_fps, new_fps):
    added_items = []
    removed_items = []

    orgs = set(old_fps.keys()).union(set(new_fps.keys()))
    projs = set()
    for org in orgs:
        if org in old_fps:
            projs = projs.union(set(old_fps[org].keys()))
        if org in new_fps:
            projs = projs.union(set(new_fps[org].keys()))

    for org in orgs:
        for proj in projs:
            new_fps_arr = new_fps[org][proj] if org in new_fps and proj in new_fps[org] else []
            old_fps_arr = old_fps[org][proj] if org in old_fps and proj in old_fps[org] else []
            for fp in new_fps_arr:
                if fp not in old_fps_arr:
                    added_items.append(fp)
            for fp in old_fps_arr:
                if fp not in new_fps_arr:
                    removed_items.append(fp)

    return added_items, removed_items


if __name__ == '__main__':
    aggregation_dir = sys.argv[1] if len(sys.argv) > 1 else '/data/GitHubMining/TestFramework/TestingLLM'
    fp_dir = sys.argv[1] if len(sys.argv) > 1 else '/data/GitHubMining/TestFramework/'

    python_dir = os.path.join(aggregation_dir, "python", "results")
    java_dir = os.path.join(aggregation_dir, "java", "results")

    python_fps_path = os.path.join(fp_dir, "python_filepairs.json")
    java_fps_path = os.path.join(fp_dir, "java_filepairs.json")

    with open(python_fps_path, "r") as f:
        python_fps = json.load(f)
    
    python_results = compute_results(python_dir, python_fps)
    added_python_fps, removed_python_fps = fp_diff(python_fps, python_results)

    with open(os.path.join(fp_dir, "python_filepairs_new.json"), "w") as f:
        json.dump(python_results, f, indent=4)
    
    with open(os.path.join(fp_dir, "python_filepairs_added.json"), "w") as f:
        json.dump(added_python_fps, f, indent=4)
    
    with open(os.path.join(fp_dir, "python_filepairs_removed.json"), "w") as f:
        json.dump(removed_python_fps, f, indent=4)

    java_results = compute_results(java_dir)
    with open(java_fps_path, "r") as f:
        json.dump(java_results, f)