import sys
import json
import os


def compute_results(data):
    unique_projs = 0
    unique_filepairs = 0

    for org in data:
        for proj in data[org]:
            unique_projs += 1
            unique_filepairs += len(data[org][proj])
    
    return unique_projs, unique_filepairs

if __name__ == '__main__':
    aggregation_dir = sys.argv[1] if len(sys.argv) > 1 else '/data/GitHubMining/TestFramework/'
    
    with open(os.path.join(aggregation_dir, "java_filepairs.json"), "r") as f:
        java_data = json.load(f)
    
    with open(os.path.join(aggregation_dir, "python_filepairs.json"), "r") as f:
        python_data = json.load(f)

    
    java_unique_projs, java_unique_filepairs = compute_results(java_data)
    python_unique_projs, python_unique_filepairs = compute_results(python_data)

    res_obj = {
        "java_unique_projs": java_unique_projs,
        "java_unique_filepairs": java_unique_filepairs,
        "python_unique_projs": python_unique_projs,
        "python_unique_filepairs": python_unique_filepairs
    }
    print(res_obj)
    with open(os.path.join(aggregation_dir, "filepair_stats.json"), "w") as f:
        json.dump(res_obj, f)