import os
import json
import sys

def build_results_set_cov_results(results):
    results_set = set()
    for line in results:
        split_line = line.split(",")
        if len(split_line) > 1:
            org = split_line[0].strip()
            proj = split_line[1].strip()
            results_set.add((org, proj))
    
    return results_set

def build_results_set_links(results):
    results_set = set()
    for line in results:
        project_link = line.split('\t')[0]
        if project_link.endswith('/'):
            project_link = project_link[:-1]
        *_, org, proj = project_link.split('/')
        results_set.add((org, proj))
    
    return results_set

if __name__ == '__main__':
    results_dir = sys.argv[1] if len(sys.argv) > 1 else '/data/GitHubMining/'
    framework_dir = os.path.join(results_dir, "TestFramework")
    output_dir = os.path.join(results_dir, "RawDataSampleOutput")

    with open(os.path.join(framework_dir, "java_coverage_results.txt"), "r") as f:
        java_results = f.read().split("\n")

    with open(os.path.join(framework_dir, "python_coverage_results.txt"), "r") as f:
        python_results = f.read().split("\n")

    print(len(java_results))
    print(len(python_results))
    java_projects_cov = build_results_set_cov_results(java_results)
    python_projects_cov = build_results_set_cov_results(python_results)

    with open(os.path.join(results_dir, f"test_filtered_fp_python.txt"), "r") as f:
        python_repos_links = f.read().split('\n')
    
    with open(os.path.join(results_dir, f"test_filtered_fp_java.txt"), "r") as f:
        java_repos_links = f.read().split('\n')

    java_projects_links = build_results_set_links(java_repos_links)
    python_projects_links = build_results_set_links(python_repos_links)
    print(len(java_projects_cov))
    print(len(python_projects_cov))
    missing_projs = python_projects_links - python_projects_cov
    proj_fps = []

    for org, proj in missing_projs:
        filepairs_path = os.path.join(output_dir, "python", 'FilePairs', 'filepairs_' + org + '__' + proj + '.json')
        with open(filepairs_path, "r") as f:
            file_pairs = json.load(f)
            
            proj_fps.append([org, proj, len(file_pairs["code_filename"])])

    # print(sorted(proj_fps, key=lambda x:x[2], reverse=True))